class Registry(object):
    def __init__(self):
        self._items = {}

    def add(self, class_name):
        def _add(klass):
            self._items[class_name] = klass
            return klass

        return _add

    def get(self, config):
        config = config.copy()
        klass = self.get_class(config.pop('class'))
        return klass(**config)

    def get_class(self, class_name):
        return self._items[class_name]
