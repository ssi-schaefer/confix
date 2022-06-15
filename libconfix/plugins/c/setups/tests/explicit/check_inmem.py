# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from .check import CheckProgramBase

from libconfix.plugins.automake.out_automake import find_automake_output_builder

import unittest

class CheckProgramInMemory(CheckProgramBase):
    def __init__(self, methodName):
        CheckProgramBase.__init__(self, methodName)
        pass

    def use_libtool(self): return False

    def test(self):
        automake_output_builder = find_automake_output_builder(self.package_.rootbuilder())
        self.assertTrue(automake_output_builder)
        
        self.assertTrue('the-test-program' in automake_output_builder.makefile_am().check_programs())
        self.assertEqual(len(automake_output_builder.makefile_am().tests_environment()), 1)
        self.assertEqual(automake_output_builder.makefile_am().tests_environment()['name'], 'value')
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(CheckProgramInMemory)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

