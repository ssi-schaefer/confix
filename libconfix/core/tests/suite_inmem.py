# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.filesys.tests.inmem.suite import Suite as FileSystemSuite
from libconfix.core.digraph.tests.suite_inmem import DiGraphSuite
from libconfix.core.machinery.tests.suite_inmem import MachineryInMemorySuite
from libconfix.core.hierarchy.tests.suite_inmem import HierarchyInMemorySuite

import unittest

class CoreInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(FileSystemSuite())
        self.addTest(DiGraphSuite())
        self.addTest(MachineryInMemorySuite())
        self.addTest(HierarchyInMemorySuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CoreInMemorySuite())
    pass
