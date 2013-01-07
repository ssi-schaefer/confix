# Copyright (C) 2006-2013 Joerg Faschingbauer

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
import clusterer.suite_inmem
import ignored_entries
import library_versions
import inter_package_inmem
import buildinfo_inmem

import libconfix.plugins.c.setups.tests.suite_inmem
import libconfix.plugins.c.relocated_headers.tests.suite_inmem

import unittest

suite = unittest.TestSuite()
suite.addTest(provide_require.suite)
suite.addTest(requires.suite)
suite.addTest(relate.suite)
suite.addTest(library.suite)
suite.addTest(libconfix.plugins.c.setups.tests.suite_inmem.suite)
suite.addTest(libconfix.plugins.c.relocated_headers.tests.suite_inmem.suite)
suite.addTest(header_visibility_inmem.suite)
suite.addTest(regressions.suite_inmem.suite)
suite.addTest(confix2_dir.suite)
suite.addTest(misc.suite)
suite.addTest(setup_cxx.suite)
suite.addTest(setup_exe.suite)
suite.addTest(setup_lexyacc.suite)
suite.addTest(setup_library.suite)
suite.addTest(clusterer.suite_inmem.suite)
suite.addTest(ignored_entries.suite)
suite.addTest(library_versions.suite)
suite.addTest(inter_package_inmem.suite)
suite.addTest(buildinfo_inmem.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
