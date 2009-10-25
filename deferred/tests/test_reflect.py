# Copyright (c) 2001-2009 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Test cases for twisted.reflect module.
"""

import os

from deferred import _reflect, _util

from twisted.trial import unittest



class Breakable(object):

    breakRepr = False
    breakStr = False

    def __str__(self):
        if self.breakStr:
            raise RuntimeError("str!")
        else:
            return '<Breakable>'

    def __repr__(self):
        if self.breakRepr:
            raise RuntimeError("repr!")
        else:
            return 'Breakable()'



class BrokenType(Breakable, type):
    breakName = False

    def get___name__(self):
        if self.breakName:
            raise RuntimeError("no name")
        return 'BrokenType'
    __name__ = property(get___name__)



class BTBase(Breakable):
    __metaclass__ = BrokenType
    breakRepr = True
    breakStr = True



class NoClassAttr(Breakable):
    __class__ = property(lambda x: x.not_class)



class SafeRepr(unittest.TestCase):
    """
    Tests for L{_reflect.safe_repr} function.
    """

    def test_workingRepr(self):
        """
        L{_reflect.safe_repr} produces the same output as C{repr} on a working
        object.
        """
        x = [1, 2, 3]
        self.assertEquals(_reflect.safe_repr(x), repr(x))


    def test_brokenRepr(self):
        """
        L{_reflect.safe_repr} returns a string with class name, address, and
        traceback when the repr call failed.
        """
        b = Breakable()
        b.breakRepr = True
        bRepr = _reflect.safe_repr(b)
        self.assertIn("Breakable instance at 0x", bRepr)
        # Check that the file is in the repr, but without the extension as it
        # can be .py/.pyc
        self.assertIn(os.path.splitext(__file__)[0], bRepr)
        self.assertIn("RuntimeError: repr!", bRepr)


    def test_brokenStr(self):
        """
        L{_reflect.safe_repr} isn't affected by a broken C{__str__} method.
        """
        b = Breakable()
        b.breakStr = True
        self.assertEquals(_reflect.safe_repr(b), repr(b))


    def test_brokenClassRepr(self):
        class X(BTBase):
            breakRepr = True
        _reflect.safe_repr(X)
        _reflect.safe_repr(X())


    def test_unsignedID(self):
        """
        L{unsignedID} is used to print ID of the object in case of error, not
        standard ID value which can be negative.
        """
        class X(BTBase):
            breakRepr = True

        ids = {X: 100}
        def fakeID(obj):
            try:
                return ids[obj]
            except (TypeError, KeyError):
                return id(obj)
        self.addCleanup(_util.setIDFunction, _util.setIDFunction(fakeID))

        xRepr = _reflect.safe_repr(X)
        self.assertIn("0x64", xRepr)


    def test_brokenClassStr(self):
        class X(BTBase):
            breakStr = True
        _reflect.safe_repr(X)
        _reflect.safe_repr(X())


    def test_brokenClassAttribute(self):
        """
        If an object raises an exception when accessing its C{__class__}
        attribute, L{_reflect.safe_repr} uses C{type} to retrieve the class
        object.
        """
        b = NoClassAttr()
        b.breakRepr = True
        bRepr = _reflect.safe_repr(b)
        self.assertIn("NoClassAttr instance at 0x", bRepr)
        self.assertIn(os.path.splitext(__file__)[0], bRepr)
        self.assertIn("RuntimeError: repr!", bRepr)


    def test_brokenClassNameAttribute(self):
        """
        If a class raises an exception when accessing its C{__name__} attribute
        B{and} when calling its C{__str__} implementation, L{_reflect.safe_repr}
        returns 'BROKEN CLASS' instead of the class name.
        """
        class X(BTBase):
            breakName = True
        xRepr = _reflect.safe_repr(X())
        self.assertIn("<BROKEN CLASS AT 0x", xRepr)
        self.assertIn(os.path.splitext(__file__)[0], xRepr)
        self.assertIn("RuntimeError: repr!", xRepr)



class SafeStr(unittest.TestCase):
    """
    Tests for L{_reflect.safe_str} function.
    """

    def test_workingStr(self):
        x = [1, 2, 3]
        self.assertEquals(_reflect.safe_str(x), str(x))


    def test_brokenStr(self):
        b = Breakable()
        b.breakStr = True
        _reflect.safe_str(b)


    def test_brokenRepr(self):
        b = Breakable()
        b.breakRepr = True
        _reflect.safe_str(b)


    def test_brokenClassStr(self):
        class X(BTBase):
            breakStr = True
        _reflect.safe_str(X)
        _reflect.safe_str(X())


    def test_brokenClassRepr(self):
        class X(BTBase):
            breakRepr = True
        _reflect.safe_str(X)
        _reflect.safe_str(X())


    def test_brokenClassAttribute(self):
        """
        If an object raises an exception when accessing its C{__class__}
        attribute, L{_reflect.safe_str} uses C{type} to retrieve the class
        object.
        """
        b = NoClassAttr()
        b.breakStr = True
        bStr = _reflect.safe_str(b)
        self.assertIn("NoClassAttr instance at 0x", bStr)
        self.assertIn(os.path.splitext(__file__)[0], bStr)
        self.assertIn("RuntimeError: str!", bStr)


    def test_brokenClassNameAttribute(self):
        """
        If a class raises an exception when accessing its C{__name__} attribute
        B{and} when calling its C{__str__} implementation, L{_reflect.safe_str}
        returns 'BROKEN CLASS' instead of the class name.
        """
        class X(BTBase):
            breakName = True
        xStr = _reflect.safe_str(X())
        self.assertIn("<BROKEN CLASS AT 0x", xStr)
        self.assertIn(os.path.splitext(__file__)[0], xStr)
        self.assertIn("RuntimeError: str!", xStr)
