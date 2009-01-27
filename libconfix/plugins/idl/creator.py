# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.machinery.creator import Creator

import builder

class IDLCreator(Creator):
    def __init__(self):
        Creator.__init__(self)
        self.handled_entries_ = set()
        pass

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def shortname(self):
        return 'IDLCreator'

    def enlarge(self):
        super(Creator, self).enlarge()
        for name, entry in self.parentbuilder().directory().entries():
            if not isinstance(entry, VFSFile):
                continue
            if name in self.handled_entries_:
                continue
            if not name.endswith('.idl'):
                continue

            self.handled_entries_.add(name)
            Creator.add_candidate_builder(self, name, builder.Builder(file=entry))
            pass
        pass
    pass
