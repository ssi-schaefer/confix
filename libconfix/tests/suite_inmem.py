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

from libconfix.core.tests.suite_inmem import CoreInMemorySuite
from libconfix.plugins.tests.suite_inmem import PluginsInMemorySuite

import unittest

class LibConfixInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CoreInMemorySuite())
        self.addTest(PluginsInMemorySuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibConfixInMemorySuite())
    pass

