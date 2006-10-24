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
from libconfix.core.filesys.file import File
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.machinery.edgefinder import EdgeFinder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.require_symbol import Require_Symbol

from libconfix.testutils import dirhier
from libconfix.testutils import find
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestSetup

class ResolveTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicResolveTest())
        self.addTest(NotResolvedTest())
        self.addTest(CycleTest())
        pass

class BasicResolveTest(unittest.TestCase):
    def runTest(self): self.test()
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
    def runTest(self): self.test()
    def test(self):
        fs = dirhier.packageroot()
        file = fs.rootdirectory().add(name='x.iface',
                                      entry=File(lines=['REQUIRE_SYMBOL(symbol="unknown_symbol", urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[FileInterfaceTestSetup()])

        try:
            package.boil(external_nodes=[])
            pass
        except EdgeFinder.SuccessorNotFound, e:
            self.assert_(e.node() is package.rootbuilder())
            self.assert_(isinstance(e.errors()[0], EdgeFinder.RequireNotResolved))
            self.assert_(isinstance(e.errors()[0].require(), Require_Symbol))
            self.assert_(e.errors()[0].require().symbol() == 'unknown_symbol')
            return

        self.fail()
        pass
    
    pass

class CycleTest(unittest.TestCase):
    def runTest(self): self.test()
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
            package.boil(external_nodes=[])
        except CycleError:
            return
        self.fail()
        pass
    pass

if __name__ == '__main__':
    unittest.main()
    pass

