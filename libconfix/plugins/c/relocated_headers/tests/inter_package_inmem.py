# Copyright (C) 2007-2008 Joerg Faschingbauer

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

import inter_package

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class InterPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterPackageInMemoryTest('test'))
        pass
    pass

class InterPackageInMemoryTest(unittest.TestCase):
    def test(self):
        common, lo, hi = inter_package.make_source(classname=self.__class__.__name__)
        
        common_package = LocalPackage(rootdirectory=common,
                                      setups=[ConfixSetup(use_libtool=False)])
        common_package.boil(external_nodes=[])
        common_installed = common_package.install()

        lo_package = LocalPackage(rootdirectory=lo,
                                  setups=[ConfixSetup(use_libtool=False)])
        lo_package.boil(external_nodes=common_installed.nodes())
        lo_installed = lo_package.install()

        hi_package = LocalPackage(rootdirectory=hi,
                                  setups=[ConfixSetup(use_libtool=False)])
        hi_package.boil(external_nodes=common_installed.nodes() + lo_installed.nodes())

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageInMemorySuite())
    pass

