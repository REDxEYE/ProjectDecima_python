class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def cleanup(mcs):
        for k in mcs._instances.copy().keys():
            del mcs._instances[k]
