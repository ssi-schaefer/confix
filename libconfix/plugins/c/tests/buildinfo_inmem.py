# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.plugins.c.buildinfo import BuildInfo_CIncludePath_NativeLocal

from libconfix.core.machinery.buildinfo import BuildInformationSet

import unittest

class BuildInformationInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BuildInformationTest('test'))
        pass
    pass

class BuildInformationTest(unittest.TestCase):
    def test(self):
        set1 = BuildInformationSet()
        set1.add(BuildInfo_CIncludePath_NativeLocal(include_dir=['a','b']))
        set2 = BuildInformationSet()
        set2.add(BuildInfo_CIncludePath_NativeLocal(include_dir=['c','d']))
        set3 = BuildInformationSet()
        set3.add(BuildInfo_CIncludePath_NativeLocal(include_dir=None))

        set1.merge(set2)
        set1.merge(set3)

        bi1 = bi2 = bi3 = None
        for bi in set1:
            if bi.include_dir() == ['a','b']:
                bi1 = bi
            elif bi.include_dir() == ['c','d']:
                bi2 = bi
            elif bi.include_dir() is None:
                bi3 = bi
                pass
            pass
        self.failUnless(bi1)
        self.failUnless(bi2)
        self.failUnless(bi3)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BuildInformationInMemorySuite())
    pass
