# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from libconfix.core.filesys import scan
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import os

class Test(PersistentTestCase):
    def test__new_file(self):
        # use a filesystem instance to conveniently create the initial
        # directory.
        fs_orig = FileSystem(self.rootpath())
        fs_orig.rootdirectory().add(
            name='file1',
            entry=File())
        fs_orig.sync()
        
        # we have synced the fs_orig, so a scan should see file1
        fs_dup = scan.scan_filesystem(self.rootpath())
        self.failUnless(fs_dup.rootdirectory().get('file1'))

        # now add a file to the directory, via fs_orig
        fs_orig.rootdirectory().add(
            name='file2',
            entry=File())
        fs_orig.sync()

        # rescan the fs_dup's rootdirectory. the file must be seen.
        scan.rescan_dir(fs_dup.rootdirectory())
        self.failUnless(fs_dup.rootdirectory().get('file2'))
        pass

    def test__new_directory(self):
        fs_orig = FileSystem(self.rootpath())
        fs_orig.sync()

        fs_dup = scan.scan_filesystem(self.rootpath())

        fs_orig.rootdirectory().add(
            name='dir',
            entry=Directory())
        fs_orig.sync()

        scan.rescan_dir(fs_dup.rootdirectory())
        self.failUnless(fs_dup.rootdirectory().get('dir'))
        pass

    def test__new_file_in_existing_directory(self):
        fs_orig = FileSystem(self.rootpath())
        orig_dir = fs_orig.rootdirectory().add(
            name='dir',
            entry=Directory())
        fs_orig.sync()

        fs_dup = scan.scan_filesystem(self.rootpath())

        orig_dir.add(
            name='file',
            entry=File())
        fs_orig.sync()

        scan.rescan_dir(fs_dup.rootdirectory())
        self.failUnless(fs_dup.rootdirectory().find(['dir', 'file']))
        pass

    def test__removed_file(self):
        # use a filesystem instance to conveniently create the initial
        # directory.
        fs = FileSystem(self.rootpath())
        fs.rootdirectory().add(
            name='file',
            entry=File())
        fs.sync()
        
        os.unlink(os.sep.join(self.rootpath()+['file']))

        # rescan the fs's rootdirectory. the file must have gone.
        scan.rescan_dir(fs.rootdirectory())
        self.failIf(fs.rootdirectory().get('file'))
        pass
        
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

