#trove-zotero

This module provides some tools to help integrate [Trove](http://trove.nla.gov.au) and [Zotero](http://zotero.org).

Requirements:

* [PyZotero](https://github.com/urschrei/pyzotero)

##Export Trove lists

If you've installed trove_python, you should be able to export a Trove List to a Zotero collection in just a few lines of code.

```python
from pyzotero import zotero
from trove_python.trove_core import trove
from trove_python.trove_zotero import export

zotero_api = zotero.Zotero('[Your Zotero user id]', 'user', '[Your Zotero API key]')
trove_api = trove.Trove('[Your Trove API key]')

export.export_list(
	list_id='[Your Trovelist id]', 
	zotero_api=zotero_api, 
	trove_api=trove_api
	)
```