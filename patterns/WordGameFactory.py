class WordGameFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)

    def enumerateBuilders(self):
        return str(self._builders.keys()).lstrip("dict_keys([").rstrip("])")

    def isBuilderRegistered(self, builder):
        return self._builders.keys().__contains__(builder)
