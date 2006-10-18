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

from basic.suite import BasicTestSuite
from c.suite_inmem import CTestSuiteInMemory
from plainfile.suite_inmem import PlainFileSuiteInMemory
from script.suite_inmem import ScriptSuiteInMemory
from idl.suite_inmem import IDLSuiteInMemory

if __name__ == '__main__':

    suite = unittest.TestSuite()

    suite.addTest(BasicTestSuite())
    suite.addTest(CTestSuiteInMemory())
    suite.addTest(PlainFileSuiteInMemory())
    suite.addTest(ScriptSuiteInMemory())
    suite.addTest(IDLSuiteInMemory())

    runner = unittest.TextTestRunner()
    runner.run(suite)
    pass
