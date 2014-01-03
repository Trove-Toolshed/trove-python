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

To get an idea of the results, you can compare [this Trove list](http://trove.nla.gov.au/list?id=50196) to [the collection](https://www.zotero.org/wragge/items/collectionKey/64KM5QZX) I automagically created in my Zotero library.

##Export Trove tags

Exporting Trove tags is similar.

```python
from pyzotero import zotero
from trove_python.trove_core import trove
from trove_python.trove_zotero import export

zotero_api = zotero.Zotero('[Your Zotero user id]', 'user', '[Your Zotero API key]')
trove_api = trove.Trove(['Your Trove API key'])
exporter = export.TagExporter(trove_api, zotero_api)

exporter.export('[Your tag]')
```

To see the results compare the Trove items tagged with ['inigo'](http://trove.nla.gov.au/result?q=publictag:\(inigo\)) to [the corresponding collection](https://www.zotero.org/wragge/items/collectionKey/7JBIBPWF) in Zotero.