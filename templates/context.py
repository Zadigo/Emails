from collections.abc import MutableMapping
from typing import OrderedDict
from zemailer.settings import configuration

class Context(MutableMapping):
    def __init__(self, **kwargs):
        self.items = OrderedDict()

    def __str__(self):
        return str(dict(self.items))

    def __delitem__(self, key):
        self.items.pop(key)

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __setitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items.values())
