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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.installed_node import InstalledNode
from libconfix.core.machinery.installed_node import InstalledNode
from libconfix.core.machinery.installed_package import InstalledPackage
from libconfix.core.machinery.provide_symbol import Provide_Symbol
from libconfix.core.machinery.require_symbol import Require_Symbol
from libconfix.core.repo.package_file import PackageFile

class PackageFileSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(PackageFileTest('test'))
        pass
    pass

class PackageFileTest(unittest.TestCase):
    def test(self):
        package = InstalledPackage(
            name='PackageFileTestPackage',
            version='1.2.3',
            nodes=[InstalledNode(name=['a','b'],
                                 provides=[Provide_Symbol(symbol='beitl')],
                                 requires=[Require_Symbol(symbol='sack', found_in=['PackageFileTest'])],
                                 buildinfos=[])])
        fs = FileSystem(path=['', 'tmp'])
        pkgfile = fs.rootdirectory().add(name='test.repo', entry=File())

        # dump package to a file, and re-read it from that
        # file. perform placebo checks.
        repo = PackageFile(file=pkgfile)
        repo.dump(package=package)
        repo = PackageFile(file=pkgfile)
        package = repo.load()

        self.failUnless(len(package.nodes()) == 1)
        node = package.nodes()[0]
        self.failUnless(len(node.provides()) == 1)
        self.failUnless(len(node.requires()) == 1)
        self.failUnless(len(node.buildinfos()) == 0)
        
        pass
    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(PackageFileSuite())
    pass
