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

from . import dependencyset
from . import depinfo
from . import enlarge_force
from . import iface
from . import provide
from . import relate
from . import resolve
from . import urgency_error
from . import local_package

import unittest

suite = unittest.TestSuite()
suite.addTest(enlarge_force.suite)
suite.addTest(dependencyset.suite)
suite.addTest(depinfo.suite)
suite.addTest(iface.suite)
suite.addTest(provide.suite)
suite.addTest(relate.suite)
suite.addTest(resolve.suite)
suite.addTest(local_package.suite)
suite.addTest(urgency_error.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

