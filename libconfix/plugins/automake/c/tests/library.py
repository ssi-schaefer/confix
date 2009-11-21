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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.c.library import LibraryBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier

import unittest

class LibraryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolLibrary('test_library_alone'))
        self.addTest(LibtoolLibrary('test_version'))
        self.addTest(ArchiveLibrary('test_library_alone'))
        self.addTest(ArchiveLibrary('test_AC_PROG_RANLIB'))
        self.addTest(LIBADD('test_libtool'))
        self.addTest(LIBADD('test_no_libtool'))
        pass
    pass

class LibraryBase(unittest.TestCase):
    def use_libtool(self): assert 0
    
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        liblo = self.fs_.rootdirectory().add(name='lo', entry=Directory())
        liblo.add(name=const.CONFIX2_DIR,
                  entry=File(lines=["LIBRARY_VERSION((1,2,3))"]))
        liblo.add(name='lo.h',
                  entry=File(lines=['#ifndef LO_H',
                                    '#  define LO_H',
                                    '#endif',
                                    'void lo();']))
        liblo.add(name='lo.c',
                  entry=File(lines=['void lo() {}']))

        self.package_ = LocalPackage(
            rootdirectory=self.fs_.rootdirectory(),
            setups=[ConfixSetup(use_libtool=self.use_libtool())])
        self.package_.boil(external_nodes=[])
        self.package_.output()

        self.lodir_builder_ = self.package_.rootbuilder().find_entry_builder(['lo'])
        self.failIf(self.lodir_builder_ is None)
        self.lodir_output_builder_ = find_automake_output_builder(self.lodir_builder_)
        self.failIf(self.lodir_output_builder_ is None)
        
        self.lolib_builder_ = None
        for b in self.lodir_builder_.iter_builders():
            if isinstance(b, LibraryBuilder):
                self.lolib_builder_ = b
                pass
            pass

        assert self.lolib_builder_ is not None

        pass
        
    def tearDown(self):
        self.fs_ = None
        self.package_ = None
        pass
        
    def test_library_alone(self):
        mf_am = self.lodir_output_builder_.makefile_am()
        self.failIfEqual(mf_am, None)

        # we ought to be building a library here
        self.failUnlessEqual(self.lolib_builder_.basename(), 'blah_lo')
        self.failUnless(self.libname() in mf_am.dir_primary(dir='lib', primary=self.primary()))

        # lo.{h,c} are the sources

        sources = mf_am.compound_sources(self.amlibname())
        self.failIf(sources is None)
        self.failUnless('lo.h' in sources)
        self.failUnless('lo.c' in sources)
        
        pass
    
    pass

class LibtoolLibrary(LibraryBase):
    def use_libtool(self): return True
    def libname(self): return 'libblah_lo.la'
    def amlibname(self): return 'libblah_lo_la'
    def primary(self): return 'LTLIBRARIES'

    def test_version(self):
        flags = self.lodir_output_builder_.makefile_am().compound_ldflags(self.amlibname())
        self.failIf(flags is None)
        self.failUnless('-version-info 1:2:3' in flags)
        pass
    pass

class ArchiveLibrary(LibraryBase):
    def use_libtool(self): return False
    def libname(self): return 'libblah_lo.a'
    def amlibname(self): return 'libblah_lo_a'
    def primary(self): return 'LIBRARIES'

    def test_AC_PROG_RANLIB(self):
        conf_ac = self.fs_.rootdirectory().find(['configure.ac'])
        self.failIf(conf_ac is None)
        found_AC_PROG_RANLIB = False
        for l in conf_ac.lines():
            if l == 'AC_PROG_RANLIB':
                found_AC_PROG_RANLIB = True
                continue
            pass
        self.failUnless(found_AC_PROG_RANLIB)
        pass
    pass

class LIBADD(unittest.TestCase):
    def setUp(self):
        self.fs_ = FileSystem(path=['don\'t', 'care'])
        self.fs_.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LIBADD')",
                              "PACKAGE_VERSION('1.2.3')"]))
        self.fs_.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = self.fs_.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo.add(
            name='lo.h',
            entry=File())
        lo.add(
            name='lo.c',
            entry=File())

        hi = self.fs_.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi.add(
            name='hi.c',
            entry=File(lines=['#include <lo.h>']))
        pass

    def test_libtool(self):
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=True)])
        package.boil(external_nodes=[])
        package.output()

        hidir_builder = package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)

        self.failUnless('-lLIBADD_lo' in hidir_output_builder.makefile_am().compound_libadd('libLIBADD_hi_la'))
        pass

    def test_no_libtool(self):
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        hidir_builder = package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)
        
        self.failUnless(hidir_output_builder.makefile_am().compound_libadd('libLIBADD_hi_a') is None)
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryInMemorySuite())
    pass
