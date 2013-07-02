__all__ = [
    'mergeFunctionMetadata',
    'setIDFunction',
    'unsignedID',
    ]

import inspect
import sys


_idFunction = id


def setIDFunction(idFunction):
    """
    Change the function used by L{unsignedID} to determine the integer id value
    of an object.  This is largely useful for testing to give L{unsignedID}
    deterministic, easily-controlled behavior.

    @param idFunction: A function with the signature of L{id}.
    @return: The previous function being used by L{unsignedID}.
    """
    global _idFunction
    oldIDFunction = _idFunction
    _idFunction = idFunction
    return oldIDFunction


_HUGEINT = (sys.maxsize + 1) * 2


# Copied from twisted.python.util.unsignedID
def unsignedID(obj):
    """
    Return the id of an object as an unsigned number so that its hex
    representation makes sense
    """
    rval = _idFunction(obj)
    if rval < 0:
        rval += _HUGEINT
    return rval


# Copied from twisted.python.util.mergeFunctionMetadata.
def mergeFunctionMetadata(f, g):
    """
    Overwrite C{g}'s name and docstring with values from C{f}.  Update
    C{g}'s instance dictionary with C{f}'s.

    To use this function safely you must use the return value. In Python 2.3,
    L{mergeFunctionMetadata} will create a new function. In later versions of
    Python, C{g} will be mutated and returned.

    @return: A function that has C{g}'s behavior and metadata merged from
        C{f}.
    """
    try:
        g.__name__ = f.__name__
    except TypeError:
        try:
            merged = types.FunctionType(
                g.__code__, g.__globals__,
                f.__name__, inspect.getargspec(g)[-1],
                g.__closure__)
        except TypeError:
            pass
    else:
        merged = g
    try:
        merged.__doc__ = f.__doc__
    except (TypeError, AttributeError):
        pass
    try:
        merged.__dict__.update(g.__dict__)
        merged.__dict__.update(f.__dict__)
    except (TypeError, AttributeError):
        pass
    merged.__module__ = f.__module__
    return merged
