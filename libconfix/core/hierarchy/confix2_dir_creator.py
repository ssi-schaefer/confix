# Copyright (C) 2008 Joerg Faschingbauer

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

from confix2_dir import Confix2_dir

from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

class Confix2_dir_Creator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__seen = False
        pass
    def locally_unique_id(self):
        # we are supposed to exist only once in a directory, so our
        # class is sufficient.
        return str(self.__class__)
    def enlarge(self):
        super(Confix2_dir_Creator, self).enlarge()
        
        if self.__seen:
            return

        for name, entry in self.parentbuilder().directory().entries():
            if name == const.CONFIX2_DIR:
                if not isinstance(entry, VFSFile):
                    raise Error('/'.join(self.parentbuilder().directory().relpath(from_dir=self.package().rootdirectory()))+
                                ': '+name+' is not a file')
                self.__seen = True
                self.parentbuilder().add_builder(Confix2_dir(file=entry))
                pass
            pass
        pass
    pass
