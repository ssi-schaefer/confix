# Copyright (C) 2009-2010 Joerg Faschingbauer

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
        self.addTest(CMakeListsInMemoryTest('unique_find_call'))
        self.addTest(CMakeListsInMemoryTest('find_call_list'))
        self.addTest(CMakeListsInMemoryTest('collapse_multiple_include'))
        self.addTest(CMakeListsInMemoryTest('target_link_libraries_tightened_after_set'))
        self.addTest(CMakeListsInMemoryTest('target_link_libraries_tightened_before_set'))
        pass
    pass

class CMakeListsInMemoryTest(unittest.TestCase):
    def unique_find_call(self):
        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.add_find_call('xxx')
        cmakelists.add_find_call('xxx')
        self.failUnlessEqual(len(cmakelists.get_find_calls()), 1)

        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.add_find_call('xxx')
        cmakelists.add_find_call(['xxx'])
        self.failUnlessEqual(len(cmakelists.get_find_calls()), 1)
        pass

    def find_call_list(self):
        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.add_find_call(['0', '1'])
        self.failUnlessEqual(cmakelists.get_find_calls()[0], '0')
        self.failUnlessEqual(cmakelists.get_find_calls()[1], '1')
        pass
    
    def collapse_multiple_include(self):
        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.add_include('xxx')
        cmakelists.add_include('xxx')
        cmakelists.add_include('yyy')
        self.failUnlessEqual(len(cmakelists.get_includes()), 2)
        self.failUnlessEqual(cmakelists.get_includes()[0], 'xxx')
        self.failUnlessEqual(cmakelists.get_includes()[1], 'yyy')
        pass
    
    def target_link_libraries_tightened_after_set(self):
        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.target_link_libraries('target', ['a', 'b'])
        cmakelists.tighten_target_link_library(target='target', basename='a', tightened='tight_a')
        cmakelists.tighten_target_link_library(target='target', basename='b', tightened='tight_b')
        self.failUnlessEqual(cmakelists.get_target_link_libraries('target'),
                             ['tight_a', 'tight_b'])
        pass

    def target_link_libraries_tightened_before_set(self):
        cmakelists = CMakeLists(custom_command_helper=None)
        cmakelists.tighten_target_link_library(target='target', basename='a', tightened='tight_a')
        cmakelists.tighten_target_link_library(target='target', basename='b', tightened='tight_b')
        cmakelists.target_link_libraries('target', ['a', 'b'])
        self.failUnlessEqual(cmakelists.get_target_link_libraries('target'),
                             ['tight_a', 'tight_b'])
        pass

    def add_custom_command__output(self):
        # only asserting parameters here. I don't know how this will
        # evolve, and I'll likely change much as time passes.

        cmakelists = CMakeLists(custom_command_helper=None)

        # full set of parameters.
        cmakelists.add_custom_command__output(
            outputs=['output1', 'output2'],
            commands=[('command1', ['arg1.1', 'arg1.2']),
                      ('command2', ['arg2.1', 'arg2.2'])],
            depends=['depend1', 'depend2'],
            working_directory='working_directory')

        # working_directory is optional.
        cmakelists.add_custom_command__output(
            outputs=['output1', 'output2'],
            commands=[('command1', ['arg1.1', 'arg1.2']),
                      ('command2', ['arg2.1', 'arg2.2'])],
            depends=['depend1', 'depend2'])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CMakeListsInMemorySuite())
    pass
