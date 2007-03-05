# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from basic.suite_build import BasicTestSuiteBuild
from c.suite_build import CTestSuiteBuild
from plainfile.suite_build import PlainFileSuiteBuild
from make.suite_build import MakeSuiteBuild
from libconfix.tests.suite_build import LibConfixBuildSuite

if __name__ == '__main__':

    suite = unittest.TestSuite()

    suite.addTest(LibConfixBuildSuite())
    suite.addTest(BasicTestSuiteBuild())
    suite.addTest(CTestSuiteBuild())
    suite.addTest(PlainFileSuiteBuild())
    suite.addTest(MakeSuiteBuild())

    runner = unittest.TextTestRunner()
    runner.run(suite)
    pass
