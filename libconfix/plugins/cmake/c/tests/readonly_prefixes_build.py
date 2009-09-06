# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.plugins.automake.repo_automake import AutomakeCascadedPackageRepository

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import unittest
import os

class ReadonlyPrefixesBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ReadonlyPrefixesBuildTest('test'))
        pass
    pass

class ReadonlyPrefixesBuildTest(PersistentTestCase):
    def test(self):

        # one-readonly, installed in prefix one-readonly
        # two-readonly, installed in prefix two-readonly
        # three-regular, installed on regular prefix
        # linked, using all three
        
        fs = FileSystem(path=self.rootpath())

        sourcedir = fs.rootdirectory().add(name='source', entry=Directory())
        builddir = fs.rootdirectory().add(name='build', entry=Directory())
        installdir = fs.rootdirectory().add(name='install', entry=Directory())
        regular_installdir = fs.rootdirectory().add(name='regular', entry=Directory())

        one_readonly_sourcedir = sourcedir.add(name='one-readonly', entry=Directory())
        one_readonly_builddir = builddir.add(name='one-readonly', entry=Directory())
        one_readonly_installdir = installdir.add(name='one-readonly', entry=Directory())

        two_readonly_sourcedir = sourcedir.add(name='two-readonly', entry=Directory())
        two_readonly_builddir = builddir.add(name='two-readonly', entry=Directory())
        two_readonly_installdir = installdir.add(name='two-readonly', entry=Directory())

        three_regular_sourcedir = sourcedir.add(name='three-regular', entry=Directory())
        three_regular_builddir = builddir.add(name='three-regular', entry=Directory())

        linked_sourcedir = sourcedir.add(name='linked', entry=Directory())
        linked_builddir = builddir.add(name='linked', entry=Directory())
        
        # one_readonly
        if True:
            one_readonly_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("one-readonly")',
                                  'PACKAGE_VERSION("1.2.3")']))
            one_readonly_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(members=[H(filename="one_readonly.h"), C(filename="one_readonly.c")])']))
            one_readonly_sourcedir.add(
                name='one_readonly.h',
                entry=File(lines=['#ifndef one_readonly_h',
                                  '#define one_readonly_h',
                                  'void one_readonly();',
                                  '#endif',
                                  ]))
            one_readonly_sourcedir.add(
                name='one_readonly.c',
                entry=File(lines=['#include "one_readonly.h"',
                                  'void one_readonly() {}']))

            one_readonly_package = LocalPackage(rootdirectory=one_readonly_sourcedir,
                                                setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            one_readonly_package.boil(external_nodes=[])
            one_readonly_package.output()
            fs.sync()

            commands.cmake(packageroot=one_readonly_sourcedir.abspath(),
                           builddir=one_readonly_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(one_readonly_installdir.abspath())])
            commands.make(builddir=one_readonly_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(one_readonly_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(one_readonly_installdir.abspath()+['include', 'one_readonly.h'])))
            pass
    
        # two_readonly
        if True:
            two_readonly_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("two-readonly")',
                                  'PACKAGE_VERSION("1.2.3")']))
            two_readonly_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(members=[H(filename="two_readonly.h"), C(filename="two_readonly.c")])']))
            two_readonly_sourcedir.add(
                name='two_readonly.h',
                entry=File(lines=['#ifndef two_readonly_h',
                                  '#define two_readonly_h',
                                  'void two_readonly();',
                                  '#endif',
                                  ]))
            two_readonly_sourcedir.add(
                name='two_readonly.c',
                entry=File(lines=['#include "two_readonly.h"',
                                  'void two_readonly() {}']))

            two_readonly_package = LocalPackage(rootdirectory=two_readonly_sourcedir,
                                                setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            two_readonly_package.boil(external_nodes=[])
            two_readonly_package.output()
            fs.sync()

            commands.cmake(packageroot=two_readonly_sourcedir.abspath(),
                           builddir=two_readonly_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(two_readonly_installdir.abspath())])
            commands.make(builddir=two_readonly_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(two_readonly_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(two_readonly_installdir.abspath()+['include', 'two_readonly.h'])))
            pass

        # three_regular
        if True:
            three_regular_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("three-regular")',
                                  'PACKAGE_VERSION("1.2.3")']))
            three_regular_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(members=[H(filename="three_regular.h"), C(filename="three_regular.c")])']))
            three_regular_sourcedir.add(
                name='three_regular.h',
                entry=File(lines=['#ifndef three_regular_h',
                                  '#define three_regular_h',
                                  'void three_regular();',
                                  '#endif',
                                  ]))
            three_regular_sourcedir.add(
                name='three_regular.c',
                entry=File(lines=['#include "three_regular.h"',
                                  'void three_regular() {}']))

            three_regular_package = LocalPackage(rootdirectory=three_regular_sourcedir,
                                                setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            three_regular_package.boil(external_nodes=[])
            three_regular_package.output()
            fs.sync()

            commands.cmake(packageroot=three_regular_sourcedir.abspath(),
                           builddir=three_regular_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(regular_installdir.abspath())])
            commands.make(builddir=three_regular_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(regular_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(regular_installdir.abspath()+['include', 'three_regular.h'])))
            pass

        # linked
        if True:
            linked_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("linked")',
                                  'PACKAGE_VERSION("1.2.3")']))
            linked_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['EXECUTABLE(exename="exe", center=C(filename="main.c"))']))
            linked_sourcedir.add(
                name='main.c',
                entry=File(lines=['#include <one_readonly.h>',
                                  '#include <two_readonly.h>',
                                  '#include <three_regular.h>',
                                  '// CONFIX:REQUIRE_H("one_readonly.h", URGENCY_ERROR)',
                                  '// CONFIX:REQUIRE_H("two_readonly.h", URGENCY_ERROR)',
                                  '// CONFIX:REQUIRE_H("three_regular.h", URGENCY_ERROR)',
                                  'int main(void) {',
                                  '    one_readonly();',
                                  '    two_readonly();',
                                  '    three_regular();',
                                  '}']))

            linked_package = LocalPackage(rootdirectory=linked_sourcedir,
                                          setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])

            # read repo files along the cascade
            repo = AutomakeCascadedPackageRepository(
                prefix=regular_installdir.abspath(),
                readonly_prefixes=[two_readonly_installdir.abspath(), one_readonly_installdir.abspath()])
            
            linked_package.boil(external_nodes=repo.nodes())
            linked_package.output()
            fs.sync()

            commands.cmake(packageroot=linked_sourcedir.abspath(),
                           builddir=linked_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(regular_installdir.abspath()),
                                 '-DREADONLY_PREFIXES='+'/'.join(one_readonly_installdir.abspath())+';'+'/'.join(two_readonly_installdir.abspath())])
            commands.make(builddir=linked_builddir.abspath(), args=[])
            
            # paranoia
            self.failUnless(os.path.isfile(os.sep.join(linked_builddir.abspath()+['exe'])))
            pass

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ReadonlyPrefixesBuildSuite())
    pass

