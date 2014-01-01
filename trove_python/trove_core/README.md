#trove-core

Basic stuff for working with Trove.

##Getting started

To set up a new Trove API connection:

```python
from trove_python.trove_core import trove

trove_api = trove.Trove('[Your Trove API key')
```
Then you can use your connection to retrieve Trove items:

```python
resource = trove_api.get_item(item_id='[Your item id]', item_type='[One of: work, article, list, contributor]')
```

The item types are:

* work -- resources in the books, articles, pictures, sound, maps and archives zones in Trove
* article -- newspaper articles
* list -- user-created Trove lists
* contributor -- Trove content partners

##Methods

Once you have an item you can use the associated methods to get useful details out.

```python
resource = trove_api.get_item(item_id='12961367', item_type='work')
resource.get_title()
```

Returns the string 'Fanny Wragge'.

```python
resource.get_details()
```

Returns the dictionary:

```python
{
	'abstract': ['Fanny Wragge, daughter of Professor Clement Wragge '],
 	'id': ['12961367'],
 	'issued': ['1885'],
 	'language': ['English', 'en'],
 	'source': 'Trove',
 	'subject': ['Wragge, Fanny', 'c. 1885'],
 	'title': ['Fanny Wragge'],
 	'troveUrl': ['http://trove.nla.gov.au/work/12961367'],
 	'type': ['Photograph'],
 	'urls': {
 		u'fulltext': u'http://images.slsa.sa.gov.au/mpcimg/18000/B17900.htm',
  		'mediumresolution': u'http://images.slsa.sa.gov.au/mpcimg/18000/B17900.jpg',
  		u'thumbnail': u'http://images.slsa.sa.gov.au/mpcimgt/18000/B17900.jpg'
  	}
 }
 ```

