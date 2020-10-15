from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_types.resource import Resource


class ArtPartsSubModelExtraResource(Resource):
    magic = 0x3602A284B924B5D3



EntryTypeManager.register_handler(ArtPartsSubModelExtraResource)