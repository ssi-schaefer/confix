# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from .vfs_entry import VFSEntry

class Entry(VFSEntry):
    def __init__(self, mode):
        VFSEntry.__init__(self)
        self.__mode = mode
        pass

    def mode(self):
        return self.__mode

    def abspath(self):
        """
        (VFSEntry implementation)
        """
        fs = self.filesystem()
        parent = self.parent()
        assert fs is not None
        if parent is None:
            return fs.path()
        return parent.abspath() + [parent.entryname(self)]

    def relpath(self, from_dir):
        """
        (VFSEntry implementation)
        """
        if from_dir is self:
            return []
        parent = self.parent()
        if parent is None:
            return []
        return parent.relpath(from_dir=from_dir) + [parent.entryname(self)]
        
    pass
