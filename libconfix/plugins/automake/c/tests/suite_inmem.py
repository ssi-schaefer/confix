# Copyright (C) 2008-2013 Joerg Faschingbauer

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

from . import external_library
from . import library_dependencies.suite_inmem
from . import library
from . import header_install_inmem

import unittest

suite = unittest.TestSuite()
suite.addTest(external_library.suite)
suite.addTest(library_dependencies.suite_inmem.suite)
suite.addTest(library.suite)
suite.addTest(header_install_inmem.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
