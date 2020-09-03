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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.plugins.automake import \
     bootstrap, \
     configure, \
     make
from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import sys

class ExplicitPackageBuildTest(PersistentTestCase):
    def test__with_libtool(self):
        self.do_test(True)
        pass
    
    def test__without_libtool(self):
        self.do_test(False)
        pass
    
    def do_test(self, use_libtool):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['lolibrary'])",
                              "DIRECTORY(['hilibrary'])",
                              "DIRECTORY(['executable'])"]))

        lolibrary_dir = source.add(
            name='lolibrary',
            entry=Directory())
        hilibrary_dir = source.add(
            name='hilibrary',
            entry=Directory())
        executable_dir = source.add(
            name='executable',
            entry=Directory())

        lolibrary_dir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[H(filename='lo.h'),",
                              "                 C(filename='lo1.c'),",
                              "                 C(filename='lo2.c')],",
                              "        basename='hansi')"]))
        lolibrary_dir.add(
            name='lo.h',
            entry=File(lines=['#ifndef LO_H',
                              '#define LO_H',
                              '#ifdef __cplusplus',
                              'extern "C" {',
                              '#endif',
                              'void lo1(void);',
                              'void lo2(void);',
                              '#ifdef __cplusplus',
                              '}',
                              '#endif',
                              '#endif']))
        lolibrary_dir.add(
            name='lo1.c',
            entry=File(lines=['#include "lo.h"',
                              'void lo1(void) { lo2(); }']))
        lolibrary_dir.add(
            name='lo2.c',
            entry=File(lines=['#include "lo.h"',
                              'void lo2(void) {}']))

        hilibrary_dir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[H(filename='hi.h', install=['hi']),",
                              "                 CXX(filename='hi.cc')])"]))
        hilibrary_dir.add(
            name='hi.h',
            entry=File(lines=["#ifndef HI_HI_H",
                              "#define HI_HI_H",
                              "void hi();",
                              "#endif"]))
        hilibrary_dir.add(
            name='hi.cc',
            entry=File(lines=['#include "hi.h"',
                              '#include <lo.h>',
                              'void hi() { lo1(); }']))

        executable_dir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(exename='the_executable',",
                              "           center=CXX(filename='main.cc'))"]))
        executable_dir.add(
            name='main.cc',
            entry=File(lines=['#include <hi/hi.h>',
                              'int main() {',
                              '    hi();',
                              '    return 0;',
                              '}']))

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitSetup(use_libtool=use_libtool)])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None)
        make.make(
            builddir=build.abspath(),
            args=[])

        pass
    pass
        
suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExplicitPackageBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
