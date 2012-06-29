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

""" These tests assert fundamental behavior: relating the
nodes. Unfortunately, the tests are tied together with the C plugin -
they should have been written using core objects. (The excuse is that
C was long considered to be core)."""


from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.testutils import dirhier

import unittest

class InterPackageRelate(unittest.TestCase):
    def test(self):
        # boil and install lo
        if True:
            losource = Directory()
            losource.add(name=const.CONFIX2_PKG,
                         entry=File(lines=['PACKAGE_NAME("lo")',
                                           'PACKAGE_VERSION("6.6.6")']))
            losource.add(name=const.CONFIX2_DIR,
                         entry=File(lines=['LIBRARY(members=[H(filename="lo.h"), C(filename="lo.c")])']))
            
            losource.add(name='lo.h', entry=File())
            losource.add(name='lo.c', entry=File())
            local_lopkg = LocalPackage(rootdirectory=losource,
                                       setups=[ExplicitDirectorySetup(), ExplicitCSetup()])
            local_lopkg.boil(external_nodes=[])
            installed_lopkg = local_lopkg.install()
            pass
        
        # boil hi, referencing things from lo.
        if True:
            hisource = Directory()
            hisource.add(name=const.CONFIX2_PKG,
                         entry=File(lines=['PACKAGE_NAME("hi")',
                                           'PACKAGE_VERSION("0.0.1")']))
            hisource.add(name=const.CONFIX2_DIR,
                         entry=File(lines=['LIBRARY(members=[C(filename="hi.c")])']))
            
            hisource.add(name='hi.c',
                         entry=File(lines=['#include <lo.h>']))
            local_hipkg = LocalPackage(rootdirectory=hisource,
                                       setups=[ExplicitDirectorySetup(), ExplicitCSetup()])
            local_hipkg.boil(external_nodes=installed_lopkg.nodes())
            pass

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

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(InterPackageRelate))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
        
