# Copyright (C) 2006-2013 Joerg Faschingbauer

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

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from .source import source_tree

import unittest

class PathsInMemoryTest(unittest.TestCase):
    def test(self):
        source = source_tree(testname=self.__class__.__name__)
        lo_dir = source.get('lo')
        hi_dir = source.get('hi')

        lo_pkg = LocalPackage(rootdirectory=lo_dir, setups=[ConfixSetup(use_libtool=False)])
        lo_pkg.boil(external_nodes=[])
        lo_pkg_inst = lo_pkg.install()

        hi_pkg = LocalPackage(rootdirectory=hi_dir, setups=[ConfixSetup(use_libtool=False)])
        hi_pkg.boil(external_nodes=lo_pkg_inst.nodes())
        hi_pkg.output()

        hi_pkg_rootdir_output_builder = find_automake_output_builder(hi_pkg.rootbuilder())
        self.assertFalse(hi_pkg_rootdir_output_builder is None)
        makefile_am = hi_pkg_rootdir_output_builder.makefile_am()
        self.assertTrue('$(readonly_prefixes_incpath)' in makefile_am.includepath())
        print() 
        hi_ldadd = makefile_am.compound_ldadd(self.__class__.__name__+'-hi_main')
        self.assertFalse(hi_ldadd is None)
        self.assertTrue('$(readonly_prefixes_libpath)' in hi_ldadd)
        pass
    pass        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(PathsInMemoryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
