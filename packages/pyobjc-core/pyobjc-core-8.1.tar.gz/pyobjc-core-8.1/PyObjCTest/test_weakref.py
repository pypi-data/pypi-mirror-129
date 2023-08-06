import weakref

from PyObjCTest.fnd import NSArray, NSAutoreleasePool, NSObject
from PyObjCTools.TestSupport import TestCase, min_os_level
import objc
from . import corefoundation

CFUUIDRef = objc.registerCFSignature(
    "CFUUIDRef",
    corefoundation.OC_TestCoreFoundation.signatureForCFUUIDRef(),
    corefoundation.OC_TestCoreFoundation.typeidForCFUUIDRef(),
)


class OC_WeakrefTest1(NSObject):
    pass


class OC_WeakrefTest2(OC_WeakrefTest1):
    pass


class TestWeakrefs(TestCase):
    def testPureObjC(self):
        o = NSObject.new()
        self.assertRaises(TypeError, weakref.ref, o)

    def testFirstGenPython(self):
        o = OC_WeakrefTest1.new()
        self.assertRaises(TypeError, weakref.ref, o)

    def testSecondGenPython(self):
        o = OC_WeakrefTest2.new()
        self.assertRaises(TypeError, weakref.ref, o)


class TestObjCWeakRef(TestCase):
    @min_os_level("10.7")
    def test_weakref_to_cftype(self):
        o = corefoundation.OC_TestCoreFoundation.createUUID()

        with self.assertRaisesRegex(
            TypeError,
            "Expecting a Cocoa object, got instance of CoreFoundation type '.*'",
        ):
            objc.WeakRef(o)

    @min_os_level("10.7")
    def test_weakref_to_python(self):
        self.assertRaises(TypeError, objc.WeakRef, 1)
        self.assertRaises(TypeError, objc.WeakRef, "hello")
        self.assertRaises(TypeError, objc.WeakRef, b"hello")
        self.assertRaises(TypeError, objc.WeakRef, [])
        self.assertRaises(TypeError, objc.WeakRef, self)

    @min_os_level("10.7")
    def test_weakref_to_objc(self):

        pool = NSAutoreleasePool.alloc().init()

        o = NSObject.alloc().init()
        a = NSArray.arrayWithObject_(o)

        r = objc.WeakRef(o)
        self.assertIs(r(), o)

        del o
        del pool
        pool = NSAutoreleasePool.alloc().init()

        self.assertIsInstance(r(), NSObject)
        del a

        del pool
        self.assertIs(r(), None)

    @min_os_level("10.7")
    def test_weakref_call_interface(self):

        pool = NSAutoreleasePool.alloc().init()

        o = NSObject.alloc().init()
        a = NSArray.arrayWithObject_(o)

        r = objc.WeakRef(object=o)
        self.assertIs(r(), o)

        with self.assertRaises(TypeError):
            r(1)

        with self.assertRaises(TypeError):
            r(x=1)

        with self.assertRaises(TypeError):
            objc.WeakRef(value=o)

        with self.assertRaises(TypeError):
            objc.WeakRef(o, value=o)

        with self.assertRaises(TypeError):
            objc.WeakRef(o, o)

        del o
        del a
        del pool
        del r

    @min_os_level("10.7")
    def test_no_subclassing(self):
        with self.assertRaisesRegex(TypeError, ".*not an acceptable base type"):

            class MyRef(objc.WeakRef):
                pass
