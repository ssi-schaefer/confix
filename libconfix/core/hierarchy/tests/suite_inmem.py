# Copyright (C) 2008 Joerg Faschingbauer

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

from dirsetup import BasicDirectorySetupSuite
from explicit_iface import ExplicitInterfaceInMemorySuite
from ignored_entries import IgnoredEntriesSuite
from pseudo_handwritten import PseudoHandwrittenSuite
from common_iface_suite import CommonDirectoryInterfaceSuite

import unittest

class HierarchyInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicDirectorySetupSuite())
        self.addTest(ExplicitInterfaceInMemorySuite())
        self.addTest(IgnoredEntriesSuite())
        self.addTest(PseudoHandwrittenSuite())
        self.addTest(CommonDirectoryInterfaceSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(HierarchyInMemorySuite())
    pass



