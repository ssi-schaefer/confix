# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from dependencyset import DependencySetSuite
from depinfo import DependencyInformationSuite
from enlarge_force import EnlargeForceSuite
from iface import BuilderInterfaceTestSuite
from provide import ProvideSuite
from relate import RelateTestSuite
from resolve import ResolveTestSuite
from urgency_error import UrgencyErrorSuite
from local_package import LocalPackageSuite

import unittest

class MachineryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(EnlargeForceSuite())
        self.addTest(DependencySetSuite())
        self.addTest(DependencyInformationSuite())
        self.addTest(BuilderInterfaceTestSuite())
        self.addTest(ProvideSuite())
        self.addTest(RelateTestSuite())
        self.addTest(ResolveTestSuite())
        self.addTest(LocalPackageSuite())
        self.addTest(UrgencyErrorSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MachineryInMemorySuite())
    pass

