# Copyright (C) 2007 Joerg Faschingbauer

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

import relocated_header

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.testutils import find

import unittest

class RelocatedHeaderInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RelocatedHeaderInMemoryTest('test'))
        pass
    pass

class RelocatedHeaderInMemoryTest(unittest.TestCase):
    def test(self):
        package = LocalPackage(rootdirectory=relocated_header.make_package_source(package_name=self.__class__.__name__),
                               setups=[ExplicitDirectorySetup(),
                                       ExplicitCSetup()])
        package.boil(external_nodes=[])

        exe_builder = find.find_entrybuilder(
            rootbuilder=package.rootbuilder(),
            path=['exe'])
        lib_implementation_builder = find.find_entrybuilder(
            rootbuilder=package.rootbuilder(),
            path=['lib_implementation'])
        include_builder = find.find_entrybuilder(
            rootbuilder=package.rootbuilder(),
            path=['include'])
        self.failIf(exe_builder is None)
        self.failIf(lib_implementation_builder is None)
        self.failIf(include_builder is None)

        self.failUnless(lib_implementation_builder in package.digraph().successors(exe_builder))
        self.failUnless(include_builder in package.digraph().successors(lib_implementation_builder))

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(RelocatedHeaderInMemorySuite())
    pass
