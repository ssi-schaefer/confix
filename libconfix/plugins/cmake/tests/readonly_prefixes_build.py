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
from libconfix.plugins.cmake.library_dependencies import LibraryDependenciesSetup
from libconfix.plugins.cmake import commands

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.cmake import CMake
from libconfix.setups.c import C

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.repo import AutomakeCascadedPackageRepository
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import unittest
import os
import time

class ReadonlyPrefixesBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
##         self.addTest(ReadonlyPrefixesBuildTest('test'))
##         self.addTest(ReadonlyPrefixesBuildTest('test_library_dependencies_with_readonly_prefixes'))
        self.addTest(ReadonlyPrefixesUtilityBuildTest('test_copy_include_files_to_local_package'))
        pass
    pass

class ReadonlyPrefixesBuildTest(PersistentTestCase):
    def setUp(self):
        super(ReadonlyPrefixesBuildTest, self).setUp()

        # one-readonly, installed in prefix one-readonly
        # two-readonly, installed in prefix two-readonly
        # three-regular, installed on regular prefix
        # linked, using all three
        
        self.__fs = FileSystem(path=self.rootpath())

        sourcedir = self.__fs.rootdirectory().add(name='source', entry=Directory())
        builddir = self.__fs.rootdirectory().add(name='build', entry=Directory())
        installdir = self.__fs.rootdirectory().add(name='install', entry=Directory())
        self.__regular_installdir = self.__fs.rootdirectory().add(name='regular', entry=Directory())

        self.__one_readonly_sourcedir = sourcedir.add(name='one-readonly', entry=Directory())
        self.__one_readonly_builddir = builddir.add(name='one-readonly', entry=Directory())
        self.__one_readonly_installdir = installdir.add(name='one-readonly', entry=Directory())

        self.__two_readonly_sourcedir = sourcedir.add(name='two-readonly', entry=Directory())
        self.__two_readonly_builddir = builddir.add(name='two-readonly', entry=Directory())
        self.__two_readonly_installdir = installdir.add(name='two-readonly', entry=Directory())

        self.__three_regular_sourcedir = sourcedir.add(name='three-regular', entry=Directory())
        self.__three_regular_builddir = builddir.add(name='three-regular', entry=Directory())

        self.__linked_sourcedir = sourcedir.add(name='linked', entry=Directory())
        self.__linked_builddir = builddir.add(name='linked', entry=Directory())
        
        # one_readonly source
        if True:
            self.__one_readonly_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("one-readonly")',
                                  'PACKAGE_VERSION("1.2.3")']))
            self.__one_readonly_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(basename="one", members=[H(filename="one_readonly.h"), C(filename="one_readonly.c")])']))
            self.__one_readonly_sourcedir.add(
                name='one_readonly.h',
                entry=File(lines=['#ifndef one_readonly_h',
                                  '#define one_readonly_h',
                                  'void one_readonly();',
                                  '#endif',
                                  ]))
            self.__one_readonly_sourcedir.add(
                name='one_readonly.c',
                entry=File(lines=['#include "one_readonly.h"',
                                  'void one_readonly() {}']))

            pass
    
        # two_readonly source
        if True:
            self.__two_readonly_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("two-readonly")',
                                  'PACKAGE_VERSION("1.2.3")']))
            self.__two_readonly_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(basename="two", members=[H(filename="two_readonly.h"), C(filename="two_readonly.c")])']))
            self.__two_readonly_sourcedir.add(
                name='two_readonly.h',
                entry=File(lines=['#ifndef two_readonly_h',
                                  '#define two_readonly_h',
                                  'void two_readonly();',
                                  '#endif',
                                  ]))
            self.__two_readonly_sourcedir.add(
                name='two_readonly.c',
                entry=File(lines=['#include "two_readonly.h"',
                                  'void two_readonly() {}']))
            pass

        # three_regular source
        if True:
            self.__three_regular_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("three-regular")',
                                  'PACKAGE_VERSION("1.2.3")']))
            self.__three_regular_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(basename="three", members=[H(filename="three_regular.h"), C(filename="three_regular.c")])']))
            self.__three_regular_sourcedir.add(
                name='three_regular.h',
                entry=File(lines=['#ifndef three_regular_h',
                                  '#define three_regular_h',
                                  'void three_regular();',
                                  '#endif',
                                  ]))
            self.__three_regular_sourcedir.add(
                name='three_regular.c',
                entry=File(lines=['#include "three_regular.h"',
                                  'void three_regular() {}']))
            pass

        # linked source
        if True:
            self.__linked_sourcedir.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("linked")',
                                  'PACKAGE_VERSION("1.2.3")']))
            self.__linked_sourcedir.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['EXECUTABLE(exename="exe", center=C(filename="main.c"))']))
            self.__linked_sourcedir.add(
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

            pass

        # build the three installed packages
        if True:
            one_readonly_package = LocalPackage(rootdirectory=self.__one_readonly_sourcedir,
                                                setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            one_readonly_package.boil(external_nodes=[])
            one_readonly_package.output()
            self.__fs.sync()

            commands.cmake(packageroot=self.__one_readonly_sourcedir.abspath(),
                           builddir=self.__one_readonly_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(self.__one_readonly_installdir.abspath())])
            commands.make(builddir=self.__one_readonly_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(self.__one_readonly_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(self.__one_readonly_installdir.abspath()+['include', 'one_readonly.h'])))
            pass

        if True:
            two_readonly_package = LocalPackage(rootdirectory=self.__two_readonly_sourcedir,
                                                setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            two_readonly_package.boil(external_nodes=[])
            two_readonly_package.output()
            self.__fs.sync()

            commands.cmake(packageroot=self.__two_readonly_sourcedir.abspath(),
                           builddir=self.__two_readonly_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(self.__two_readonly_installdir.abspath())])
            commands.make(builddir=self.__two_readonly_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(self.__two_readonly_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(self.__two_readonly_installdir.abspath()+['include', 'two_readonly.h'])))
            pass

        if True:
            three_regular_package = LocalPackage(rootdirectory=self.__three_regular_sourcedir,
                                                 setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            three_regular_package.boil(external_nodes=[])
            three_regular_package.output()
            self.__fs.sync()

            commands.cmake(packageroot=self.__three_regular_sourcedir.abspath(),
                           builddir=self.__three_regular_builddir.abspath(),
                           args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(self.__regular_installdir.abspath())])
            commands.make(builddir=self.__three_regular_builddir.abspath(), args=['install'])

            # paranoia
            self.failUnless(os.path.isdir(os.sep.join(self.__regular_installdir.abspath()+['lib'])))
            self.failUnless(os.path.isfile(os.sep.join(self.__regular_installdir.abspath()+['include', 'three_regular.h'])))
            pass
        
        pass

    def test(self):
        linked_package = LocalPackage(rootdirectory=self.__linked_sourcedir,
                                      setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])

        # read repo files along the cascade
        repo = AutomakeCascadedPackageRepository(
            prefix=self.__regular_installdir.abspath(),
            readonly_prefixes=[self.__two_readonly_installdir.abspath(), self.__one_readonly_installdir.abspath()])
            
        linked_package.boil(external_nodes=repo.iter_nodes())
        linked_package.output()
        self.__fs.sync()

        commands.cmake(packageroot=self.__linked_sourcedir.abspath(),
                       builddir=self.__linked_builddir.abspath(),
                       args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(self.__regular_installdir.abspath()),
                             '-DREADONLY_PREFIXES='+
                             '/'.join(self.__one_readonly_installdir.abspath())+';'+
                             '/'.join(self.__two_readonly_installdir.abspath())])
        commands.make(builddir=self.__linked_builddir.abspath(), args=[])

        self.failUnless(os.path.isfile(os.sep.join(self.__linked_builddir.abspath()+['exe'])))
        pass

    def test_library_dependencies_with_readonly_prefixes(self):
        # boil package with library dependencies enabled.
        linked_package = LocalPackage(rootdirectory=self.__linked_sourcedir,
                                      setups=[LibraryDependenciesSetup(),
                                              ExplicitDirectorySetup(),
                                              ExplicitCSetup(),
                                              CMakeSetup()])

        # read repo files along the cascade
        repo = AutomakeCascadedPackageRepository(
            prefix=self.__regular_installdir.abspath(),
            readonly_prefixes=[self.__two_readonly_installdir.abspath(), self.__one_readonly_installdir.abspath()])
            
        linked_package.boil(external_nodes=repo.iter_nodes())
        linked_package.output()
        self.__fs.sync()

        commands.cmake(packageroot=self.__linked_sourcedir.abspath(),
                       builddir=self.__linked_builddir.abspath(),
                       args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(self.__regular_installdir.abspath()),
                             '-DREADONLY_PREFIXES='+
                             '/'.join(self.__one_readonly_installdir.abspath())+';'+
                             '/'.join(self.__two_readonly_installdir.abspath())])
        commands.make(builddir=self.__linked_builddir.abspath(), args=[])

        # wait a bit and then touch libone.a.
        if True:
            time.sleep(1)
            libone = os.sep.join(self.__one_readonly_installdir.abspath()+['lib', 'libone.a'])
            os.utime(libone, None)
            libone_stat = os.stat(libone)

            # exe is rebuilt as it depends on libone.a
            if True:
                commands.make(builddir=self.__linked_builddir.abspath(), args=[])
                self.failUnless(os.stat(os.sep.join(self.__linked_builddir.abspath()+['exe'])).st_mtime >= libone_stat.st_mtime)
                pass
            pass

        # wait a bit and then touch libtwo.a.
        if True:
            time.sleep(1)
            libtwo = os.sep.join(self.__two_readonly_installdir.abspath()+['lib', 'libtwo.a'])
            os.utime(libtwo, None)
            libtwo_stat = os.stat(libtwo)

            # exe is rebuilt as it depends on libtwo.a
            if True:
                commands.make(builddir=self.__linked_builddir.abspath(), args=[])
                self.failUnless(os.stat(os.sep.join(self.__linked_builddir.abspath()+['exe'])).st_mtime >= libtwo_stat.st_mtime)
                pass
            pass

        # wait a bit and then touch libone.a.
        if True:
            time.sleep(1)
            libthree = os.sep.join(self.__regular_installdir.abspath()+['lib', 'libthree.a'])
            os.utime(libthree, None)
            libthree_stat = os.stat(libthree)

            # exe is rebuilt as it depends on libthree.a
            if True:
                commands.make(builddir=self.__linked_builddir.abspath(), args=[])
                self.failUnless(os.stat(os.sep.join(self.__linked_builddir.abspath()+['exe'])).st_mtime >= libthree_stat.st_mtime)
                pass
            pass

        pass
    pass

