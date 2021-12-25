class RTTITypeProxy:
    def __init__(self, type_name: str, type_registry):
        from ProjectDecima.core.rtti_types import RTTITypeRegistry

        self.type_name = type_name
        self.type_registry: RTTITypeRegistry = type_registry

    def resolve(self):
        return self.type_registry.find_by_name(self.type_name)
