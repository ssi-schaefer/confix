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

from . import library_dependencies.suite_build as library_dependencies_build
from . import noinst_headers_build

import unittest

suite = unittest.TestSuite()
suite.addTest(library_dependencies_build.suite)
suite.addTest(noinst_headers_build.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
