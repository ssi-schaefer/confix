# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import unittest

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.testutils import dirhier

class ExecutableSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolExecutable('common_test'))
        self.addTest(StandardExecutable('common_test'))
        self.addTest(LibtoolExecutable('test'))
        self.addTest(StandardExecutable('test'))
        self.addTest(CheckAndNoinstProgram('test'))
        self.addTest(LDADD('test_libtool'))
        self.addTest(LDADD('test_no_libtool'))
        pass
    pass

class ExecutableBase(unittest.TestCase):
    def use_libtool(self): assert 0, 'abstract'
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        liblo = self.fs_.rootdirectory().add(name='lo', entry=Directory())
        liblo.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
        liblo.add(name='lo.h',
                  entry=File(lines=['#ifndef LO_H',
                                    '#define LO_H',
                                    'void lo();',
                                    '#endif',
                                    ]))
        liblo.add(name='lo.c',
                  entry=File(lines=['void lo() {}']))
        
        libhi = self.fs_.rootdirectory().add(name='hi', entry=Directory())
        libhi.add(name=const.CONFIX2_DIR, entry=File(lines={}))
        libhi.add(name='hi.h',
                   entry=File(lines=['#ifndef HI_H',
                                     '#  define HI_H',
                                     '#endif',
                                     'void hi();']))
        libhi.add(name='hi.c',
                   entry=File(lines=['#include <hi.h>',
                                     '#include <lo.h>',
                                     'void hi() { lo(); }']))
        
        exe = self.fs_.rootdirectory().add(name='exe', entry=Directory())
        exe.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
        exe.add(name='main.c',
                entry=File(lines=['#include <hi.h>',
                                  'int main(void) {',
                                  '    hi();',
                                  '    return 0;',
                                  '}']))
        exe.add(name='something.c', entry=File())
        
        self.package_ = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                                     setups=[ConfixSetup(short_libnames=False, use_libtool=self.use_libtool())])
        self.package_.boil(external_nodes=[])
        self.package_.output()

        self.lodir_builder_ = self.package_.rootbuilder().find_entry_builder(['lo'])
        self.hidir_builder_ = self.package_.rootbuilder().find_entry_builder(['hi'])
        self.exedir_builder_ = self.package_.rootbuilder().find_entry_builder(['exe'])
        assert self.lodir_builder_
        assert self.hidir_builder_
        assert self.exedir_builder_

        self.lolib_builder_ = None
        self.hilib_builder_ = None
        self.exe_builder_ = None

        for b in self.lodir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.lolib_builder_ = b
                pass
            pass
        for b in self.hidir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.hilib_builder_ = b
                pass
            pass
        for b in self.exedir_builder_.builders():
            if isinstance(b, ExecutableBuilder):
                self.exe_builder_ = b
                pass
            pass
        pass

    def tearDown(self):
        self.fs_ = None
        self.package_ = None
        pass

    def common_test(self):
        self.failUnless('blah_exe_main' in self.exedir_builder_.makefile_am().bin_programs())
        self.failUnless('main.c' in self.exedir_builder_.makefile_am().compound_sources('blah_exe_main'))
        self.failUnless('something.c' in self.exedir_builder_.makefile_am().compound_sources('blah_exe_main'))
        pass
    pass

class LibtoolExecutable(ExecutableBase):
    def use_libtool(self): return True

    # a libtool executable must have only its direct dependencies on
    # the link line.

    def test(self):
        self.failUnlessEqual(self.exedir_builder_.makefile_am().compound_ldadd('blah_exe_main'),
                             ['-L$(top_builddir)/hi',
                              '-lblah_hi'])
        pass
    pass

class StandardExecutable(ExecutableBase):
    def use_libtool(self): return False

    # a standard (non-libtool) executable must have all its
    # dependencies, in reverse-topological order.

    def test(self):
        self.failUnlessEqual(self.exedir_builder_.makefile_am().compound_ldadd('blah_exe_main'),
                             ['-L$(top_builddir)/hi',
                              '-L$(top_builddir)/lo',
                              '-lblah_hi',
                              '-lblah_lo'])
        pass
    pass

class CheckAndNoinstProgram(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='_check_proggy.c',
                               entry=File(lines=['int main(void) { return 0; }']))
        fs.rootdirectory().add(name='_proggy.c',
                               entry=File(lines=['int main(void) { return 0; }']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('blah__check_proggy' in package.rootbuilder().makefile_am().check_programs())
        self.failUnless('blah__proggy' in package.rootbuilder().makefile_am().noinst_programs())
        pass
    pass

class LDADD(unittest.TestCase):
    def setUp(self):
        self.fs_ = FileSystem(path=['don\'t', 'care'])
        self.fs_.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LDADD')",
                              "PACKAGE_VERSION('1.2.3')"]))
        self.fs_.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib = self.fs_.rootdirectory().add(
            name='lib',
            entry=Directory())
        lib.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib.add(
            name='lib.h',
            entry=File())
        lib.add(
            name='lib.c',
            entry=File())

        exe = self.fs_.rootdirectory().add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File())
        exe.add(
            name='exe.c',
            entry=File(lines=['#include <lib.h>',
                              'int main() {}']))
        pass

    def test_libtool(self):
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=True, short_libnames=False)])
        package.boil(external_nodes=[])
        package.output()

        exedir_builder = package.rootbuilder().find_entry_builder(['exe'])
        self.failUnless('-lLDADD_lib' in exedir_builder.makefile_am().compound_ldadd('LDADD_exe_exe'))
        pass

    def test_no_libtool(self):
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])
        package.output()

        exedir_builder = package.rootbuilder().find_entry_builder(['exe'])
        self.failUnless('-lLDADD_lib' in exedir_builder.makefile_am().compound_ldadd('LDADD_exe_exe'))
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExecutableSuite())
    pass
