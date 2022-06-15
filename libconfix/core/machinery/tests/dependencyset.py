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

from libconfix.core.machinery.dependency_utils import DependencySet
from libconfix.core.machinery.provide import Provide

import unittest

class DependencySetTest(unittest.TestCase):
    def test(self):
        a = Provide('a')
        b = Provide('b')
        c = Provide('c')
        
        s = DependencySet()
        s.add(a)
        s.add(b)
        s.add(c)

        found_a = found_b = found_c = None
        elements_of_s = [e for e in s]
        self.assertTrue(a in elements_of_s)
        self.assertTrue(b in elements_of_s)
        self.assertTrue(c in elements_of_s)
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DependencySetTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

