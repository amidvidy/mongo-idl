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
            type=self._type
        )

    def getter(self):
        fmt = None
        if self._primitive:
            fmt = "{type} get{cname}() {{ return _{name}; }}"
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

    def serialize(self):
        pass

    def deserialize(self):
        pass

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
