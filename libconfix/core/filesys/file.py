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

import os

from .vfs_file import VFSFile
from .entry import Entry
from .filesys import FileSystem

from libconfix.core.utils.error import Error, NativeError
import libconfix.core.utils.helper

class FileState:
    NEW = 0
    SYNC_INMEM = 1
    SYNC_CLEAR = 2
    DIRTY = 3
    VIRTUAL = 4
    pass

class File(VFSFile, Entry):

    def __init__(self, lines=None, mode=None, state=FileState.NEW):
        Entry.__init__(self, mode=mode)
        self.__lines = lines
        self.__state = state

        if self.__state == FileState.NEW:
            if self.__lines is None:
                self.__lines = []
                pass
            pass
        elif self.__state == FileState.SYNC_INMEM:
            assert self.__lines is not None, 'SYNC_INMEM implies lines not None'
            pass
        elif self.__state == FileState.SYNC_CLEAR:
            assert self.__lines is None, 'SYNC_CLEAR implies line not None'
            pass
        elif self.__state == FileState.DIRTY:
            assert self.__lines is not None, 'DIRTY implies lines not None'
            pass
        elif self.__state == FileState.VIRTUAL:
            assert self.__lines is not None, 'VIRTUAL implies lines not None'
        else:
            assert 0
            pass
        pass

    def is_persistent(self):
        """
        (VFSEntry implementation)
        """
        if self.__state == FileState.NEW:
            return False
        if self.__state == FileState.SYNC_INMEM:
            return True
        if self.__state == FileState.SYNC_CLEAR:
            return True
        if self.__state == FileState.DIRTY:
            return True
        assert 0
        pass

    def sync(self):
        """
        (VFSEntry implementation)
        """
        assert self.filesystem() is not None

        if self.__state == FileState.NEW:
            filename = os.sep.join(self.abspath())
            try:
                libconfix.core.utils.helper.write_lines_to_file_if_changed(
                    filename=filename,
                    lines=self.__lines)
            except Error as err:
                raise Error('Could not write file '+filename, [err])
            if self.mode() is not None:
                try:
                    os.chmod(filename, self.mode())
                except OSError as err:
                    raise Error('Could not change mode of file '+filename,
                                [NativeError(err, sys.exc_info()[2])])
                pass

            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.__lines = None
                self.__state = FileState.SYNC_CLEAR
            else:
                self.__state = FileState.SYNC_INMEM
                pass
            return

        if self.__state == FileState.SYNC_CLEAR:
            return

        if self.__state == FileState.SYNC_INMEM:
            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.__lines = None
                self.__state = FileState.SYNC_CLEAR
                pass
            return

        if self.__state == FileState.DIRTY:
            filename = os.sep.join(self.abspath())
            try:
                libconfix.core.utils.helper.write_lines_to_file(
                    filename=filename,
                    lines=self.__lines)
            except Error as err:
                raise Error('Could not write file '+filename, [err])
            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.__lines = None
                self.__state = FileState.SYNC_CLEAR
            else:
                self.__state = FileState.SYNC_INMEM
                pass
            return

        if self.__state == FileState.VIRTUAL:
            return
        assert 0
        pass

    def lines(self):
        """
        (VFSFile implementation)
        """
        self.__read_lines_if_necessary()
        return self.__lines

    def add_lines(self, lines):
        """
        (VFSFile implementation)
        """
        self.__read_lines_if_necessary()
        self.__lines.extend(lines)
        if self.__state == FileState.NEW:
            return
        if self.__state == FileState.SYNC_INMEM:
            self.__state = FileState.DIRTY
            return
        if self.__state == FileState.SYNC_CLEAR:
            assert 0
            return
        if self.__state == FileState.DIRTY:
            return
        if self.__state == FileState.VIRTUAL:
            return
        assert 0
        pass

    def truncate(self):
        """
        (VFSFile implementation)
        """
        if self.__state == FileState.NEW:
            self.__lines = []
            return
        if self.__state == FileState.SYNC_INMEM:
            if self.__lines != []:
                self.__lines = []
                self.__state = FileState.DIRTY
                pass
            return
        if self.__state == FileState.SYNC_CLEAR:
            self.__lines = []
            self.__state = FileState.DIRTY
            return
        if self.__state == FileState.DIRTY:
            self.__lines = []
            return
        assert 0
        pass

    def is_overlayed(self):
        """
        (VFSFile implementation)
        """
        return False

    def state(self):
        return self.__state

    def raw_lines(self):
        """
        Bare access to self.__lines, without reading the file. Used
        for testing only, meaningless elsewhere.
        """
        return self.__lines

    def __read_lines_if_necessary(self):
        if self.__state == FileState.NEW:
            return
        if self.__state == FileState.SYNC_INMEM:
            return
        if self.__state == FileState.SYNC_CLEAR:
            self.__lines = libconfix.core.utils.helper.lines_of_file(os.sep.join(self.abspath()))
            self.__state = FileState.SYNC_INMEM
            return
        if self.__state == FileState.DIRTY:
            return
        if self.__state == FileState.VIRTUAL:
            return
        assert 0
        pass
        
        
    pass
