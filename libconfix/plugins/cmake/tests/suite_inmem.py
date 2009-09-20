# Copyright (C) 2009 Joerg Faschingbauer

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

from cmakelists_inmem import CMakeListsInMemorySuite
from toplevel_boilerplate import ToplevelBoilerplateInMemorySuite
from modules_inmem import ModulesInMemorySuite
from hierarchy_inmem import HierarchyInMemorySuite
from intra_package_inmem import IntraPackageInMemorySuite
from inter_package_inmem import InterPackageInMemorySuite
from iface_inmem import InterfaceInMemorySuite
from dependency_order_check_inmem import DependencyOrderInMemorySuite
from external_library_inmem import ExternalLibraryInMemorySuite
from buildinfo_inmem import BuildInformationInMemorySuite

import unittest

class CMakeInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CMakeListsInMemorySuite())
        self.addTest(ToplevelBoilerplateInMemorySuite())
        self.addTest(ModulesInMemorySuite())
        self.addTest(HierarchyInMemorySuite())
        self.addTest(IntraPackageInMemorySuite())
        self.addTest(InterPackageInMemorySuite())
        self.addTest(InterfaceInMemorySuite())
        self.addTest(DependencyOrderInMemorySuite())
        self.addTest(ExternalLibraryInMemorySuite())
        self.addTest(BuildInformationInMemorySuite())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CMakeInMemorySuite())
    pass
