from __future__ import print_function

from idl.types import *
from idl.base import *

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

