# Copyright (C) 2009-2013 Joerg Faschingbauer

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

from . import cmakelists_inmem
from . import toplevel_boilerplate
from . import modules_inmem
from . import hierarchy_inmem
from . import intra_package_inmem
from . import inter_package_inmem
from . import iface_inmem
from . import dependency_order_check_inmem
from . import external_library_inmem
from . import buildinfo_inmem

import unittest

suite = unittest.TestSuite()
suite.addTest(cmakelists_inmem.suite)
suite.addTest(toplevel_boilerplate.suite)
suite.addTest(modules_inmem.suite)
suite.addTest(hierarchy_inmem.suite)
suite.addTest(intra_package_inmem.suite)
suite.addTest(inter_package_inmem.suite)
suite.addTest(iface_inmem.suite)
suite.addTest(dependency_order_check_inmem.suite)
suite.addTest(external_library_inmem.suite)
suite.addTest(buildinfo_inmem.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
