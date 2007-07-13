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

from basic.suite_inmem import BasicTestSuiteInMemory
from c.suite_inmem import CTestSuiteInMemory

# since Jan 7, 2007 I try to keep tests as near to the code as
# possible. seems like a better way.
from libconfix.tests.suite_inmem import LibConfixInMemorySuite

if __name__ == '__main__':

    suite = unittest.TestSuite()

    suite.addTest(BasicTestSuiteInMemory())
    suite.addTest(CTestSuiteInMemory())
    suite.addTest(LibConfixInMemorySuite())

    runner = unittest.TextTestRunner()
    runner.run(suite)
    pass
