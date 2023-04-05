import math
import copy

# ----------------------------------------------------------------------
# Functions implementing the prototype-based system.
#
# I think it's easier to keep track of relationships between different objects using classes
#
# ----------------------------------------------------------------------

def clone(obj):
    """Clone an existing object to create a new one."""
    new_obj = copy.deepcopy(obj)
    new_obj['_parent'] = obj
    return new_obj
    
def find(obj, method_name):
    """Find a method."""
    if obj is None:
        raise NotImplementedError("method_name")
    if method_name in obj: 
        return cls[method_name]
    return find(obj["_parent"], method_name)

def call(obj, method_name, *args):
    """Call a method."""
    method = find(obj, method_name)
    return method(obj, *args)

