from datetime import datetime

import pymysql
from PyMatcha import database_config

# Connect to the database
connection = pymysql.connect(**database_config)


class Field:
    """
    A holder for the value inside a model instance. Allows some restriction
    options and defaults to the data contained within.

    typeof     : Make sure data coming in can be of this type
    default    : Set this default value if nothing is supplied
    fmt        : Date format, only used with datetime types
    hidden     : Hide this field from API endpoints, will be skipped when dict(model) is called
    modifiable : If False will raise and exception if this field is modified
    """

    def __init__(self, typeof=str, default=None, fmt="%Y-%m-%d", hidden=False, modifiable=True):
        self.modifiable = modifiable
        self.type = typeof
        self.hidden = hidden
        self.value = default
        self.fmt = fmt

    def __repr__(self):
        """
        Display field name and value when using `print` on the field.
        """
        return "<{0}:{1}>".format(self.type.__name__, self.value)

    def deserialize(self):
        """
        Return value that is safe for SQL insert.
        """
        if self.type == datetime and self.value:
            return self.value.strftime(self.fmt)

        return self.value

    def serialize(self, value):
        """
        Serialise a database item into a python object
        """
        self.value = value
