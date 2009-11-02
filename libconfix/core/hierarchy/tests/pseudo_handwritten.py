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

from libconfix.setups.boilerplate import Boilerplate

from libconfix.core.hierarchy import pseudo_handwritten

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils import helper_pickle

import unittest
import sys

class PseudoHandwrittenSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        sys.stderr.write('PseudoHandwritten not working\n')
        self.addTest(PseudoHandwritten('test'))
        pass
    pass

class PseudoHandwritten(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('PseudoHandwritten')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        package1 = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[Boilerplate()])
        pseudo_output_builder1 = pseudo_handwritten.find_pseudo_handwritten_builder(package1.rootbuilder())
        file1 = pseudo_output_builder1.create_file('file1')
        file1.add_lines(['line1'])

        package1.boil(external_nodes=[])
        package1.output()

        self.failUnless(fs.rootdirectory().get(pseudo_handwritten.PseudoHandWrittenFileManager.PSEUDO_HANDWRITTEN_LIST_FILENAME))
        self.failUnless(fs.rootdirectory().get('file1').lines() == ['line1'])

        package1 = None

        package2 = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[Boilerplate()])

        pseudo_output_builder2 = pseudo_handwritten.find_pseudo_handwritten_builder(package2.rootbuilder())
        file2 = pseudo_output_builder2.create_file('file2')
        file2.add_lines(['line2'])
        package2.boil(external_nodes=[])
        package2.output()

        self.failUnless(fs.rootdirectory().get(pseudo_handwritten.PseudoHandWrittenFileManager.PSEUDO_HANDWRITTEN_LIST_FILENAME))

        # note that we ought to remove the file, but we can only
        # truncate it.

        #self.failIf(fs.rootdirectory().get('file1'))
        self.failUnless(len(fs.rootdirectory().get('file1').lines()) == 0)

        self.failUnless(fs.rootdirectory().get('file2').lines() == ['line2'])

        package2 = None

        package3 = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[Boilerplate()])
        package3.boil(external_nodes=[])
        package3.output()

        # note that we ought to remove the file, but we can only
        # truncate it.

        #self.failIf(fs.rootdirectory().get(pseudo_handwritten.PseudoHandWrittenFileManager.PSEUDO_HANDWRITTEN_LIST_FILENAME))

        self.failUnless(len(helper_pickle.load_object_from_lines(
            fs.rootdirectory().get(
                pseudo_handwritten.PseudoHandWrittenFileManager.PSEUDO_HANDWRITTEN_LIST_FILENAME).lines())) == 0)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(PseudoHandwrittenSuite())
    pass

