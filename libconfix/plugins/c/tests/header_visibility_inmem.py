# Copyright (C) 2009-2012 Joerg Faschingbauer

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

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.c import C

from libconfix.plugins.c.h import HeaderBuilder
import libconfix.plugins.c.h

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import unittest

class Interfaces(unittest.TestCase):
    def test_auto_fileproperty_only(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=[]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), ['xxx'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['xxx'])
        pass

    def test_auto_fileiface_only(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), ['xxx'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['xxx'])
        pass

    def test_auto_fileiface_fileproperty_conflict(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return
        self.fail()
        pass

    def test_auto_fileiface_diriface_conflict(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('xxx')"]))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['yyy'])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return
        self.fail()
        pass

    def test_auto_fileproperty_diriface_conflict(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('xxx')"]))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File())
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return
        self.fail()
        pass

    # this comes out of a regression I had one day. INSTALLDIR_H('')
    # led to headerfiles being provided as '/file.h' rather than
    # 'file.h'.
    def test_auto_INSTALLDIR_H_empty_string(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('')"]))
        lo.add(
            name='lo.h',
            entry=File())
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[]))
        hi.add(
            name='hi.cc',
            entry=File(lines=["//CONFIX:REQUIRE_H('lo.h', REQUIRED)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        pass

    def test_auto_INSTALLDIR_H_overrides_namespace(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('')"]))
        lo.add(
            name='lo.h',
            entry=File(lines=['namespace x {',
                              '} // /namespace x']))
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[]))
        hi.add(
            name='hi.cc',
            entry=File(lines=["//CONFIX:REQUIRE_H('lo.h', REQUIRED)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        pass

    def test_explicit_diriface(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='file.h', install=['xxx'])"]))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(), C()])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        
        self.failUnlessEqual(file_h_builder.visibility(), ['xxx'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['xxx'])
        pass

    def test_explicit_fileproperty_conflict(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='file.h', install=['xxx'])"]))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File())
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(), C()])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return
        self.fail()
        pass

    def test_explicit_fileiface_conflict(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='file.h', install=['xxx'])"]))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['yyy'])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(), C()])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            return
        self.fail()
        pass

    pass

class Namespace(unittest.TestCase):
    def testSimple(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))
        
        self.failUnlessEqual(file_h_builder.visibility(), ['A'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['A'])
        pass

    def testNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              'namespace B {',
                              '}; // /namespace',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), ['A', 'B'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['A', 'B'])
        pass

    def testGlobal(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), [])
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], [])
        pass

    def testAmbiguousFlat(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              '}; // /namespace',
                              'namespace B {',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.BadNamespace))
            return
        self.fail()
        pass
    def testAmbiguousNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              ' namespace A1 {',
                              ' }; // /namespace',
                              '}; // /namespace',
                              'namespace A {',
                              ' namespace A2 {',
                              ' }; // /namespace',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.BadNamespace))
            return
        self.fail()
        pass
    def testDirectory(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=["PACKAGE_NAME('xxx')",
                                                 "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=["SET_FILE_PROPERTY(",
                                                 "    filename='file.h', ",
                                                 "    name='INSTALLPATH_CINCLUDE',",
                                                 "    value=['xxx'])"]))
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), ['xxx'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['xxx'])
        pass

    def test_bad_namespace_and_no_idea_where_to_install(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        rootdirectory.add(
            name='file.h',
            entry=File(lines=['namespace X {',
                              '}']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.BadNamespace))
            pass
        pass

    def test_bad_namespace_but_good_installdir(self):
        fs = FileSystem(path=["don't", 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['INSTALLDIR_H("")']))
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace X {',
                              '}']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        pass
    
    pass

class InstallPriorities(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('install/from/dir/iface')"]))
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace install {',
                              'namespace from {',
                              'namespace ns {',
                              'namespace hierarchy {',
                              '} // /namespace',
                              '} // /namespace',
                              '} // /namespace',
                              '} // /namespace',
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visibility(), ['install','from','dir','iface'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['install','from','dir','iface'])
        pass
    pass

class HeaderInstallPath(unittest.TestCase):
    def test_iface(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH('a/b')"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failUnlessEqual(file_h_builder.visibility(), ['a', 'b'])
        self.failUnless(file_h_builder.public())
        self.failUnlessEqual(file_h_builder.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnlessEqual(file_h_builder.package_visibility_action()[1], ['a', 'b'])
        pass

    def test_ambig1(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        # ambiguity here
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH('a/b')"]))
        file.set_property('INSTALLPATH_CINCLUDE', ['x'])

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return
        self.fail()
        pass

    def test_ambig2(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))

        # ambiguity here
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['INSTALLDIR_H("x/y")']))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File())
        file.set_property('INSTALLPATH_CINCLUDE', ['x'])

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        try:
            package.boil(external_nodes=[])
            package.output()
        except Error, e:
            self.failUnless(e.contains_error_of_type(libconfix.plugins.c.h.AmbiguousVisibility))
            return 
        self.fail()
        pass

    pass

class IntelligentConditionalLocalInstall(unittest.TestCase):
    # Two modules lo and hi where hi.h includes lo.h. Both header
    # files are made visible with no prefix directory. These files
    # should not be locally installed into $(prefix)/confix-include. A
    # user module should get an appropriate build info that contains
    # the relative source paths of each of the files, and should
    # compose its include path appropriately.
    def test_basic(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        lodir = rootdirectory.add(
            name='lo',
            entry=Directory())
        lodir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lodir.add(
            name='lo.h',
            entry=File())

        hidir = rootdirectory.add(
            name='hi',
            entry=Directory())
        hidir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hidir.add(
            name='hi.h',
            entry=File(lines=['#include <lo.h>']))

        user = rootdirectory.add(
            name='user',
            entry=Directory())
        user.add(
            name=const.CONFIX2_DIR,
            entry=File())
        user.add(
            name='user.c',
            entry=File(lines=['#include <hi.h>']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        user_c_builder = package.rootbuilder().find_entry_builder(['user', 'user.c'])
        self.failIf(user_c_builder is None)

        hi_pos = lo_pos = None
        for i in xrange(len(user_c_builder.native_local_include_dirs())):
            if user_c_builder.native_local_include_dirs()[i] == ['hi']:
                self.failUnless(hi_pos is None)
                hi_pos = i
                continue
            if user_c_builder.native_local_include_dirs()[i] == ['lo']:
                self.failUnless(lo_pos is None)
                lo_pos = i
                continue
            pass

        self.failIf(hi_pos is None)
        self.failIf(lo_pos is None)
        self.failIf(hi_pos > lo_pos)

        lo_h = package.rootbuilder().find_entry_builder(['lo', 'lo.h'])
        self.failUnlessEqual(lo_h.visibility(), [])
        self.failUnless(lo_h.public())
        self.failUnlessEqual(lo_h.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
        self.failUnlessEqual(lo_h.package_visibility_action()[1], ['lo'])
        
        pass

    # Local install from root directory (pathologic situation :-)
    def test_from_root_directory(self):
        
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        file_h = rootdirectory.add(
            name='file.h',
            entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['x', 'y'])

        user = rootdirectory.add(
            name='user',
            entry=Directory())
        user.add(
            name=const.CONFIX2_DIR,
            entry=File())
        user.add(
            name='user.cc',
            entry=File(lines=['#include <x/y/file.h>',
                              '// CONFIX:REQUIRE_H(filename="x/y/file.h", urgency=REQUIRED)']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        file_h_builder = package.rootbuilder().find_entry_builder(['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnless(file_h_builder.visibility(), ['x', 'y'])
        self.failUnless(file_h_builder.public())
        self.failUnless(file_h_builder.package_visibility_action()[0] is HeaderBuilder.LOCALVISIBILITY_INSTALL)
        self.failUnless(file_h_builder.package_visibility_action()[1] == ['x', 'y'])
        pass

    pass

    
class NoPublicInstall(unittest.TestCase):
    def test_explicit_no_public_visibility(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='header.h', public=False)"]))
        fs.rootdirectory().add(
            name='header.h',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[Boilerplate(), C()])
        package.boil(external_nodes=[])
        package.output()

        h = package.rootbuilder().find_entry_builder(['header.h'])

        # no explicit local visibility is given, so the namespace
        # recognizer sees no namespace - and the file can locally be
        # included directly.
        self.failUnlessEqual(h.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
        self.failUnlessEqual(h.package_visibility_action()[1], [])

        # public visibility is explicitly not wanted.
        self.failIf(h.public())
        pass
    
    def test_auto_no_public_visibility(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_HEADER_PUBLIC(shellmatch='header.h', public=False)",
                              "SET_HEADER_PUBLIC(regex='^.+a.h$', public=False)"]))
        fs.rootdirectory().add(
            name='header.h',
            entry=File())
        fs.rootdirectory().add(
            name='regexa.h',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        header_h = package.rootbuilder().find_entry_builder(['header.h'])
        regexa_h = package.rootbuilder().find_entry_builder(['regexa.h'])

        # no explicit local visibility is given, so the namespace
        # recognizer sees no namespace - and the file can locally be
        # included directly.
        self.failUnlessEqual(header_h.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
        self.failUnlessEqual(header_h.package_visibility_action()[1], [])
        self.failUnlessEqual(regexa_h.package_visibility_action()[0], HeaderBuilder.LOCALVISIBILITY_DIRECT_INCLUDE)
        self.failUnlessEqual(regexa_h.package_visibility_action()[1], [])
        # public visibility is explicitly not wanted.
        self.failIf(header_h.public())
        self.failIf(regexa_h.public())
        pass
    
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Interfaces))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Namespace))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(InstallPriorities))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HeaderInstallPath))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(IntelligentConditionalLocalInstall))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NoPublicInstall))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
