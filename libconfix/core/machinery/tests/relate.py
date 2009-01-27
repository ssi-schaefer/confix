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

from libconfix.core.filesys.file import File
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.testutils import dirhier
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestSetup

import unittest

class RelateTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RelateBasic('test'))
        self.addTest(InternalRequires('test'))
        pass
    pass

class RelateBasic(unittest.TestCase):

    """ See if we are calculating dependencies correctly. """
    
    def test(self):
        fs = dirhier.packageroot()

        lodir = dirhier.subdir(fs.rootdirectory(), 'lo')
        lofile = lodir.add(
            name='lo.iface',
            entry=File(lines=['PROVIDE_SYMBOL(symbol="lo")']))
        
        hidir = dirhier.subdir(fs.rootdirectory(), 'hi')
        hifile = hidir.add(
            name='hi.iface',
            entry=File(lines=['REQUIRE_SYMBOL(symbol="lo", urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ImplicitDirectorySetup(),
                                       FileInterfaceTestSetup()])
        package.boil(external_nodes=[])

        lodirbuilder = package.rootbuilder().find_entry_builder(['lo'])
        self.failIf(lodirbuilder is None)
        hidirbuilder = package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidirbuilder is None)
        lofilebuilder = package.rootbuilder().find_entry_builder(['lo', 'lo.iface'])
        self.failIf(lofilebuilder is None)
        hifilebuilder = package.rootbuilder().find_entry_builder(['hi', 'hi.iface'])
        self.failIf(hifilebuilder is None)

        self.failIf(lofilebuilder.successors() is None)
        self.failUnlessEqual(len(lofilebuilder.successors()), 0)
        self.failUnlessEqual(len(hifilebuilder.successors()), 1)
        self.failUnless(lodirbuilder in hifilebuilder.successors())
        self.failUnless(lofilebuilder.node() is lodirbuilder)
        self.failUnless(hifilebuilder.node() is hidirbuilder)
        self.failUnlessEqual(lofilebuilder.relate_calls(), 1)
        self.failUnlessEqual(hifilebuilder.relate_calls(), 1)
        
        pass
    pass

class InternalRequires(unittest.TestCase):

    """ Require objects of one node that are resolved by the same node
    must not molest the dependency calculation."""
    
    def test(self):
        fs = dirhier.packageroot()
        providing_file = fs.rootdirectory().add(
            name='providing_file.iface',
            entry=File(lines=['PROVIDE_SYMBOL(symbol="the_symbol_which_it_is_all_about")']))
        requiring_file = fs.rootdirectory().add(
            name='requiring_file.iface',
            entry=File(lines=['REQUIRE_SYMBOL(symbol="the_symbol_which_it_is_all_about",',
                              '               urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ImplicitDirectorySetup(),
                                       FileInterfaceTestSetup()])
        package.boil(external_nodes=[])

        self.failUnlessEqual(len(package.rootbuilder().requires()), 0)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(RelateTestSuite())
    pass

