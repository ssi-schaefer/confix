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

from . import dirsetup
from . import explicit_iface
from . import ignored_entries
from . import pseudo_handwritten
from . import common_iface_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(dirsetup.suite)
suite.addTest(explicit_iface.suite)
suite.addTest(ignored_entries.suite)
suite.addTest(pseudo_handwritten.suite)
suite.addTest(common_iface_suite.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass



