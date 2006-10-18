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

import os

from libconfix.core.utils.error import Error, NativeError
import libconfix.core.utils.helper

from entry import DirectoryEntry
from filesys import FileSystem

class FileState:
    NEW = 0
    SYNC_INMEM = 1
    SYNC_CLEAR = 2
    DIRTY = 3
    VIRTUAL = 4
    pass

class File(DirectoryEntry):

    def __init__(self, lines=None, mode=None, state=FileState.NEW):
        DirectoryEntry.__init__(self, mode=mode)
        self.lines_ = lines
        self.state_ = state
        self.filesystem_ = None

        if self.state_ == FileState.NEW:
            if self.lines_ is None:
                self.lines_ = []
                pass
            pass
        elif self.state_ == FileState.SYNC_INMEM:
            assert self.lines_ is not None, 'SYNC_INMEM implies lines not None'
            pass
        elif self.state_ == FileState.SYNC_CLEAR:
            assert self.lines_ is None, 'SYNC_CLEAR implies line not None'
            pass
        elif self.state_ == FileState.DIRTY:
            assert self.lines_ is not None, 'DIRTY implies lines not None'
            pass
        elif self.state_ == FileState.VIRTUAL:
            assert self.lines_ is not None, 'VIRTUAL implies lines not None'
        else:
            assert 0
            pass
        pass

    def state(self):
        return self.state_

    def is_persistent(self):
        if self.state_ == FileState.NEW:
            return False
        if self.state_ == FileState.SYNC_INMEM:
            return True
        if self.state_ == FileState.SYNC_CLEAR:
            return True
        if self.state_ == FileState.DIRTY:
            return True
        assert 0
        pass

    def lines(self):
        self.read_lines_if_necessary_()
        return self.lines_

    def add_lines(self, lines):
        self.read_lines_if_necessary_()
        self.lines_.extend(lines)
        if self.state_ == FileState.NEW:
            return
        if self.state_ == FileState.SYNC_INMEM:
            self.state_ = FileState.DIRTY
            return
        if self.state_ == FileState.SYNC_CLEAR:
            assert 0
            return
        if self.state_ == FileState.DIRTY:
            return
        if self.state_ == FileState.VIRTUAL:
            return
        assert 0
        pass

    def add_line(self, line):
        self.add_lines([line])
        pass

    def set_filesystem(self, filesystem):
        assert filesystem is not None
        assert self.filesystem_ is None
        self.filesystem_ = filesystem
        pass
        
    def sync(self):
        assert self.filesystem() is not None

        if self.state_ == FileState.NEW:
            filename = os.sep.join(self.abspath())
            try:
                libconfix.core.utils.helper.write_lines_to_file_if_changed(
                    filename=filename,
                    lines=self.lines_)
            except Error, err:
                raise Error('Could not write file '+filename, [err])
            if self.mode_ is not None:
                try:
                    os.chmod(filename, self.mode_)
                except OSError, err:
                    raise Error('Could not change mode of file '+filename,
                                [NativeError(err, sys.exc_traceback)])
                pass

            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.lines_ = None
                self.state_ = FileState.SYNC_CLEAR
            else:
                self.state_ = FileState.SYNC_INMEM
                pass
            return

        if self.state_ == FileState.SYNC_CLEAR:
            return

        if self.state_ == FileState.SYNC_INMEM:
            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.lines_ = None
                self.state_ = FileState.SYNC_CLEAR
                pass
            return

        if self.state_ == FileState.DIRTY:
            filename = os.sep.join(self.abspath())
            try:
                libconfix.core.utils.helper.write_lines_to_file(
                    filename=filename,
                    lines=self.lines_)
            except Error, err:
                raise Error('Could not write file '+filename, [err])
            if FileSystem.CLEAR_ON_SYNC in self.filesystem().flags():
                self.lines_ = None
                self.state_ = FileState.SYNC_CLEAR
            else:
                self.state_ = FileState.SYNC_INMEM
                pass
            return

        if self.state_ == FileState.VIRTUAL:
            return
        assert 0
        pass

    def truncate(self):
        if self.state_ == FileState.NEW:
            self.lines_ = []
            return
        if self.state_ == FileState.SYNC_INMEM:
            if self.lines_ != []:
                self.lines_ = []
                self.state_ = FileState.DIRTY
                pass
            return
        if self.state_ == FileState.SYNC_CLEAR:
            self.lines_ = []
            self.state_ = FileState.DIRTY
            return
        if self.state_ == FileState.DIRTY:
            self.lines_ = []
            return
        assert 0
        pass

    def read_lines_if_necessary_(self):
        if self.state_ == FileState.NEW:
            return
        if self.state_ == FileState.SYNC_INMEM:
            return
        if self.state_ == FileState.SYNC_CLEAR:
            self.lines_ = libconfix.core.utils.helper.lines_of_file(os.sep.join(self.abspath()))
            self.state_ = FileState.SYNC_INMEM
            return
        if self.state_ == FileState.DIRTY:
            return
        if self.state_ == FileState.VIRTUAL:
            return
        assert 0
        pass
        
        
    pass
