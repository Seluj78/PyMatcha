"""
https://speakerdeck.com/lig/your-own-orm-in-python-how-and-why
"""


class StrictDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError("{} is not a legal key of this StricDict".format(repr(key)))
        dict.__setitem__(self, key, value)


class Field:
    def __get__(self, obj, type=None):
        return obj._data[self._name]

    def __set__(self, obj, value):
        obj._data[self._name] = value


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        for field_name, field in attrs.items():
            field._name = field_name
        attrs['_data'] = StrictDict.fromkeys(attrs.keys())
        return type(name, bases, attrs)


class Model:
    __metaclass__ = ModelMeta
    pass


class CharField(Field):
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(obj, self._name, str, value)

        super().__set__(obj, value)


class User(Model):
    name = CharField()
