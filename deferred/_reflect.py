__all__ = [
    'allYourBase',
    'qual',
    'safe_repr',
    'safe_str',
    ]

import traceback

from io import StringIO


from deferred._util import unsignedID


def allYourBase(classObj, baseClass=None):
    """allYourBase(classObj, baseClass=None) -> list of all base
    classes that are subclasses of baseClass, unless it is None,
    in which case all bases will be added.
    """
    l = []
    accumulateBases(classObj, l, baseClass)
    return l


def accumulateBases(classObj, l, baseClass=None):
    for base in classObj.__bases__:
        if baseClass is None or issubclass(base, baseClass):
            l.append(base)
        accumulateBases(base, l, baseClass)


def qual(clazz):
    """Return full import path of a class."""
    return clazz.__module__ + '.' + clazz.__name__


def _determineClass(x):
    try:
        return x.__class__
    except:
        return type(x)



def _determineClassName(x):
    c = _determineClass(x)
    try:
        return c.__name__
    except:
        try:
            return str(c)
        except:
            return '<BROKEN CLASS AT 0x%x>' % unsignedID(c)



def _safeFormat(formatter, o):
    """
    Helper function for L{safe_repr} and L{safe_str}.
    """
    try:
        return formatter(o)
    except:
        io = StringIO()
        traceback.print_exc(file=io)
        className = _determineClassName(o)
        tbValue = io.getvalue()
        return "<%s instance at 0x%x with %s error:\n %s>" % (
            className, unsignedID(o), formatter.__name__, tbValue)



def safe_repr(o):
    """
    safe_repr(anything) -> string

    Returns a string representation of an object, or a string containing a
    traceback, if that object's __repr__ raised an exception.
    """
    return _safeFormat(repr, o)



def safe_str(o):
    """
    safe_str(anything) -> string

    Returns a string representation of an object, or a string containing a
    traceback, if that object's __str__ raised an exception.
    """
    return _safeFormat(str, o)
