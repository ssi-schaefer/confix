# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2012 Joerg Faschingbauer

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

""" These tests assert fundamental behavior: relating the
nodes. Unfortunately, the tests are tied together with the C plugin -
they should have been written using core objects. (The excuse is that
C was long considered to be core)."""

import unittest

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CIncludePath_NativeLocal, BuildInfo_CLibrary_NativeLocal

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier
from libconfix.testutils import packages

class InternalRequires(unittest.TestCase):
    def testNoInstallPath(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h',
                               entry=File(lines=[]))
        fs.rootdirectory().add(name='file.c',
                               entry=File(lines=['#include "file.h"']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        self.assertEqual(len(package.rootbuilder().requires()), 0)
        pass
    pass        

class RelateBasic(unittest.TestCase):
    def setUp(self):
        fs = FileSystem(path=[''],
                        rootdirectory=packages.lo_hi1_hi2_highest_exe(name='xxx', version='1.2.3'))
        
        self.package_ = LocalPackage(rootdirectory=fs.rootdirectory(),
                                     setups=[ConfixSetup(use_libtool=False)])
        self.package_.boil(external_nodes=[])

        # from here on, we collect things that we will need in the
        # test cases.

        # directory and file builder instances

        self.lodir_builder_ = self.package_.rootbuilder().find_entry_builder(['lo'])
        self.lodir_lo_h_builder_ = self.package_.rootbuilder().find_entry_builder(['lo', 'lo.h'])
        self.lodir_lo_c_builder_ = self.package_.rootbuilder().find_entry_builder(['lo', 'lo.c'])
        
        self.hi1dir_builder_ = self.package_.rootbuilder().find_entry_builder(['hi1'])
        self.hi1dir_hi1_h_builder_ = self.package_.rootbuilder().find_entry_builder(['hi1', 'hi1.h'])
        self.hi1dir_hi1_c_builder_ = self.package_.rootbuilder().find_entry_builder(['hi1', 'hi1.c'])
        
        self.hi2dir_builder_ = self.package_.rootbuilder().find_entry_builder(['hi2'])
        self.hi2dir_hi2_h_builder_ = self.package_.rootbuilder().find_entry_builder(['hi2', 'hi2.h'])
        self.hi2dir_hi2_c_builder_ = self.package_.rootbuilder().find_entry_builder(['hi2', 'hi2.c'])

        self.highestdir_builder_ = self.package_.rootbuilder().find_entry_builder(['highest'])
        self.highestdir_highest_c_builder_ = self.package_.rootbuilder().find_entry_builder(['highest', 'highest.c'])

        self.exedir_builder_ = self.package_.rootbuilder().find_entry_builder(['exe'])
        self.exedir_main_c_builder_ = self.package_.rootbuilder().find_entry_builder(['exe', 'main.c'])

        # library and executable builder instances
        
        self.lodir_lib_builder_ = None
        self.hi1dir_lib_builder_ = None
        self.hi2dir_lib_builder_ = None
        self.highestdir_lib_builder_ = None
        self.exedir_exe_builder_ = None

        for b in self.lodir_builder_.iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertFalse(self.lodir_lib_builder_ is not None)
                self.lodir_lib_builder_ = b
                pass
            pass

        for b in self.hi1dir_builder_.iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertFalse(self.hi1dir_lib_builder_ is not None)
                self.hi1dir_lib_builder_ = b
                pass
            pass

        for b in self.hi2dir_builder_.iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertFalse(self.hi2dir_lib_builder_ is not None)
                self.hi2dir_lib_builder_ = b
                pass
            pass

        for b in self.highestdir_builder_.iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertFalse(self.highestdir_lib_builder_ is not None)
                self.highestdir_lib_builder_ = b
                pass
            pass

        for b in self.exedir_builder_.iter_builders():
            if isinstance(b, ExecutableBuilder):
                self.assertFalse(self.exedir_exe_builder_ is not None)
                self.exedir_exe_builder_ = b
                pass
            pass

        # relevant build information

        self.lodir_lib_libinfo_ = None

        for bi in self.lodir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.assertFalse(self.lodir_lib_libinfo_ is not None)
                self.lodir_lib_libinfo_ = bi
                pass
            pass
        
        self.hi1dir_lib_libinfo_ = None

        for bi in self.hi1dir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.assertFalse(self.hi1dir_lib_libinfo_ is not None)
                self.hi1dir_lib_libinfo_ = bi
                pass
            pass
        
        self.hi2dir_lib_libinfo_ = None

        for bi in self.hi2dir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.assertFalse(self.hi2dir_lib_libinfo_ is not None)
                self.hi2dir_lib_libinfo_ = bi
                pass
            pass

        self.highestdir_lib_libinfo_ = None

        for bi in self.highestdir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.assertFalse(self.highestdir_lib_libinfo_ is not None)
                self.highestdir_lib_libinfo_ = bi
                pass
            pass
        
        pass
                                    
    def testGraph(self):
        self.assertTrue(self.lodir_builder_ in self.package_.digraph().successors(self.hi1dir_builder_))
        self.assertTrue(self.lodir_builder_ in self.package_.digraph().successors(self.hi2dir_builder_))
        self.assertTrue(self.hi1dir_builder_ in self.package_.digraph().successors(self.highestdir_builder_))
        self.assertTrue(self.hi2dir_builder_ in self.package_.digraph().successors(self.highestdir_builder_))
        self.assertTrue(self.hi1dir_builder_ in self.package_.digraph().successors(self.exedir_builder_))
        self.assertTrue(self.hi2dir_builder_ in self.package_.digraph().successors(self.exedir_builder_))
        pass

    def testLocalBuildInfo(self):
        # see if everyone who is involved in the game has the right
        # buildinfo.

        for bi in self.lodir_builder_.find_entry_builder(['lo.h']).iter_buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.lodir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.hi1dir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.hi1dir_builder_.find_entry_builder(['hi1.h']).iter_buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.hi2dir_lib_builder_.iter_buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                hi2_lib = bi
                continue
            pass

        for bi in self.hi2dir_builder_.find_entry_builder(['hi2.h']).iter_buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def testPropagatedLibraryInfo(self):

        # hi1 depends on lo
        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.hi1dir_lib_builder_.direct_libraries()))
        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.hi1dir_lib_builder_.topo_libraries()))
        self.assertEqual(len(self.hi1dir_lib_builder_.topo_libraries()), 1)
        self.assertEqual(len(self.hi1dir_lib_builder_.direct_libraries()), 1)

        # hi2 depends on lo
        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.hi2dir_lib_builder_.direct_libraries()))
        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.hi2dir_lib_builder_.topo_libraries()))
        self.assertEqual(len(self.hi2dir_lib_builder_.topo_libraries()), 1)
        self.assertEqual(len(self.hi2dir_lib_builder_.direct_libraries()), 1)

        # highest depends on lo (indirect) and hi1, hi2 (direct)
        self.assertFalse(self.lodir_lib_libinfo_ in self.highestdir_lib_builder_.direct_libraries())
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.direct_libraries()))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.direct_libraries()))

        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.topo_libraries()))
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.topo_libraries()))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.topo_libraries()))

        self.assertEqual(len(self.highestdir_lib_builder_.topo_libraries()), 3)
        self.assertEqual(len(self.highestdir_lib_builder_.direct_libraries()), 2)

        # exe depends on lo (indirect) and hi1, hi2 (direct)
        self.assertFalse(self.lodir_lib_libinfo_.basename() in
                    (bi.basename() for bi in self.exedir_exe_builder_.direct_libraries()))
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.direct_libraries()))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.direct_libraries()))

        self.assertTrue(self.lodir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.topo_libraries()))
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.topo_libraries()))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.topo_libraries()))

        self.assertEqual(len(self.exedir_exe_builder_.topo_libraries()), 3)
        self.assertEqual(len(self.exedir_exe_builder_.direct_libraries()), 2)

        pass

    def testPropagatedIncludeInfo(self):
        # lo.c has no native includes
        self.assertFalse(len(self.lodir_lo_c_builder_.native_local_include_dirs()) > 0)

        # whereas all the others have
        self.assertTrue(len(self.hi1dir_hi1_c_builder_.native_local_include_dirs()) > 0)
        self.assertTrue(len(self.hi2dir_hi2_c_builder_.native_local_include_dirs()) > 0)
        self.assertTrue(len(self.highestdir_highest_c_builder_.native_local_include_dirs()) > 0)
        self.assertTrue(len(self.exedir_main_c_builder_.native_local_include_dirs()) > 0)
        
        pass

    def testLinkOrder(self):
        # highest
        # -------
        
        # highest depends on hi1, hi2, lo
        self.assertEqual(len(self.highestdir_lib_builder_.topo_libraries()), 3)

        # lo is the lowest in the dependency list, so it must come at the end
        self.assertEqual(self.lodir_lib_libinfo_.basename(), self.highestdir_lib_builder_.topo_libraries()[2].basename())

        # hi1 and hi2 are equal orders, so they must come either first or second
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.topo_libraries()[0:2]))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.highestdir_lib_builder_.topo_libraries()[0:2]))

        # exe
        # ---
        
        # exe depends on hi1, hi2, lo
        self.assertEqual(len(self.highestdir_lib_builder_.topo_libraries()), 3)

        # lo is the lowest in the dependency list, so it must come at the end
        self.assertEqual(self.lodir_lib_libinfo_.basename(), self.exedir_exe_builder_.topo_libraries()[2].basename())

        # hi1 and hi2 are equal orders, so they must come either first or second
        self.assertTrue(self.hi1dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.topo_libraries()[0:2]))
        self.assertTrue(self.hi2dir_lib_libinfo_.basename() in
                        (bi.basename() for bi in self.exedir_exe_builder_.topo_libraries()[0:2]))

        pass
    
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(InternalRequires))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(RelateBasic))
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

