import pymysql

from copy import deepcopy

from PyMatcha import database_config
from PyMatcha.utils.orm import Field

# Connect to the database
connection = pymysql.connect(**database_config)


class Model(object):
    """
    Base Model class, all other Models will inherit from this
    """

    db = connection

    # Every model should override this with the correct table name
    table_name = None

    def __init__(self, _data={}, **kwargs):
        """
        Create a new instance of Model class

        Can take a dictionary or keyword args to fill the internal fields

        eg:
            model = Model({"name" : "test"})
                or
            model = Model(name="test")

        Inheriting models should have class level attributes of class Field,
        this fills the self.fields attribute on an instance.

        All external calls to this class hang on the self.fields attr being
        populated.

        A call to self.get(username="test") can also fill the fields attr on
        an empty instance.
        """

        data = _data or kwargs
        self.fields = {}
        self.before_init(data)
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                self.fields[k] = deepcopy(v)
                if k in data.keys():
                    self.fields[k].serialize(data[k])

    def __getattribute__(self, name):
        """
        Override for __getattribute__ to allow dot accessor eg. model.username

        AttributeError will be thrown when a key is in the instance field attribute
        keys list. This will then call __getattr__(key) and allow the above mentioned
        dot operator
        """

        if name in ["__class__", "fields"]:
            return super(Model, self).__getattribute__(name)
        if name in self.fields:
            raise AttributeError
        return super(Model, self).__getattribute__(name)

    def __getattr__(self, key):
        """
        Override for __getattr__ will be called if __getattribute throws an AttributeError
        """

        if key in self.fields:
            return self.fields[key].value
        raise AttributeError("Field not present {}".format(key))

    def __getitem__(self, key):
        """
        Override dictionary style getters 'model["username"]' to always
        lookup the value in self.fields
        """

        if key in self.fields.keys():
            return self.fields[key].deserialize()
        else:
            return self.__dict__[key]

    def __setitem__(self, key, val):
        """
        Override dictionary style setters 'model["username"] = "test"'

        Calls self.__setattr__ for convenience.
        """

        self.__setattr__(key, val)

    def __setattr__(self, key, val):
        """
        Override for dot notation setters 'model.username = "test"'

        This method will edit the Field objects value contained in self.fields

        @Exception raised if the Field is not modifiable
        @AttributeError raised if key is not found
        """

        if key == "fields":
            super(Model, self).__setattr__(key, val)
        else:
            if key in self.fields:
                if self.fields[key].modifiable:
                    self.fields[key].value = val
                else:
                    raise Exception("Cannot modify field '{}'".format(key))
            else:
                raise AttributeError("Field {0} does not exist in Model {1}".format(key, self.__class__.__name__))

    def __repr__(self):
        """
        Display model name and id when printed
        """

        return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)

    def __len__(self):
        """
        Override length method will return the number of fields in this instance
        """

        return len(self.fields)

    def __iter__(self):
        """
        Allow this object to be typed into a dictionary using 'dict(model)'

        This is used when JSON encoding a model: 'See helpers/json_encoder.py'
        """

        for k, v in self.fields.items():
            if not v.hidden:
                yield k, v.value

    def before_init(self, data):
        """
        Hook to modify data before it is populated into 'self.fields'

        Useful to hash and set a password for a user.
        """

        pass

    def save(self):
        """
        Save this model to the database, REPLACE INTO is used to avoid having multiple
        database calls. Will insert if the row does not exist or update if it does.
        """
        columns = []
        values = []

        for name, field in self.fields.items():
            if name == "id" and not field.value:
                continue
            columns.append(name)
            try:
                values.append(field.deserialize())
            except TypeError:
                raise TypeError("Field {0} is not of type {1}".format(name, field.type.__name__))

        query = """
            REPLACE INTO users 
                ({0})
            VALUES
                ({1})
        """.format(
            ", ".join(columns), ", ".join(["%s"] * len(values))
        )

        with self.db.cursor() as c:
            c.execute(query, tuple(values))
            self.db.commit()

    def update(self, _dict={}, **kwargs):
        """
        Update fields on instance, using dictionary style setters will go through __setattr__
        which will update the fields in self.fields

        A model.save() will need to be done after updating to save to the database
        """
        data = _dict or kwargs

        if data:
            for k, v in data.items():
                self[k] = v
        else:
            raise Exception("Nothing to update")

    def delete(self):
        """
        Delete the record from the database, will only run when an 'id' is present.

        @Exception raised when an id is not present.
        """
        if self.id:
            with self.db.cursor() as c:
                c.execute(
                    """
                    DELETE FROM {0} WHERE id='{1}'
                """.format(
                        self.table_name, self.id
                    )
                )
                self.db.commit()
        else:
            raise Exception("User not in database")

    @classmethod
    def get(cls, **kwargs):
        """
        Get a model from the database, using a single keyword argument as a filter.

        Class method allows you to use without instanciation eg.

            model = Model.get(username="test")

        Returns a populated user instance on success and raises an error if the row count was 0

        """

        if len(kwargs) > 1:
            return False
        key = next(iter(kwargs))
        val = kwargs[key]

        temp = cls()
        with temp.db.cursor() as c:
            c.execute(
                """
                SELECT 
                    {fields}
                FROM 
                    {table} 
                WHERE   {cond}=%s""".format(
                    fields=", ".join(temp.fields.keys()), table=cls.table_name, cond=key
                ),
                (val,),
            )

            data = c.fetchone()
        if data:
            return cls(data)
        else:
            raise ValueError("{} not found in table {}".format(key, cls.table_name))

    @classmethod
    def select_all(cls):
        temp = cls()
        with temp.db.cursor() as c:
            c.execute("""SELECT * FROM {}""".format(cls.table_name))
            data = c.fetchall()
        for item in data:
            yield cls(item)
