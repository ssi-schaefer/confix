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

from dirbuilder import DirectoryBuilder
from confix2_dir import Confix2_dir

from libconfix.core.machinery.builder import Builder
from libconfix.core.filesys.vfs_directory import VFSDirectory
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import os

class SubdirectoryRecognizer(Builder):
    def __init__(self):
        Builder.__init__(self)
        # remember directories that we already saw.
        self.__recognized_directories = set()
        pass

    def shortname(self):
        return 'Hierarchy.SubdirectoryRecognizer'

    def locally_unique_id(self):
        # I am supposed to be the only SubdirectoryRecognizer in any
        # given directory, so my class ensures uniqueness.
        return str(self.__class__)

    def enlarge(self):
        """
        If my parentbuilder has any subdirectories, see if they
        contain a Confix2.dir file. If any, wrap DirectoryBuilder
        objects around them and add them to the parentbuilder.
        """
        
        Builder.enlarge(self)

        errors = []
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, VFSDirectory):
                continue
            if entry in self.__recognized_directories:
                continue
            confix2_dir_file = entry.get(const.CONFIX2_DIR)
            if confix2_dir_file is None:
                continue
            if not isinstance(confix2_dir_file, VFSFile):
                errors.append(Error(os.sep.join(confix2_dir_file.relpath(self.package().rootdirectory()))+' is not a file'))
                continue

            try:
                self.__recognized_directories.add(entry)
                dirbuilder = DirectoryBuilder(directory=entry)
                dirbuilder.add_builder(Confix2_dir(file=confix2_dir_file))
                self.parentbuilder().add_builder(dirbuilder)
            except Error, e:
                errors.append(Error('Error creating directory builder for '+\
                                    os.sep.join(self.parentbuilder().directory().relpath(self.package().rootdirectory())), [e]))
                pass
            pass
        if len(errors):
            raise Error('There were errors in directory '+\
                        os.sep.join(self.parentbuilder().directory().relpath(self.package().rootdirectory())), errors)
        pass
    
    pass

