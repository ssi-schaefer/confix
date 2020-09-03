# Copyright (C) 2006-2013 Joerg Faschingbauer

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

import libconfix.plugins.c.tests.suite_inmem as c
import libconfix.plugins.plainfile.tests.suite_inmem as plainfile
import libconfix.plugins.idl.tests.suite_inmem as idl
import libconfix.plugins.automake.tests.suite_inmem as automake
import libconfix.plugins.cmake.tests.suite_inmem as cmake

import unittest

suite = unittest.TestSuite()
suite.addTest(c.suite)
suite.addTest(plainfile.suite)
suite.addTest(idl.suite)
suite.addTest(automake.suite)
suite.addTest(cmake.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass


