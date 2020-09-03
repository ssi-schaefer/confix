# Copyright (C) 2007-2013 Joerg Faschingbauer

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
from libconfix.setups.explicit_setup import ExplicitSetup

import unittest

class RelocatedHeaderInMemoryTest(unittest.TestCase):
    def test__basic(self):
        package = LocalPackage(rootdirectory=relocated_header.make_package_source(package_name=self.__class__.__name__),
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        exe_builder = package.rootbuilder().find_entry_builder(['exe'])
        lib_implementation_builder = package.rootbuilder().find_entry_builder(['lib_implementation'])
        include_builder = package.rootbuilder().find_entry_builder(['include'])
        self.failIf(exe_builder is None)
        self.failIf(lib_implementation_builder is None)
        self.failIf(include_builder is None)

        self.failUnless(lib_implementation_builder in package.digraph().successors(exe_builder))
        self.failUnless(include_builder in package.digraph().successors(lib_implementation_builder))

        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(RelocatedHeaderInMemoryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
