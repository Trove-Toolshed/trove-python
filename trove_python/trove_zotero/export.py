import datetime
import urlparse
import os.path
import tempfile
import copy

from .mappings import TROVE_ZOTERO_MAPPINGS, FIELD_MAPPINGS
from ..trove_core.utilities import get_url
from ..trove_harvest.harvest import TroveHarvester


def guess_zotero_type(item_type):
	if isinstance(item_type, list):
		item_type = item_type[0]
	try:
		zotero_type = TROVE_ZOTERO_MAPPINGS[item_type]
	except KeyError:
		zotero_type = 'journalArticle'
	return zotero_type


def process_name(name):
	parts = name.split(',')
	if len(parts) > 1:
		family_name = parts[0]
		other_names = parts[1]
	else:
		family_name = parts[0]
		other_names = ''
	return {'family_name': family_name, 'other_names': other_names}


def extract_filename_from_url(url):
	filename = os.path.basename(urlparse.urlsplit(url).path)
	if '.' not in filename:
		filename = None
	return filename


def prepare_attachment(url, default):
	response = get_url(url)
	filename = extract_filename_from_url(url)
	if not filename:
		filename = default
	folder = tempfile.gettempdir()
	filename = os.path.join(folder, filename)
	with open(filename, 'wb') as attachment:
		attachment.write(response.read())
	return filename


def prepare_tags(tags):
	'''
	Takes a list of tags and formats in the object format expected by Zotero.
	'''
	return [{'tag': tag} for tag in tags]


def create_zotero_object(zotero_api, trove_api, record):
	attachments = []
	item_type = record.keys()[0]
	item = record[item_type]
	if item_type == 'work':
		zotero_type = guess_zotero_type(item['type'])
		zotero_template = zotero_api.item_template(zotero_type)
		template = copy.deepcopy(zotero_template)
		print template
		work = trove_api.get_item(item_id=item['id'], item_type='work')
		details = work.get_details()
		fields = FIELD_MAPPINGS[zotero_type]
		for t_field, z_field in fields.items():
			print t_field
			if t_field in details:
				template[z_field] = '; '.join(details[t_field])
		if 'contributor' in details:
			for index, contributor in enumerate(details['contributor']):
				names = process_name(contributor)
				template['creators'][index]['firstName'] = names['other_names']
				template['creators'][index]['lastName'] = names['family_name']
		tags = work.get_all_tags()
		if 'subject' in details:
			tags.extend(details['subject'])
		if tags:
			template['tags'] = prepare_tags(tags)
		source = work.get_repository()
		repository = None
		if source['nuc']:
			contributor = trove_api.get_item(item_id=source['nuc'], item_type='contributor')
			repository = contributor.get_title()
		elif source['repository']:
			repository = source['repository']
		if repository:
			template['archive'] = repository
		urls = work.get_urls()
		if 'mediumresolution' in urls:
			image_url = urls['mediumresolution']
		elif 'thumbnail' in urls:
			image_url = urls['thumbnail']
		else:
			image_url = None
		if image_url:
			attachments.append(prepare_attachment(image_url, 'image.jpg'))
		pdf_url = work.get_pdf_url()
		if pdf_url:
			attachments.append(prepare_attachment(pdf_url, 'article.pdf'))
		#print template
		
	elif item_type == 'people':
		zotero_type = 'encyclopediaArticle'
		template = zotero_api.item_template(zotero_type)
		template['title'] = 'Trove party record'
		template['url'] = item['troveUrl']

	elif item_type == 'article':
		zotero_type = 'newspaperArticle'
		template = zotero_api.item_template(zotero_type)
		template['title'] = item['heading']
		template['url'] = 'http://nla.gov.au/nla.news-article' + item['id']
		template['publicationTitle'] = item['title']['value']
		template['pages'] = item['page']
		template['date'] = item['date']
		pdf_url = 'http://trove.nla.gov.au/ndp/del/printArticlePdf/{}/3'.format(item['id'])
		response = get_url(pdf_url)
		with open('article.pdf', 'wb') as pdf:
			pdf.write(response.read())
		attachments.append('article.pdf')

	elif item_type == 'externalWebsite':
		zotero_type = 'webpage'
		template = zotero_api.item_template(zotero_type)
		template['title'] = item['title']
		template['url'] = item['identifier']['value']

	if template['itemType'] != 'webpage':
		template['libraryCatalog'] = 'Trove'
	template['accessDate'] = datetime.datetime.now().date().isoformat()
	return {'zotero_item': template, 'attachments': attachments}


def create_zotero_collection(zotero_api, list_name):
	'''
	Creates a Zotero collection with the given name,
	then retrieves the key for that collection.
	'''
	collection_key = None
	if list_name:
		created = zotero_api.create_collection({'name': list_name})
		if created:
			collections = zotero_api.collections(q=list_name)
			try:
				collection_key = collections[0]['key']
			except (IndexError, KeyError):
				print 'Error retrieving collection key.'
		else:
			print 'Error creating collection.'
	return collection_key


def export_list(list_id, zotero_api, trove_api):
	#zotero_items = []
	trove_list = trove_api.get_item(item_id=list_id, item_type='list')
	list_name = trove_list.get_title()
	collection_key = create_zotero_collection(zotero_api, list_name)
	if collection_key:
		for item in trove_list.list_items:
			details = create_zotero_object(zotero_api, trove_api, item)
			zotero_item = details['zotero_item']
			zotero_item['collections'] = [collection_key]
			response = zotero_api.create_items([zotero_item])
			print response
			if details['attachments']:
				zotero_api.attachment_simple(details['attachments'], response[0]['key'])
			#zot.addto_collection(collection_key, resp)
			#zotero_items.append(zotero_item.copy())
		#Can't get the adding of multiple items to work
		#And check_items fails
		#zot.check_items(zotero_items)
		#resp = zot.create_items(zotero_items)
		#zot.addto_collection(collection_key, resp)

class TagExport(TroveHarvester):

	def __init__(self, trove_api, zotero_api):
		TroveHarvester.__init__(self, trove_api=trove_api)
		self.zotero_api = zotero_api
		
	def process_results(self, zones):
		"""
		Do something with each set of results.
		Needs to update self.harvested
		"""
		item_type = None
		for zone in zones:
			records = zone['records']
			if int(records['n']) > 0:
				if 'work' in records:
					item_type = 'work'
				elif 'article' in records:
					item_type = 'article'
				if item_type:
					for item in records[item_type]:
						details = create_zotero_object(self.zotero_api, self.trove_api, {item_type: item})
						zotero_item = details['zotero_item']
						zotero_item['collections'] = [self.collection_key]
						response = self.zotero_api.create_items([zotero_item])
						print response
						if details['attachments']:
							self.zotero_api.attachment_simple(details['attachments'], response[0]['key'])
		self.harvested += self.get_highest_n(zones)

	def export_tag(self, tag, start=0, number=20):
		self.harvested = int(start)
		self.number = int(number)
		query_url = 'http://api.trove.nla.gov.au/result?q=publictag:("{}")&zone=all&encoding=json&key={}'
		self.query = query_url.format(tag, self.trove_api.api_key)
		collection_name = '{} (Trove tag)'.format(tag)
		self.collection_key = create_zotero_collection(self.zotero_api, collection_name)
		if self.collection_key:
			self.harvest()


		

