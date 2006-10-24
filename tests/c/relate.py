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
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.plugins.c.setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CIncludePath_NativeLocal, BuildInfo_CLibrary_NativeLocal

from libconfix.testutils import dirhier
from libconfix.testutils import find
from libconfix.testutils import packages

class RelateSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InternalRequires('testNoInstallPath'))
        self.addTest(RelateBasic('testGraph'))
        self.addTest(RelateBasic('testLocalBuildInfo'))
        self.addTest(RelateBasic('testPropagatedLibraryInfo'))
        self.addTest(RelateBasic('testPropagatedIncludeInfo'))
        self.addTest(RelateBasic('testPropagatedIncludeInfo'))
        self.addTest(RelateBasic('testLinkOrder'))
        pass
    pass

class InternalRequires(unittest.TestCase):
    def testNoInstallPath(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h',
                               entry=File(lines=[]))
        fs.rootdirectory().add(name='file.c',
                               entry=File(lines=['#include "file.h"']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])
        self.failUnlessEqual(len(package.rootbuilder().requires()), 0)
        pass
    pass        

class RelateBasic(unittest.TestCase):
    def setUp(self):
        fs = FileSystem(path=[''],
                        rootdirectory=packages.lo_hi1_hi2_highest_exe(name='xxx', version='1.2.3'))
        
        self.package_ = LocalPackage(rootdirectory=fs.rootdirectory(),
                                     setups=[DirectorySetup(),
                                             DefaultCSetup(short_libnames=False,
                                                    use_libtool=False)])
        self.package_.boil(external_nodes=[])

        # from here on, we collect things that we will need in the
        # test cases.

        # directory and file builder instances

        self.lodir_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['lo'])
        self.lodir_lo_h_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['lo', 'lo.h'])
        self.lodir_lo_c_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['lo', 'lo.c'])
        
        self.hi1dir_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi1'])
        self.hi1dir_hi1_h_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi1', 'hi1.h'])
        self.hi1dir_hi1_c_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi1', 'hi1.c'])
        
        self.hi2dir_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi2'])
        self.hi2dir_hi2_h_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi2', 'hi2.h'])
        self.hi2dir_hi2_c_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['hi2', 'hi2.c'])

        self.highestdir_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['highest'])
        self.highestdir_highest_c_builder_ = find.find_entrybuilder(self.package_.rootbuilder(),
                                                               ['highest', 'highest.c'])

        self.exedir_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['exe'])
        self.exedir_main_c_builder_ = find.find_entrybuilder(self.package_.rootbuilder(), ['exe', 'main.c'])

        # library and executable builder instances
        
        self.lodir_lib_builder_ = None
        self.hi1dir_lib_builder_ = None
        self.hi2dir_lib_builder_ = None
        self.highestdir_lib_builder_ = None
        self.exedir_exe_builder_ = None

        for b in self.lodir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(self.lodir_lib_builder_ is not None)
                self.lodir_lib_builder_ = b
                pass
            pass

        for b in self.hi1dir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(self.hi1dir_lib_builder_ is not None)
                self.hi1dir_lib_builder_ = b
                pass
            pass

        for b in self.hi2dir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(self.hi2dir_lib_builder_ is not None)
                self.hi2dir_lib_builder_ = b
                pass
            pass

        for b in self.highestdir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(self.highestdir_lib_builder_ is not None)
                self.highestdir_lib_builder_ = b
                pass
            pass

        for b in self.exedir_builder_.builders():
            if isinstance(b, ExecutableBuilder):
                self.failIf(self.exedir_exe_builder_ is not None)
                self.exedir_exe_builder_ = b
                pass
            pass

        # relevant build information

        self.lodir_lib_libinfo_ = None

        for bi in self.lodir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.failIf(self.lodir_lib_libinfo_ is not None)
                self.lodir_lib_libinfo_ = bi
                pass
            pass
        
        self.hi1dir_lib_libinfo_ = None

        for bi in self.hi1dir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.failIf(self.hi1dir_lib_libinfo_ is not None)
                self.hi1dir_lib_libinfo_ = bi
                pass
            pass
        
        self.hi2dir_lib_libinfo_ = None

        for bi in self.hi2dir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.failIf(self.hi2dir_lib_libinfo_ is not None)
                self.hi2dir_lib_libinfo_ = bi
                pass
            pass

        self.highestdir_lib_libinfo_ = None

        for bi in self.highestdir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                self.failIf(self.highestdir_lib_libinfo_ is not None)
                self.highestdir_lib_libinfo_ = bi
                pass
            pass
        
        pass
                                    
    def testGraph(self):
        self.failUnless(self.lodir_builder_ in self.package_.digraph().successors(self.hi1dir_builder_))
        self.failUnless(self.lodir_builder_ in self.package_.digraph().successors(self.hi2dir_builder_))
        self.failUnless(self.hi1dir_builder_ in self.package_.digraph().successors(self.highestdir_builder_))
        self.failUnless(self.hi2dir_builder_ in self.package_.digraph().successors(self.highestdir_builder_))
        self.failUnless(self.hi1dir_builder_ in self.package_.digraph().successors(self.exedir_builder_))
        self.failUnless(self.hi2dir_builder_ in self.package_.digraph().successors(self.exedir_builder_))
        pass

    def testLocalBuildInfo(self):
        # see if everyone who is involved in the game has the right
        # buildinfo.

        for bi in find.find_default_installer(rootbuilder=self.lodir_builder_, path=[]).buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.lodir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.hi1dir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in find.find_default_installer(rootbuilder=self.hi1dir_builder_, path=[]).buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        
        for bi in self.hi2dir_lib_builder_.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                hi2_lib = bi
                continue
            pass

        for bi in find.find_default_installer(rootbuilder=self.hi2dir_builder_, path=[]).buildinfos():
            if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def testPropagatedLibraryInfo(self):

        # hi1 depends on lo
        self.failUnless(self.lodir_lib_libinfo_ in self.hi1dir_lib_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.lodir_lib_libinfo_ in self.hi1dir_lib_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnlessEqual(len(self.hi1dir_lib_builder_.buildinfo_topo_dependent_native_libs()), 1)
        self.failUnlessEqual(len(self.hi1dir_lib_builder_.buildinfo_direct_dependent_native_libs()), 1)

        # hi2 depends on lo
        self.failUnless(self.lodir_lib_libinfo_ in self.hi2dir_lib_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.lodir_lib_libinfo_ in self.hi2dir_lib_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnlessEqual(len(self.hi2dir_lib_builder_.buildinfo_topo_dependent_native_libs()), 1)
        self.failUnlessEqual(len(self.hi2dir_lib_builder_.buildinfo_direct_dependent_native_libs()), 1)

        # highest depends on lo (indirect) and hi1, hi2 (direct)
        self.failIf(self.lodir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.hi1dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.hi2dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_direct_dependent_native_libs())

        self.failUnless(self.lodir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnless(self.hi1dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnless(self.hi2dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs())

        self.failUnlessEqual(len(self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()), 3)
        self.failUnlessEqual(len(self.highestdir_lib_builder_.buildinfo_direct_dependent_native_libs()), 2)

        # exe depends on lo (indirect) and hi1, hi2 (direct)
        self.failIf(self.lodir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.hi1dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_direct_dependent_native_libs())
        self.failUnless(self.hi2dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_direct_dependent_native_libs())

        self.failUnless(self.lodir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnless(self.hi1dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs())
        self.failUnless(self.hi2dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs())

        self.failUnlessEqual(len(self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs()), 3)
        self.failUnlessEqual(len(self.exedir_exe_builder_.buildinfo_direct_dependent_native_libs()), 2)

        pass

    def testPropagatedIncludeInfo(self):
        # lo.c has no native includes
        self.failIf(self.lodir_lo_c_builder_.buildinfo_includepath_native_local())

        # whereas all the others have
        self.failUnless(self.hi1dir_hi1_c_builder_.buildinfo_includepath_native_local())
        self.failUnless(self.hi2dir_hi2_c_builder_.buildinfo_includepath_native_local())
        self.failUnless(self.highestdir_highest_c_builder_.buildinfo_includepath_native_local())
        self.failUnless(self.exedir_main_c_builder_.buildinfo_includepath_native_local())
        
        pass
    
    def testPropagatedIncludeInfo(self):
        # highest depends on hi1, hi2, lo
        self.failUnless(self.highestdir_highest_c_builder_.buildinfo_includepath_native_local() == 3)
        pass

    def testLinkOrder(self):
        # highest
        # -------
        
        # highest depends on hi1, hi2, lo
        self.failUnlessEqual(len(self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()), 3)

        # lo is the lowest in the dependency list, so it must come at the end
        self.failUnless(self.lodir_lib_libinfo_ is self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()[2])

        # hi1 and hi2 are equal orders, so they must come either first or second
        self.failUnless(self.hi1dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()[0:2])
        self.failUnless(self.hi2dir_lib_libinfo_ in self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()[0:2])

        # exe
        # ---
        
        # exe depends on hi1, hi2, lo
        self.failUnlessEqual(len(self.highestdir_lib_builder_.buildinfo_topo_dependent_native_libs()), 3)

        # lo is the lowest in the dependency list, so it must come at the end
        self.failUnless(self.lodir_lib_libinfo_ is self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs()[2])

        # hi1 and hi2 are equal orders, so they must come either first or second
        self.failUnless(self.hi1dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs()[0:2])
        self.failUnless(self.hi2dir_lib_libinfo_ in self.exedir_exe_builder_.buildinfo_topo_dependent_native_libs()[0:2])

        pass
    
    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(RelateSuite())
    pass
