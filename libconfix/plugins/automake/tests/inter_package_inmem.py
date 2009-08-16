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

from libconfix.plugins.automake.setup import AutomakeSetup
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier

import unittest

class InterPackageInMemorySuite(unittest.TestSuite):

    """ These tests assert fundamental behavior: relating the
    nodes. Unfortunately, the tests are tied together with the C
    plugin - they should have been written using core objects. (The
    excuse is that C was long considered to be core)."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RepoInstall('test'))
        self.addTest(InterPackageRelate('test'))
        pass
    pass

class RepoInstall(unittest.TestCase):
    def test(self):
        rootdir = Directory()
        rootdir.add(name=const.CONFIX2_PKG,
                    entry=File(lines=["PACKAGE_NAME('blah')",
                                      "PACKAGE_VERSION('1.2.3')"]))
        rootdir.add(name=const.CONFIX2_DIR,
                    entry=File())

        package = LocalPackage(rootdirectory=rootdir, setups=[ExplicitDirectorySetup(), AutomakeSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)

        self.failUnless('confixrepo' in rootdir_output_builder.makefile_am().install_directories())

        pass

    pass

class InterPackageRelate(unittest.TestCase):
    def test(self):
        lofs = dirhier.packageroot(name='lo', version='1.2.3')
        lofs.rootdirectory().add(name='lo.h', entry=File())
        lofs.rootdirectory().add(name='lo.c', entry=File())
        local_lopkg = LocalPackage(rootdirectory=lofs.rootdirectory(),
                                   setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        local_lopkg.boil(external_nodes=[])
        installed_lopkg = local_lopkg.install()

        hifs = dirhier.packageroot(name='hi', version='1.2.3')
        hifs.rootdirectory().add(name='hi.c',
                                 entry=File(lines=['#include <lo.h>']))
        local_hipkg = LocalPackage(rootdirectory=hifs.rootdirectory(),
                                   setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        local_hipkg.boil(external_nodes=installed_lopkg.nodes())

        lo_h_builder = local_lopkg.rootbuilder().find_entry_builder(['lo.h'])
        lo_c_builder = local_lopkg.rootbuilder().find_entry_builder(['lo.c'])
        liblo_builder = None
        for b in local_lopkg.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                liblo_builder = b
                break
            pass
        else:
            self.fail()
            pass

        hi_c_builder = local_hipkg.rootbuilder().find_entry_builder(['hi.c'])
        libhi_builder = None
        for b in local_hipkg.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                libhi_builder = b
                break
            pass
        else:
            self.fail()
            pass

        # hi.c includes lo.h, so it must have a BuildInfo for
        # installed header files, but none for local header files.
        self.failUnless(hi_c_builder.using_native_installed() > 0)
        self.failUnless(len(hi_c_builder.native_local_include_dirs()) == 0)
        self.failUnless(len(libhi_builder.direct_libraries()) == 1)
        self.failUnless(len(libhi_builder.topo_libraries()) == 1)
        self.failUnless(isinstance(libhi_builder.direct_libraries()[0],
                                   BuildInfo_CLibrary_NativeInstalled))
        self.failUnless(isinstance(libhi_builder.topo_libraries()[0],
                                   BuildInfo_CLibrary_NativeInstalled))
        self.failUnless(libhi_builder.topo_libraries()[0] is \
                        libhi_builder.direct_libraries()[0])                        
        self.failUnless(libhi_builder.direct_libraries()[0].basename() == 'lo')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageInMemorySuite())
    pass
        
