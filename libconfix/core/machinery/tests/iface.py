# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.provide import Provide_Symbol
from libconfix.core.machinery.require import Require
from libconfix.core.machinery.require import Require_Symbol
from libconfix.core.machinery.setup import NullSetup
from libconfix.core.utils import const

from libconfix.testutils import dirhier
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestBuilder

import unittest

class BuilderInterfaceTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BuilderInterface('testFilePropertyOK'))
        self.addTest(BuilderInterface('testRequires'))
        self.addTest(BuilderInterface('testProvides'))
        pass

class BuilderInterface(unittest.TestCase):
    def testFilePropertyOK(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=["SET_FILE_PROPERTY(name='XXX', value=666)",
                              "SET_FILE_PROPERTIES({'YYY': 777})"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[NullSetup()])
        package.rootbuilder().add_builder(FileInterfaceTestBuilder(file=file))

        self.assertNotEqual(file.get_property(name='XXX'), None)
        self.assertEqual(file.get_property(name='XXX'), 666)
        self.assertNotEqual(file.get_property(name='YYY'), None)
        self.assertEqual(file.get_property(name='YYY'), 777)
        pass
    
    def testRequires(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=["from libconfix.core.machinery.require import Require_Symbol",
                              "REQUIRE_SYMBOL(symbol='sym1')",
                              "REQUIRE_SYMBOL(symbol='sym2', urgency=URGENCY_IGNORE)",
                              "REQUIRE_SYMBOL(symbol='sym3', urgency=URGENCY_WARN)",
                              "REQUIRE_SYMBOL(symbol='sym4', urgency=URGENCY_ERROR)",
                              "REQUIRE(Require_Symbol(symbol='sym5',",
                              "                       found_in=['xxx'], ",
                              "                       urgency=URGENCY_ERROR))"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[NullSetup()])
        builder = FileInterfaceTestBuilder(file=file)
        builder.initialize(package=package)
        self.assertEqual(len(builder.dependency_info().requires()), 5)
        sym1 = None
        sym2 = None
        sym3 = None
        sym4 = None
        sym5 = None
        for r in builder.dependency_info().requires():
            self.assert_(isinstance(r, Require_Symbol))
            if r.symbol() == 'sym1':
                sym1 = r
                continue
            if r.symbol() == 'sym2':
                sym2 = r
                continue
            if r.symbol() == 'sym3':
                sym3 = r
                continue
            if r.symbol() == 'sym4':
                sym4 = r
                continue
            if r.symbol() == 'sym5':
                sym5 = r
                continue
            pass
        self.assertNotEqual(sym1, None)
        self.assertNotEqual(sym2, None)
        self.assertNotEqual(sym3, None)
        self.assertNotEqual(sym4, None)
        self.assertNotEqual(sym5, None)
        self.assertEqual(sym1.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(sym2.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(sym3.urgency(), Require.URGENCY_WARN)
        self.assertEqual(sym4.urgency(), Require.URGENCY_ERROR)
        self.assertEqual(sym5.urgency(), Require.URGENCY_ERROR)
        pass

    def testProvides(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=['from libconfix.core.machinery.provide import Provide_Symbol',
                              "PROVIDE_SYMBOL(symbol='sym1')",
                              "PROVIDE_SYMBOL(symbol='sym2', match=EXACT_MATCH)",
                              "PROVIDE_SYMBOL(symbol='sym3', match=PREFIX_MATCH)",
                              "PROVIDE_SYMBOL(symbol='sym4', match=GLOB_MATCH)",
                              "PROVIDE(Provide_Symbol(symbol='sym5'))"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[NullSetup()])
        builder = FileInterfaceTestBuilder(file=file)
        package.rootbuilder().add_builder(builder)
        self.assertEqual(len(builder.dependency_info().provides()), 5)
        sym1 = None
        sym2 = None
        sym3 = None
        sym4 = None
        sym5 = None
        for p in builder.dependency_info().provides():
            self.assert_(isinstance(p, Provide_Symbol))
            if p.symbol() == 'sym1':
                sym1 = p
                continue
            if p.symbol() == 'sym2':
                sym2 = p
                continue
            if p.symbol() == 'sym3':
                sym3 = p
                continue
            if p.symbol() == 'sym4':
                sym4 = p
                continue
            if p.symbol() == 'sym5':
                sym5 = p
                continue
            pass
        self.assertNotEqual(sym1, None)
        self.assertNotEqual(sym2, None)
        self.assertNotEqual(sym3, None)
        self.assertNotEqual(sym4, None)
        self.assertNotEqual(sym5, None)
        self.assertEqual(sym1.match(), Provide.EXACT_MATCH)
        self.assertEqual(sym2.match(), Provide.EXACT_MATCH)
        self.assertEqual(sym3.match(), Provide.PREFIX_MATCH)
        self.assertEqual(sym4.match(), Provide.GLOB_MATCH)
        self.assertEqual(sym5.match(), Provide.EXACT_MATCH)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BuilderInterfaceTestSuite())
    pass
