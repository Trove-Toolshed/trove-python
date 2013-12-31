from pyzotero import zotero
from ..trove_core import trove
from ..trove_zotero import export

from .credentials import TROVE_API_KEY, ZOTERO_USER_ID, ZOTERO_API_KEY

zotero_api = zotero.Zotero(ZOTERO_USER_ID, 'user', ZOTERO_API_KEY)
trove_api = trove.Trove(TROVE_API_KEY)
list_id = '50196'

export.export_list(
	list_id=list_id, 
	zotero_api=zotero_api, 
	trove_api=trove_api
	)