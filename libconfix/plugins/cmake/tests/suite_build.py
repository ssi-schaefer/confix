# Copyright (C) 2009-2013 Joerg Faschingbauer

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

import intra_package_build
import local_install_build
import public_install_build
import inter_package_build
import library_dependencies_build
import readonly_prefixes_build
import external_library_build
import plainfile_build
import idl_build
import script_build
import repo_install_build
import generator_build
import cmake_bug_10082_build
import custom_command_build

import unittest

suite = unittest.TestSuite()
suite.addTest(intra_package_build.suite)
suite.addTest(local_install_build.suite)
suite.addTest(public_install_build.suite)
suite.addTest(inter_package_build.suite)
suite.addTest(library_dependencies_build.suite)
suite.addTest(readonly_prefixes_build.suite)
suite.addTest(external_library_build.suite)
suite.addTest(plainfile_build.suite)
suite.addTest(idl_build.suite)
suite.addTest(script_build.suite)
suite.addTest(repo_install_build.suite)
suite.addTest(generator_build.suite)
suite.addTest(cmake_bug_10082_build.suite)
suite.addTest(custom_command_build.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
