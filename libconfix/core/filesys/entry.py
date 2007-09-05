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

class DirectoryEntry:

    def __init__(self, mode):
        self.mode_ = mode
        self.properties_ = {}
        self.parent_ = None
        self.filesystem_ = None
        pass

    def mode(self):
        return self.mode_

    def parent(self):
        return self.parent_

    def set_parent(self, parent):
        assert self.parent_ is None
        self.parent_ = parent
        pass

    def filesystem(self):
        return self.filesystem_

    def set_filesystem(self, filesystem):
        assert 0, 'abstract'
        pass

    def name(self):
        assert self.parent_ is not None, 'not yet mounted'
        return self.parent_.entryname(self)

    def abspath(self):
        if self.filesystem_ is None:
            return []
        if self.parent_ is None:
            return self.filesystem_.path()
        return self.parent_.abspath() + [self.parent_.entryname(self)]

    def relpath(self, dir):
        """
        Returns the relative path to self as seen from dir
        """
        if dir is self:
            return []
        if self.parent_ is None:
            return []
        return self.parent_.relpath(dir) + [self.parent_.entryname(self)]

    def set_property(self, name, value):
        self.properties_[name] = value
        pass

    def get_property(self, name):
        return self.properties_.get(name)

    def del_property(self, name):
        del self.properties_[name]
        pass

    def sync(self):
        assert 0, 'abstract'
        pass

    pass
