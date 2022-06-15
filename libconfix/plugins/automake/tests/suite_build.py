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

from . import simple_build
from . import kde_hack
from . import autoconf_archive
from . import exename.suite_build as exename
from . import readonly_prefixes.suite_build as readonly_prefixes
from . import interix_link
from . import inter_package_build
from . import intra_package_build
from . import check.suite_build as check_build
from . import relocated_headers.suite_build as relocated_headers_build
from . import explicit_package_build

import libconfix.plugins.automake.c.tests.suite_build as automake_c_build
import libconfix.plugins.automake.plainfile.tests.suite_build as plainfile_build
from . import idl_build
import libconfix.plugins.automake.script.tests.suite_build as script_build

import unittest

suite = unittest.TestSuite()
suite.addTest(simple_build.suite)
suite.addTest(kde_hack.suite)
suite.addTest(autoconf_archive.suite)
suite.addTest(exename.suite)
suite.addTest(readonly_prefixes.suite)
suite.addTest(interix_link.suite)
suite.addTest(automake_c_build.suite)
suite.addTest(inter_package_build.suite)
suite.addTest(intra_package_build.suite)
suite.addTest(check_build.suite)
suite.addTest(relocated_headers_build.suite)
suite.addTest(explicit_package_build.suite)
suite.addTest(plainfile_build.suite)
suite.addTest(idl_build.suite)
suite.addTest(script_build.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
