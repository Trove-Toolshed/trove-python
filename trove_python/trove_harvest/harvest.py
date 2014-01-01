import re
import json
from urllib2 import urlopen, Request, HTTPError
from utilities import retry


class ServerError(Exception):
    pass


class TroveHarvester:
	"""
	A basic harvester for downloading records via the Trove API.
	You'll want to subclass this and, at a minimum, overwrite 
	process_results() to actually do something with the stuff
	you're harvesting.

	"""
	trove_api = None
	query = None
	harvested = 0
	number = 20

	def __init__(self, trove_api, **kwargs):
		self.trove_api = trove_api
		query = kwargs.get('query', None)
		if query:
			self.query = self._clean_query(query)
		self.harvested = int(kwargs.get('start', 0))
		self.number = int(kwargs.get('number', 20))

	def _clean_query(self, query):
		"""Remove s and n values just in case."""
		query = re.sub(r'&s=\d+', '', query)
		query = re.sub(r'&n=\d+', '', query)
		return query

	def log_query(self):
		"""Do something with details of query -- ie log date"""
		pass

	@retry(ServerError, tries=10, delay=1)
	def _get_url(self, url):
		''' Try to retrieve the supplied url.'''
		req = Request(url)
		try:
			response = urlopen(req)
		except HTTPError as e:
			if e.code == 503 or e.code == 504:
				raise ServerError("The server didn't respond")
			else:
				raise
		else:
			return response

	def harvest(self):
		number = self.number
		query_url = '{}&n={}&key={}'.format(
				self.query, 
				self.number, 
				self.trove_api.api_key
				)
		while number == self.number:
			current_url = '{}&s={}'.format(
				query_url, 
				self.harvested
				)
			print current_url
			response = self._get_url(current_url)
			try:
				results = json.load(response)
			except (AttributeError, ValueError):
				pass
				# Log errors?
			else:
				zones = results['response']['zone']
				self.process_results(zones)
				number = self.get_highest_n(zones)

	def get_highest_n(self, zones):
		n = 0
		for zone in zones:
			new_n = int(zone['records']['n'])
			if new_n > n:
				n = new_n
		return n

	def process_results(self, results):
		"""
		Do something with each set of results.
		Needs to update self.harvested
		"""
		self.harvested += self.number
