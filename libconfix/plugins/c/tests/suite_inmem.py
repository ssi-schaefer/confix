# Copyright (C) 2006-2012 Joerg Faschingbauer

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

import provide_require
import requires
import relate
import library
import regressions.suite_inmem
import header_visibility_inmem
import confix2_dir
import misc
import setup_cxx
import setup_exe
import setup_lexyacc
import setup_library
from clusterer.suite_inmem import ClustererInMemorySuite
import ignored_entries
import library_versions
import inter_package_inmem
import buildinfo_inmem

from libconfix.plugins.c.setups.tests.suite_inmem import SetupsInMemorySuite
from libconfix.plugins.c.relocated_headers.tests.suite_inmem import RelocatedHeadersInMemorySuite

import unittest

class CInMemoryTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(provide_require.suite)
        self.addTest(requires.suite)
        self.addTest(relate.suite)
        self.addTest(library.suite)
        self.addTest(SetupsInMemorySuite())
        self.addTest(RelocatedHeadersInMemorySuite())
        self.addTest(header_visibility_inmem.suite)
        self.addTest(regressions.suite_inmem.suite)
        self.addTest(confix2_dir.suite)
        self.addTest(misc.suite)
        self.addTest(setup_cxx.suite)
        self.addTest(setup_exe.suite)
        self.addTest(setup_lexyacc.suite)
        self.addTest(setup_library.suite)
        self.addTest(ClustererInMemorySuite())
        self.addTest(ignored_entries.suite)
        self.addTest(library_versions.suite)
        self.addTest(inter_package_inmem.suite)
        self.addTest(buildinfo_inmem.suite)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CInMemoryTestSuite())
    pass
