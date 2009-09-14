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

from libconfix.plugins.cmake.cmakelists import CMakeLists

import unittest

class CMakeListsInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CMakeListsInMemoryTest('link_directories'))
        self.addTest(CMakeListsInMemoryTest('target_link_libraries_tightened_after_set'))
        self.addTest(CMakeListsInMemoryTest('target_link_libraries_tightened_before_set'))
        pass
    pass

class CMakeListsInMemoryTest(unittest.TestCase):
    def link_directories(self):
        cmakelists = CMakeLists()
        cmakelists.link_directories(['1', '2'])
        cmakelists.link_directories(['3', '4'])
        self.failUnlessEqual(cmakelists.get_link_directories(), ['3', '4'])
        cmakelists.add_link_directories(['5', '6'])
        self.failUnlessEqual(cmakelists.get_link_directories(), ['3', '4', '5', '6'])
        pass
    
    def target_link_libraries_tightened_after_set(self):
        cmakelists = CMakeLists()
        cmakelists.target_link_libraries('target', ['a', 'b'])
        cmakelists.tighten_target_link_library(target='target', basename='a', tightened='tight_a')
        cmakelists.tighten_target_link_library(target='target', basename='b', tightened='tight_b')
        self.failUnlessEqual(cmakelists.get_target_link_libraries('target'),
                             ['tight_a', 'tight_b'])
        pass

    def target_link_libraries_tightened_before_set(self):
        cmakelists = CMakeLists()
        cmakelists.tighten_target_link_library(target='target', basename='a', tightened='tight_a')
        cmakelists.tighten_target_link_library(target='target', basename='b', tightened='tight_b')
        cmakelists.target_link_libraries('target', ['a', 'b'])
        self.failUnlessEqual(cmakelists.get_target_link_libraries('target'),
                             ['tight_a', 'tight_b'])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CMakeListsInMemorySuite())
    pass
