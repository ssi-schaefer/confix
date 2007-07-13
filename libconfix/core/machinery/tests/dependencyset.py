# Copyright (C) 2002-2006 Salomon Automation
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

import unittest

from libconfix.core.machinery.dependencyset import DependencySet
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.provide_string import Provide_String

class DependencySetSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(DependencySetTest('test'))
        pass
    pass

class DependencySetTest(unittest.TestCase):
    def test(self):
        a = Provide_String('a')
        b = Provide_String('b')
        c = Provide_String('c')
        
        s = DependencySet(klass=Provide, string_klass=Provide_String)
        s.add(a)
        s.add(b)
        s.add(c)

        found_a = found_b = found_c = None
        elements_of_s = [e for e in s]
        self.failUnless(a in elements_of_s)
        self.failUnless(b in elements_of_s)
        self.failUnless(c in elements_of_s)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(DependencySetSuite())
    pass

