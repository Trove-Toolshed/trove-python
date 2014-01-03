from pyzotero import zotero
from trove_python.trove_core import trove
from trove_python.trove_zotero import export

from credentials import TROVE_API_KEY, ZOTERO_USER_ID, ZOTERO_API_KEY

zotero_api = zotero.Zotero(ZOTERO_USER_ID, 'user', ZOTERO_API_KEY)
trove_api = trove.Trove(TROVE_API_KEY)
exporter = export.TagExporter(trove_api, zotero_api)

exporter.export('inigo')