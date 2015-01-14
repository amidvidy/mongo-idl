from __future__ import print_function

import six
import os
import mako

from mako.template import Template

"""
Structs that have been defined are stored here
"""
env = {}

"""
Returns the fields from a struct object
"""
def get_field_names(cls):
    return (attr for attr in dir(cls) if not attr.startswith('_'))

"""
This will generate code for all the structs that we have defined.
"""
def gen():
    for cls in env.values():
        print(cls._generate())

"""
Base exception for all mongo-idl exceptions
"""
class IdlError(Exception):
    pass

"""
Dummy init method so that people don't instantiate struct classes.
"""
def raise_error_on_init(cls, *args, **kwargs):
    raise IdlError("Cannot create instances of an idl definition.")

"""
The metaclass for all Structs.
inspired by the Django ORM internals
"""
class MetaStruct(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(MetaStruct, cls).__new__
        if attrs.get('__abstract__', False):
            return super_new(cls, name, bases, attrs)

        # Don't let users actually create instances of Structs
        attrs['__init__'] = raise_error_on_init

        # Construct the struct
        struct_cls = super_new(cls, name, bases, attrs)
        
        # Add to environment
        env[name] = struct_cls

        return struct_cls

        
"""
Base class for all Structs. Users inherit from this
to define their own message types.
"""
class Struct(six.with_metaclass(MetaStruct)):
    __abstract__ = True

    @classmethod
    def _generate(cls, *args, **kwargs):
        fields = []
        
        for field_name in get_field_names(cls):
            field = getattr(cls, field_name)
            field._name = field_name # todo, do this automagically w/ metaclass  
            fields.append(field)

        try:
            # TODO only load template once
            return Template(filename=os.path.join(os.path.dirname(__file__),'tpl', 'message.tpl')).render(
                struct_name=cls.__name__,
                fields=fields,
            )
        except:
            return (mako.exceptions.text_error_template().render())


class Field(object):
    def __init__(self, *args, **kwargs):
        pass

    def header(self):
        if hasattr(self, '_header'):
            return "#include {}".format(self._header)
        return None

    def decl(self):
        return "{type} _{name};".format(
            name=self._name, 
            type=self._type)

    def getter(self):
        fmt = None
        if self._primitive:
            fmt = "{type} get{cname}() {{ return _{name};}}"
        else:
            fmt = "const {type}& get{cname}() {{ return _{name}; }}"
        return fmt.format(
            name=self._name,
            cname=self._name.capitalize(),
            type=self._type
        )

    def setter(self):
        fmt = None
        if self._primitive:
            fmt = "void set{cname}({type} {name}) {{ _{name} = {name}; }}"
        else:
            fmt = "void set{cname}(const {type}& {name}) {{ _{name} = {name}; }}"
        return fmt.format(
            name=self._name,
            cname=self._name.capitalize(),
            type=self._type
        )


## TODO, autogenerate these classes from a map of types->headers

class String(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'std::string'
        self._header = '<string>' # TODO auto add headers
        self._primitive = False
        super(String, self).__init__(self, *args, **kwargs)
    

class Document(Field):
    def __init__(self, *args, **kwargs):
        self.fields = kwargs
        super(Document, self).__init__(self, *args, **kwargs)


class Long(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'long'
        self._primitive = True
        super(Long, self).__init__(self, *args, **kwargs)


class Array(Field):
    def __init__(self, *args, **kwargs):
        pass


class Bool(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'bool'
        self._primitive = True
        super(Bool, self).__init__(self, *args, **kwargs)
