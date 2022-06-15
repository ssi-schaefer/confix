# Copyright (C) 2002-2006 Salomon Automation
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

from libconfix.core.machinery.dependency_utils import DependencyInformation
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.require import Require

import unittest

class DependencyInformationEqual(unittest.TestCase):
    def test(self):
        d1 = DependencyInformation()
        d2 = DependencyInformation()
        self.assertTrue(d1.is_equal(d2))
        
        d1 = DependencyInformation()
        d1.add_provide(Provide('a'))
        d1.add_provide(Provide('b'))
        d2 = DependencyInformation()
        d2.add_provide(Provide('a'))
        d2.add_provide(Provide('b'))
        self.assertTrue(d1.is_equal(d2))
        self.assertTrue(d2.is_equal(d1))

        d1 = DependencyInformation()
        d1.add_provide(Provide('a'))
        d2 = DependencyInformation()
        self.assertFalse(d1.is_equal(d2))
        self.assertFalse(d2.is_equal(d1))

        d1 = DependencyInformation()
        d1.add_provide(Provide('a'))
        d2 = DependencyInformation()
        d2.add_provide(Provide('b'))
        self.assertFalse(d1.is_equal(d2))
        self.assertFalse(d2.is_equal(d1))

        d1 = DependencyInformation()
        d1.add_provide(Provide('a'))
        d2 = DependencyInformation()
        d2.add_provide(Provide('a', Provide.GLOB_MATCH))
        self.assertFalse(d1.is_equal(d2))
        self.assertFalse(d2.is_equal(d1))
        
        d1 = DependencyInformation()
        d1.add_provide(Provide('a', Provide.GLOB_MATCH))
        d2 = DependencyInformation()
        d2.add_provide(Provide('a', Provide.GLOB_MATCH))
        self.assertTrue(d1.is_equal(d2))
        self.assertTrue(d2.is_equal(d1))

        d1 = DependencyInformation()
        d1.add_provide(Provide('a'))
        d1.add_require(Require(string='a', found_in=[]))
        d2 = DependencyInformation()
        d2.add_provide(Provide('a'))
        self.assertFalse(d1.is_equal(d2))
        self.assertFalse(d2.is_equal(d1))
        
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DependencyInformationEqual))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

