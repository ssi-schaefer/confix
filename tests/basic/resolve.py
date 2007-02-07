# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import unittest

from libconfix.core.digraph.cycle import CycleError
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.machinery.edgefinder import EdgeFinder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.require_symbol import Require_Symbol
from libconfix.core.machinery.provide_symbol import Provide_Symbol
from libconfix.core.machinery.resolve_error import NotResolved, AmbiguouslyResolved
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

from libconfix.testutils import dirhier
from libconfix.testutils import find
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestSetup

class ResolveTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicResolveTest('test'))
        self.addTest(NotResolvedTest('test'))
        self.addTest(AmbiguousResolveTest('test'))
        self.addTest(CycleTest('test'))
        pass

class BasicResolveTest(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()

        lodir = dirhier.subdir(fs.rootdirectory(), 'lo')
        lofile = lodir.add(name='lo.iface',
                           entry=File(lines=['PROVIDE_SYMBOL(symbol="lo")']))
        
        hidir = dirhier.subdir(fs.rootdirectory(), 'hi')
        hifile = hidir.add(name='hi.iface',
                           entry=File(lines=['REQUIRE_SYMBOL(symbol="lo", urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       FileInterfaceTestSetup()])
        package.boil(external_nodes=[])

        lodirbuilder = find.find_entrybuilder(package.rootbuilder(), ['lo'])
        hidirbuilder = find.find_entrybuilder(package.rootbuilder(), ['hi'])

        self.assertEqual(len(package.digraph().nodes()), 3 \
                         # plus 1 for confix-admin which is a full-fledged node
                         +1)
        rootnode = None
        lonode = None
        hinode = None
        for n in package.digraph().nodes():
            if n is package.rootbuilder():
                rootnode = n
                continue
            if n is lodirbuilder:
                lonode = n
                continue
            if n is hidirbuilder:
                hinode = n
                continue
            pass

        self.assertEqual(len(package.digraph().successors(hinode)), 1)
        self.assertEqual(len(package.digraph().successors(lonode)), 0)
        self.assert_(lonode in package.digraph().successors(hinode))
            
        pass
    
    pass

class NotResolvedTest(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        file = fs.rootdirectory().add(name='x.iface',
                                      entry=File(lines=['REQUIRE_SYMBOL(symbol="unknown_symbol", urgency=URGENCY_ERROR)']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[FileInterfaceTestSetup()])
        self.failUnlessRaises(NotResolved, package.boil, external_nodes=[])
        pass
    
    pass

class AmbiguousResolveTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo1 = fs.rootdirectory().add(
            name='lo1',
            entry=Directory())
        lo2 = fs.rootdirectory().add(
            name='lo2',
            entry=Directory())
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])

        lo1_builder = DirectoryBuilder(directory=lo1)
        lo1_builder.add_provide(Provide_Symbol(symbol='the_ambiguous_symbol'))
        package.rootbuilder().add_builder(lo1_builder)

        lo2_builder = DirectoryBuilder(directory=lo2)
        lo2_builder.add_provide(Provide_Symbol(symbol='the_ambiguous_symbol'))
        package.rootbuilder().add_builder(lo2_builder)

        hi_builder = DirectoryBuilder(directory=hi)
        hi_builder.add_require(Require_Symbol(symbol='the_ambiguous_symbol', found_in=[]))
        package.rootbuilder().add_builder(hi_builder)

        self.failUnlessRaises(Error, package.boil, external_nodes=[])
        pass
    pass

class CycleTest(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()

        dirA = dirhier.subdir(fs.rootdirectory(), 'A')
        fileA = dirA.add(name='A.iface',
                         entry=File(lines=['PROVIDE_SYMBOL(symbol="A")',
                                           'REQUIRE_SYMBOL(symbol="B")']))
        
        dirB = dirhier.subdir(fs.rootdirectory(), 'B')
        fileB = dirB.add(name='B.iface',
                         entry=File(lines=['PROVIDE_SYMBOL(symbol="B")',
                                           'REQUIRE_SYMBOL(symbol="A")']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       FileInterfaceTestSetup()])
        try:
            print 'boil'
            package.boil(external_nodes=[])
            print 'done'
        except CycleError:
            return
        self.fail()
        pass
    pass


if __name__ == '__main__':
    unittest.TextTestRunner().run(ResolveTestSuite())
    pass

