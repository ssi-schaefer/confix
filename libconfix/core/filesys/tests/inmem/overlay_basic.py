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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.overlay_filesys import OverlayFileSystem
from libconfix.core.filesys.overlay_file import OverlayFile
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.filesys.vfs_directory import VFSDirectory
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import os

class OverlayBasicTest(PersistentTestCase):
    """
    Derived tests cover a handful of facets of overlaying - sync
    issues, adding, etc.

    They all use as a basis the following layout,

    first                     self.first()
    |-- first_file            self.first_first_file()
    `-- subdir                self.first_subdir()
        `-- first_file        self.first_subdir_first_file()
    
    second                    self.second()
    |-- second_file           self.second_second_file()
    `-- subdir                self.second_subdir()
        `-- second_file       self.second_subdir_second_file()
    """
    def setUp(self):
        super(OverlayBasicTest, self).setUp()
        
        self.__first = FileSystem(path=self.rootpath()+['first'])
        self.__first_first_file = self.__first.rootdirectory().add(
            name='first_file',
            entry=File())
        self.__first_subdir = self.__first.rootdirectory().add(
            name='subdir',
            entry=Directory())
        self.__first_subdir_first_file = self.__first_subdir.add(
            name='first_file',
            entry=File())
        
        self.__second = FileSystem(path=self.rootpath()+['second'])
        self.__second_second_file = self.__second.rootdirectory().add(
            name='second_file',
            entry=File())
        self.__second_subdir = self.__second.rootdirectory().add(
            name='subdir',
            entry=Directory())
        self.__second_subdir_second_file = self.__second_subdir.add(
            name='second_file',
            entry=File())
        pass

    def first(self): return self.__first
    def first_first_file(self): return self.__first_first_file
    def first_subdir(self): return self.__first_subdir
    def first_subdir_first_file(self): return self.__first_subdir_first_file

    def second(self): return self.__second
    def second_second_file(self): return self.__second_second_file
    def second_subdir(self): return self.__second_subdir
    def second_subdir_second_file(self): return self.__second_subdir_second_file

    def test__basic(self):

        # (this one doesn't use anything from the base, it's just
        # there)

        # The following tree contains two directories, original and
        # overlay, where overlay is supposed to be 'overlayed' over
        # original. That is, the union of both directories contains
        # ... yes ... what one would expect.

        # .
        # |-- original
        # |   `-- root
        # |       `-- d10
        # |           |-- d20
        # |           `-- f0
        # `-- overlayed
        #     `-- root
        #         |-- d10
        #         |   |-- d20
        #         |   `-- f1
        #         `-- d11
        
        original = FileSystem(path=['dont', 'care', 'original'])
        original_d10 = original.rootdirectory().add(
            name='d10',
            entry=Directory())
        original_d10.add(
            name='f0',
            entry=File())
        original_d20 = original_d10.add(
            name='d20',
            entry=Directory())

        overlay = FileSystem(path=['dont', 'care', 'overlay'])
        overlay_d10 = overlay.rootdirectory().add(
            name='d10',
            entry=Directory())
        overlay_d10.add(
            name="f1",
            entry=File())
        overlay_d10.add(
            name='d20',
            entry=Directory())
        overlay.rootdirectory().add(
            name='d11',
            entry=Directory())

        union = OverlayFileSystem(original=original, overlay=overlay)

        # root has d10 from original and d11 from overlay
        self.failUnless(len([e for e in union.rootdirectory().entries()]) == 2)
        union_d10 = union.rootdirectory().find(['d10'])
        union_d11 = union.rootdirectory().find(['d11'])
        self.failIf(union_d10 is None)
        self.failIf(union_d11 is None)

        # d10 has d20 and f0 from first and f1 from second. we search
        # these using three different ways: using the directory
        # union_d10 directly (get() and find()), and using the root
        # directory (the "absolute path", so to say)
        self.failUnless(len([ e for e in union_d10.entries()]) == 3)

        found_f0_0 = union_d10.find(['f0'])
        found_f0_1 = union_d10.get('f0')
        found_f0_2 = union.rootdirectory().find(['d10', 'f0'])
        self.failIf(found_f0_0 is None)
        self.failIf(found_f0_1 is None)
        self.failIf(found_f0_2 is None)
        self.failUnless(isinstance(found_f0_0, VFSFile))
        self.failUnless(found_f0_0 is found_f0_1 is found_f0_2) 

        found_f1_0 = union_d10.find(['f1'])
        found_f1_1 = union_d10.get('f1')
        found_f1_2 = union.rootdirectory().find(['d10', 'f1'])
        self.failIf(found_f1_0 is None)
        self.failIf(found_f1_1 is None)
        self.failIf(found_f1_2 is None)
        self.failUnless(isinstance(found_f1_0, VFSFile))
        self.failUnless(found_f1_0 is found_f1_1 is found_f1_2)

        found_d20_0 = union_d10.find(['d20'])
        found_d20_1 = union_d10.get('d20')
        found_d20_2 = union.rootdirectory().find(['d10', 'd20'])
        self.failIf(found_d20_0 is None)
        self.failIf(found_d20_1 is None)
        self.failIf(found_d20_2 is None)
        self.failUnless(isinstance(found_d20_0, VFSDirectory))
        self.failUnless(found_d20_0 is found_d20_1 is found_d20_2)

        pass

    def test__sync_1(self):

        # all write access goes to first, and so does sync

        union = OverlayFileSystem(original=self.first(), overlay=self.second())
        union.sync()

        self.failUnless(os.path.exists(os.sep.join(self.first_first_file().abspath())))
        self.failUnless(os.path.exists(os.sep.join(self.first_subdir().abspath())))
        self.failUnless(os.path.exists(os.sep.join(self.first_subdir_first_file().abspath())))

        self.failIf(os.path.exists(os.sep.join(self.second_second_file().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second_subdir().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second_subdir_second_file().abspath())))

        pass

    def test__add_file(self):

        # adding a file to a unioned directory always goes to the
        # first, and not to the second.

        union = OverlayFileSystem(original=self.first(), overlay=self.second())
        union.rootdirectory().add(
            name='added_file',
            entry=File())

        # the unioned filesystem must have it at the appropriate
        # place.
        self.failUnless(union.rootdirectory().get('added_file'))
        # the first fs must have received it through the union.
        self.failUnless(self.first().rootdirectory().get('added_file'))
        # the second is read only.
        self.failIf(self.second().rootdirectory().get('added_file'))

        pass

    def test__add_directory(self):
        union = OverlayFileSystem(original=self.first(), overlay=self.second())

        # like file addition above, a directory addition must show up
        # in union and first, but not on second.
        union_newdir = union.rootdirectory().add(
            name='newdir',
            entry=Directory())
        first_newdir = self.first().rootdirectory().get('newdir')
        self.failUnless(first_newdir)
        self.failIf(self.second().rootdirectory().get('newdir'))

        # file and directory addition to union_newdir must show up in
        # but union_newdir and first_newdir (and cannot show up in
        # second_newdir because by definition that doesn't exist :-).
        union_newdir_dir = union_newdir.add(
            name='dir',
            entry=File())
        union_newdir_file = union_newdir.add(
            name='file',
            entry=Directory())
        self.failUnless(union_newdir.get('dir'))
        self.failUnless(union_newdir.get('file'))
        self.failUnless(first_newdir.get('dir'))
        self.failUnless(first_newdir.get('file'))
        pass

    def test__sync_2(self):
        union = OverlayFileSystem(original=self.first(), overlay=self.second())

        # sync the union; first is synced, and second is not.
        union.sync()
        self.failUnless(os.path.exists(os.sep.join(self.first().rootdirectory().abspath())))
        self.failUnless(os.path.exists(os.sep.join(self.first_first_file().abspath())))
        self.failUnless(os.path.exists(os.sep.join(self.first_subdir().abspath())))
        self.failUnless(os.path.exists(os.sep.join(self.first_subdir_first_file().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second().rootdirectory().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second_second_file().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second_subdir().abspath())))
        self.failIf(os.path.exists(os.sep.join(self.second_subdir_second_file().abspath())))

        # add file and dir here and there, sync and check again.
        union.rootdirectory().add(
            name='newfile',
            entry=File())
        newdir = union.rootdirectory().add(
            name='newdir',
            entry=Directory())
        newdir.add(
            name='newfile',
            entry=File())

        union.sync()

        self.failUnless(os.path.exists(os.sep.join(self.first().rootdirectory().abspath()+['newfile'])))
        self.failUnless(os.path.exists(os.sep.join(self.first().rootdirectory().abspath()+['newdir'])))
        self.failUnless(os.path.exists(os.sep.join(self.first().rootdirectory().abspath()+['newdir', 'newfile'])))
        self.failIf(os.path.exists(os.sep.join(self.second().rootdirectory().abspath()+['newfile'])))
        self.failIf(os.path.exists(os.sep.join(self.second().rootdirectory().abspath()+['newdir'])))
        self.failIf(os.path.exists(os.sep.join(self.second().rootdirectory().abspath()+['newdir', 'newfile'])))
        pass

    def test__abspath(self):
        union = OverlayFileSystem(original=self.first(), overlay=self.second())

        # the path of the union filesystem itself is the first.

        self.failUnlessEqual(union.path(), self.first().path())

        # the abspath of the entries is that of their respective
        # locations. files cannot exist in both filesystems, thus file
        # unions have their respective file locationin the underlying
        # filessystems. union directories have their first path if
        # they exist in both. if they exist in only one filesystem,
        # ... blah.

        # <entries of first>
        union_first_file = union.rootdirectory().find(['first_file'])
        self.failIf(union_first_file is None)
        self.failUnlessEqual(self.first_first_file().abspath(), union_first_file.abspath())

        union_subdir = union.rootdirectory().find(['subdir'])
        self.failIf(union_subdir is None)
        self.failUnlessEqual(self.first_subdir().abspath(), union_subdir.abspath())

        union_subdir_first_file = union.rootdirectory().find(['subdir', 'first_file'])
        self.failIf(union_subdir_first_file is None)
        self.failUnlessEqual(self.first_subdir_first_file().abspath(), union_subdir_first_file.abspath())
        # </entries of first>

        # <entries of second>
        union_second_file = union.rootdirectory().find(['second_file'])
        self.failIf(union_second_file is None)
        self.failUnlessEqual(self.second_second_file().abspath(), union_second_file.abspath())

        union_subdir_second_file = union.rootdirectory().find(['subdir', 'second_file'])
        self.failIf(union_subdir_second_file is None)
        self.failUnlessEqual(self.second_subdir_second_file().abspath(), union_subdir_second_file.abspath())
        # </entries of second>

        pass

    def test__file_truncate(self):
        union = OverlayFileSystem(original=self.first(), overlay=self.second())
        first_file = union.rootdirectory().find(['first_file'])
        second_file = union.rootdirectory().find(['second_file'])
        first_file.truncate()
        try:
            second_file.truncate()
            self.fail()
        except OverlayFile.TruncateError: pass
        pass

    def test__file_add_lines(self):
        union = OverlayFileSystem(original=self.first(), overlay=self.second())
        first_file = union.rootdirectory().find(['first_file'])
        second_file = union.rootdirectory().find(['second_file'])
        first_file.add_lines([''])
        try:
            second_file.add_lines([''])
            self.fail()
        except OverlayFile.AddLinesError: pass
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(OverlayBasicTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

