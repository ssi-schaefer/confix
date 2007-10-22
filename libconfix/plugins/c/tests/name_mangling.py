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
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder

class NameManglingSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LongNamesWithLibtool('test'))
        self.addTest(LongNamesWithoutLibtool('test'))
        self.addTest(ShortNamesWithLibtool('test'))
        self.addTest(ShortNamesWithoutLibtool('test'))
        pass
    pass

class NamesBase(unittest.TestCase):
    def use_libtool(self): assert 0
    def short_libnames(self): assert 0
    def setUp(self):
        fs = FileSystem(path=['', 'path', 'to', 'our', 'package'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('package')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        libdir = fs.rootdirectory().add(
            name='lib1',
            entry=Directory())
        libdir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        libdir = libdir.add(
            name='lib2',
            entry=Directory())
        libdir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        libdir.add(
            name='file.c',
            entry=File())

        exedir = fs.rootdirectory().add(
            name='exe1',
            entry=Directory())
        exedir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        exedir = exedir.add(
            name='exe2',
            entry=Directory())
        exedir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        exedir.add(
            name='main.c',
            entry=File(lines=['int main(void) { return 0; }']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultDirectorySetup(),
                                       DefaultCSetup(use_libtool=self.use_libtool(),
                                                     short_libnames=self.short_libnames())])
        package.boil(external_nodes=[])

        libdir_builder = package.rootbuilder().find_entry_builder(['lib1', 'lib2'])
        exedir_builder = package.rootbuilder().find_entry_builder(['exe1', 'exe2'])
        self.failIf(libdir_builder is None)
        self.failIf(exedir_builder is None)

        for builder in libdir_builder.builders():
            if isinstance(builder, LibraryBuilder):
                self.lib_builder_ = builder
                break
            pass
        else:
            self.fail()
            pass

        for builder in exedir_builder.builders():
            if isinstance(builder, ExecutableBuilder):
                self.exe_builder_ = builder
                break
            pass
        else:
            self.fail()
            pass
        
        pass
    pass

class LongNamesBase(NamesBase):
    def short_libnames(self):
        return False
    def test(self):
        self.failUnlessEqual(self.lib_builder_.basename(), 'package_lib1_lib2')
        self.failUnlessEqual(self.exe_builder_.exename(), 'package_exe1_exe2_main')
        pass
    pass
class LongNamesWithLibtool(LongNamesBase):
    def use_libtool(self): return True
    pass
class LongNamesWithoutLibtool(LongNamesBase):
    def use_libtool(self): return True
    pass

class ShortNamesBase(NamesBase):
    def short_libnames(self):
        return True
    def test(self):
        # hmmm. we cannot define the short mangling (it depends upon
        # the whole package content, and the order of its evaluation),
        # so we only check that the computed short name is shorter
        # than the long name :-}
        self.failUnless(len(self.lib_builder_.basename()) < len('package_lib1_lib2'))
        self.failUnlessEqual(self.exe_builder_.exename(), 'package_exe1_exe2_main')
        pass
    pass
class ShortNamesWithLibtool(ShortNamesBase):
    def use_libtool(self): return True
    pass
class ShortNamesWithoutLibtool(ShortNamesBase):
    def use_libtool(self): return True
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(NameManglingSuite())
    pass

