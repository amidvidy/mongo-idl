# Base class for a mongo-idl code-gen backend. Design based on Thrift's t_generator
class CodeGenerator(object):
    
    def __init__(self, *args, *kwargs):
        pass
    
    # Actually does the generation
    def generate(self):
        pass

    # todo potentially remove
    def _generate_comment(self, comment_start, line_prefix, contents, comment_end):
        pass

    def _escape_string(self, s):
        pass

    # Subclasses can override this to do something at the start of generation
    def _init_generator(self):
        pass

    # Subclasses can override this to do something at the completion of generation
    def _close_generator(self):
        pass

    def _generate_constants(self, constants):
        pass

    def _generate_typedef(self, typedef):
        pass

    def _generate_enum(self, enum):
        pass

    def generate_const(self, const):
        pass

    def generate_struct(self, const):
        pass

    def generate_forward_decl(self, const):
        pass
    


