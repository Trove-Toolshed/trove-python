from urllib2 import Request, urlopen, URLError, HTTPError

def get_url(url):
		response = None
		req = Request(url)
		try:
		    response = urlopen(req)
		except HTTPError as e:
		    print 'The server couldn\'t fulfill the request.'
		    print 'Error code: ', e.code
		except URLError as e:
		    print 'We failed to reach a server.'
		    print 'Reason: ', e.reason
		return response