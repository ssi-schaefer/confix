# Copyright (C) 2007-2009 Joerg Faschingbauer

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

import libconfix.plugins.c.relocated_headers.tests.inter_package as inter_package

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.repo import AutomakePackageRepository
from libconfix.plugins.automake import bootstrap, configure, make, helper
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import sys

class InterPackageBuildTest(PersistentTestCase):
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(InterPackageBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass


