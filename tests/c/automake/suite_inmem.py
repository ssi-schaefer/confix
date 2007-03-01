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

from c import CSuite
from library import LibrarySuite
from exe import ExecutableSuite
from libtool_version import LibtoolVersionSuite
from libtool_linking import LibtoolLinkingSuite
from intra_package_inmem import IntraPackageInMemorySuite
from check_inmem import CheckProgramInMemorySuite
from external_library import ExternalLibraryInMemorySuite
from library_dependencies.suite_inmem import LibraryDependenciesInMemorySuite
from exename.suite_inmem import ExecutableNameInMemorySuite
import readonly_prefixes.suite_inmem

import unittest

class AutomakeCSuiteInMemory(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CSuite())
        self.addTest(LibrarySuite())
        self.addTest(LibtoolVersionSuite())
        self.addTest(LibtoolLinkingSuite())
        self.addTest(ExecutableSuite())
        self.addTest(IntraPackageInMemorySuite())
        self.addTest(CheckProgramInMemorySuite())
        self.addTest(ExternalLibraryInMemorySuite())
        self.addTest(LibraryDependenciesInMemorySuite())
        self.addTest(ExecutableNameInMemorySuite())
        self.addTest(readonly_prefixes.suite_inmem.InMemorySuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeCSuiteInMemory())
    pass
