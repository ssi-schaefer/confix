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

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake import commands

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import os
import subprocess
import unittest

class ExternalLibraryBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExternalLibraryTest('test'))
        pass
    pass

class ExternalLibraryTest(PersistentTestCase):
    def setUp(self):
        super(ExternalLibraryTest, self).setUp()
        
        self.__fs = FileSystem(path=self.rootpath())

        source = self.__fs.rootdirectory().add(
            name='source',
            entry=Directory())

        build = self.__fs.rootdirectory().add(
            name='build',
            entry=Directory())
        build.add(
            name='external-library',
            entry=Directory())
        build.add(
            name='user-of-external-library',
            entry=Directory())

        self.__fs.rootdirectory().add(
            name='install',
            entry=Directory())

        # installed into install/external-library
        if True:
            external_library_root = source.add(
                name='external-library',
                entry = Directory())
            external_library_root.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('ExternalLibrary')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            external_library_root.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["LIBRARY(basename='my-external-library',",
                                  "        members=[H(filename='my-external-library.h'),",
                                  "                 C(filename='my-external-library.c')])"
                                  ]))
            external_library_root.add(
                name='my-external-library.h',
                entry=File(lines=['#ifndef MY_EXTERNAL_LIBRARY_H',
                                  '#define MY_EXTERNAL_LIBRARY_H',
                                  '#ifndef PROPAGATED_CMDLINE_MACRO',
                                  '#  define PROPAGATED_CMDLINE_MACRO "fallback"',
                                  '#endif',
                                  'static inline const char* my_external_library_inline_string() {',
                                  '    return PROPAGATED_CMDLINE_MACRO;',
                                  '}',
                                  'extern const char* my_external_library_linked_string();',
                                  '#endif']))
            external_library_root.add(
                name='my-external-library.c',
                entry=File(lines=['#include "my-external-library.h"',
                                  'const char* my_external_library_linked_string() {',
                                  '    return "my-external-library-linked-string";',
                                  '}']))
            pass

        if True:
            user_of_external_library_root = source.add(
                name='user-of-external-library',
                entry=Directory())
            user_of_external_library_root.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('UserOfExternalLibrary')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            user_of_external_library_root.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["DIRECTORY(['confix-code'])",
                                  "DIRECTORY(['lib'])",
                                  "DIRECTORY(['bin'])"]))

            confix_source = user_of_external_library_root.add(
                name='confix-code',
                entry=Directory())

            module_content = """
            MACRO(FindMyExternalLibrary)
            SET(my_external_library_libpath %(lib)s)
            SET(my_external_library_includepath %(inc)s)
            ENDMACRO(FindMyExternalLibrary)""" % \
            {'lib': '/'.join(self.rootpath()+['install', 'lib']),
             'inc': '/'.join(self.rootpath()+['install', 'include'])}

            confix_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["PROVIDE_SYMBOL('my-external-library')",
                                  "CMAKE_ADD_CONFIX_MODULE(",
                                  "    name='FindMyExternalLibrary.cmake',",
                                  "    lines=['''"+module_content+"'''])",
                                  "CMAKE_CMAKELISTS_ADD_INCLUDE_CONFIX_MODULE('FindMyExternalLibrary.cmake')",
                                  "CMAKE_CMAKELISTS_ADD_FIND_CALL('FindMyExternalLibrary()')",
                                  "CMAKE_EXTERNAL_LIBRARY(",
                                  "    incpath=['${my_external_library_includepath}'],",
                                  "    libpath=['${my_external_library_libpath}'],",
                                  "    libs=['my-external-library'],",
                                  "    cmdlinemacros={'PROPAGATED_CMDLINE_MACRO': '\"my-propagated-cmdline-macro\"'})",
                                  ]))

            lib_source = user_of_external_library_root.add(
                name='lib',
                entry=Directory())
            lib_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('my-external-library', URGENCY_ERROR)",
                                  "LIBRARY(members=[H(filename='user-library.h'), C(filename='user-library.c')])"]))
            lib_source.add(
                name='user-library.h',
                entry=File(lines=['#ifndef USER_LIBRARY_H',
                                  '#define USER_LIBRARY_H',
                                  'const char* user_library_inline_string();',
                                  '#endif']))
            lib_source.add(
                name='user-library.c',
                entry=File(lines=['#include "user-library.h"',
                                  '#include <my-external-library.h>',
                                  'const char* user_library_inline_string() {',
                                  '    return my_external_library_inline_string();',
                                  '}',
                                  'const char* user_library_linked_string() {',
                                  '    return my_external_library_linked_string();',
                                  '}']))

            bin_source = user_of_external_library_root.add(
                name='bin',
                entry=Directory())
            bin_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["EXECUTABLE(exename='inline-string', center=C(filename='inline-string.c'))",
                                  "EXECUTABLE(exename='linked-string', center=C(filename='linked-string.c'))"]))
            bin_source.add(name='inline-string.c',
                           entry=File(lines=['#include <user-library.h>',
                                             '#include <stdio.h>',
                                             'int main(void) {',
                                             r'    printf("%s\n", user_library_inline_string());',
                                             '    return 0;',
                                             '}']))
            bin_source.add(name='linked-string.c',
                           entry=File(lines=['#include <user-library.h>',
                                             '#include <stdio.h>',
                                             'int main(void) {',
                                             r'    printf("%s\n", user_library_linked_string());',
                                             '    return 0;',
                                             '}']))
            pass
        pass

    def test(self):
        external_library_source = self.__fs.rootdirectory().find(['source', 'external-library'])
        external_library_package = LocalPackage(rootdirectory=external_library_source,
                                                setups=[ExplicitDirectorySetup(),
                                                        ExplicitCSetup(),
                                                        CMakeSetup()])
        external_library_package.boil(external_nodes=[])
        external_library_package.output()

        self.__fs.sync()

        external_library_builddir = self.__fs.rootdirectory().find(['build', 'external-library'])
        installdir = self.__fs.rootdirectory().find(['install'])

        commands.cmake(packageroot=external_library_source.abspath(),
                       builddir=external_library_builddir.abspath(),
                       args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(installdir.abspath())])
        commands.make(builddir=external_library_builddir.abspath(), args=['install'])

        user_source = self.__fs.rootdirectory().find(['source', 'user-of-external-library'])
        user_package = LocalPackage(rootdirectory=user_source,
                                    setups=[ExplicitDirectorySetup(),
                                            ExplicitCSetup(),
                                            CMakeSetup()])
        user_package.boil(external_nodes=[])
        user_package.output()

        self.__fs.sync()

        user_builddir = self.__fs.rootdirectory().find(['build', 'user-of-external-library'])

        commands.cmake(packageroot=user_source.abspath(),
                       builddir=user_builddir.abspath(),
                       args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(installdir.abspath())])
        commands.make(builddir=user_builddir.abspath(), args=['VERBOSE=yes', 'install'])

        # 'inline-string' prints the string that the
        # 'user-of-external-library' package's confix code defined on
        # the command line. package 'external-library' leave the value
        # of that string open for users to define on the command line
        # (testing the 'cmdlinemacros' parameter of
        # CMAKE_EXTERNAL_LIBRARY()).
        pipe = subprocess.Popen([os.sep.join(user_builddir.abspath()+['bin', 'inline-string'])], stdout=subprocess.PIPE)
        self.failUnlessEqual(pipe.stdout.next(), 'my-propagated-cmdline-macro\n')

        # 'linked-string' prints the strign that is defined in the
        # 'external-library' package.
        pipe = subprocess.Popen([os.sep.join(user_builddir.abspath()+['bin', 'linked-string'])], stdout=subprocess.PIPE)
        self.failUnlessEqual(pipe.stdout.next(), 'my-external-library-linked-string\n')

        pass
                              
if __name__ == '__main__':
    unittest.TextTestRunner().run(ExternalLibraryBuildSuite())
    pass