class ReadonlyPrefixesUtilityBuildTest(PersistentTestCase):
    def test_copy_include_files_to_local_package(self):
        fs = FileSystem(path=self.rootpath())

        if True:
            # readonly_prefix1 has a file flatfile.h, flat in
            # prefix/include.
            readonly_prefix1_source = fs.rootdirectory().add(
                name='readonly_prefix1_source',
                entry=Directory())
            readonly_prefix1_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('readonly_prefix1')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            readonly_prefix1_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["H(filename='flatfile.h')"]))
            readonly_prefix1_source.add(
                name='flatfile.h',
                entry=File())
            readonly_prefix1_build = fs.rootdirectory().add(
                name='readonly_prefix1_build',
                entry=Directory())
            readonly_prefix1_install = fs.rootdirectory().add(
                name='readonly_prefix1_install',
                entry=Directory())

            readonly_prefix1_package = LocalPackage(
                rootdirectory=readonly_prefix1_source,
                setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
            readonly_prefix1_package.boil(external_nodes=[])
            readonly_prefix1_package.output()
            fs.sync()

            commands.cmake(
                packageroot=readonly_prefix1_source.abspath(),
                builddir=readonly_prefix1_build.abspath(),
                prefix=readonly_prefix1_install.abspath())
            commands.make(
                builddir=readonly_prefix1_build.abspath(),
                args=['install'])

            # readonly_prefix2 has a file subdirfile.h, in a subdir,
            # prefix/include/subdir.
            readonly_prefix2_source = fs.rootdirectory().add(
                name='readonly_prefix2_source',
                entry=Directory())
            readonly_prefix2_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('readonly_prefix2')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            readonly_prefix2_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["H(filename='subdirfile.h', install=['subdir'])"]))
            readonly_prefix2_source.add(
                name='subdirfile.h',
                entry=File())
            readonly_prefix2_build = fs.rootdirectory().add(
                name='readonly_prefix2_build',
                entry=Directory())
            readonly_prefix2_install = fs.rootdirectory().add(
                name='readonly_prefix2_install',
                entry=Directory())

            readonly_prefix2_package = LocalPackage(
                rootdirectory=readonly_prefix2_source,
                setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
            readonly_prefix2_package.boil(external_nodes=readonly_prefix1_package.install().nodes())
            readonly_prefix2_package.output()
            fs.sync()

            commands.cmake(
                packageroot=readonly_prefix2_source.abspath(),
                builddir=readonly_prefix2_build.abspath(),
                prefix=readonly_prefix2_install.abspath())
            commands.make(
                builddir=readonly_prefix2_build.abspath(),
                args=['install'])

            # prefix has
            # prefix/include/prefixsubdir/prefixsubdirfile.h
            prefix_source = fs.rootdirectory().add(
                name='prefix_source',
                entry=Directory())
            prefix_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('prefix')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            prefix_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["H(filename='prefixsubdirfile.h', install=['prefixsubdir'])"]))
            prefix_source.add(
                name='prefixsubdirfile.h',
                entry=File())
            prefix_build = fs.rootdirectory().add(
                name='prefix_build',
                entry=Directory())
            prefix_install = fs.rootdirectory().add(
                name='prefix_install',
                entry=Directory())

            prefix_package = LocalPackage(
                rootdirectory=prefix_source,
                setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
            prefix_package.boil(external_nodes=readonly_prefix1_package.install().nodes() + readonly_prefix2_package.install().nodes())
            prefix_package.output()
            fs.sync()

            commands.cmake(
                packageroot=prefix_source.abspath(),
                builddir=prefix_build.abspath(),
                prefix=prefix_install.abspath())
            commands.make(
                builddir=prefix_build.abspath(),
                args=['install'])
            pass

        test_source = fs.rootdirectory().add(
            name='test_source',
            entry=Directory())
        test_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_source')",
                              "PACKAGE_VERSION('1.2.3')"]))
        test_source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_FIND_CALL([',
                              '    "ConfixFindNativeInstalledFile(flatfile_dir flatfile.h include)",',
                              '    "ConfixFindNativeInstalledFile(subdirfile_dir subdirfile.h include/subdir)",',
                              '    "ConfixFindNativeInstalledFile(prefixsubdirfile_dir prefixsubdirfile.h include/prefixsubdir)",',
                              '    "MESSAGE(STATUS flatfile: ${flatfile_dir})",',
                              '    "MESSAGE(STATUS subdirfile: ${subdirfile_dir})",',
                              '    "MESSAGE(STATUS prefixsubdirfile: ${prefixsubdirfile_dir})",',
                              '    ],',
                              '    flags=CMAKE_BUILDINFO_LOCAL,',
                              ')',
                              'CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(',
                              '    outputs=["flatfile-copy.h"],',
                              '    commands=[("cp ${flatfile_dir}/flatfile.h flatfile-copy.h", [])],',
                              '    depends=["${flatfile_dir}/flatfile.h"],',
                              ')',
                              'CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(',
                              '    outputs=["subdirfile-copy.h"],',
                              '    commands=[("cp ${subdirfile_dir}/subdirfile.h subdirfile-copy.h", [])],',
                              '    depends=["${subdirfile_dir}/subdirfile.h"],',
                              ')',
                              'CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(',
                              '    outputs=["prefixsubdirfile-copy.h"],',
                              '    commands=[("cp ${prefixsubdirfile_dir}/prefixsubdirfile.h prefixsubdirfile-copy.h", [])],',
                              '    depends=["${prefixsubdirfile_dir}/prefixsubdirfile.h"],',
                              ')',
                              'CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(',
                              '    name="we-make-them-with-all-target",',
                              '    all=True,',
                              '    depends=["flatfile-copy.h", "subdirfile-copy.h", "prefixsubdirfile-copy.h"])',
                              ]))
        test_build = fs.rootdirectory().add(
            name='test_build',
            entry=Directory())

        test_package = LocalPackage(
            rootdirectory=test_source,
            setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
        test_package.boil(external_nodes=readonly_prefix1_package.install().nodes() + \
                          readonly_prefix2_package.install().nodes() + \
                          prefix_package.install().nodes())
        test_package.output()
        fs.sync()

        commands.cmake(
            packageroot=test_source.abspath(),
            builddir=test_build.abspath(),
            args=['-DREADONLY_PREFIXES='+\
                  '/'.join(prefix_install.abspath())+';'+ \
                  '/'.join(readonly_prefix2_install.abspath())+';'+ \
                  '/'.join(readonly_prefix1_install.abspath())])
        commands.make(
            builddir=test_build.abspath())

        scan.rescan_dir(test_build)
        self.failUnless(test_build.get('flatfile-copy.h'))
        self.failUnless(test_build.get('subdirfile-copy.h'))
        self.failUnless(test_build.get('prefixsubdirfile-copy.h'))
            
        self.fail('comment the others back in')
        pass
    pass


if __name__ == '__main__':
    unittest.TextTestRunner().run(ReadonlyPrefixesBuildSuite())
    pass

