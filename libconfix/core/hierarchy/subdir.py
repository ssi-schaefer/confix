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

from libconfix.core.machinery.builder import Builder
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

from dirbuilder import DirectoryBuilder
from confix2_dir import Confix2_dir

class SubdirectoryRecognizer(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__recognized_directories = set()
        pass

    def shortname(self):
        return 'Hierarchy.SubdirectoryRecognizer'

    def locally_unique_id(self):
        # I am supposed to be the only SubdirectoryRecognizer in any
        # given directory, so my class ensures uniqueness.
        return str(self.__class__)

    def enlarge(self):
        Builder.enlarge(self)

        errors = []
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, Directory):
                continue
            if entry in self.__recognized_directories:
                continue
            confix2_dir_file = entry.get(const.CONFIX2_DIR)
            if confix2_dir_file is None:
                continue
            if not isinstance(confix2_dir_file, File):
                errors.append(Error(confix2_dir_file.relpath()+' is not a file'))
                continue
            try:
                confix2_dir = Confix2_dir(file=confix2_dir_file)
                dirbuilder = DirectoryBuilder(directory=entry, configurator=confix2_dir)
                dirbuilder.add_builder(confix2_dir)
                self.parentbuilder().add_builder(dirbuilder)
                for setup in self.package().setups():
                    setup.setup_directory(directory_builder=dirbuilder)
                    pass
                self.__recognized_directories.add(entry)
            except Error, e:
                errors.append(Error('Error executing '+os.sep.join(confix2_dir_file.relpath()), [e]))
                pass
            pass
        if len(errors):
            raise Error('There were errors in directory '+\
                        os.sep.join(self.parentbuilder().directory().relpath()), errors)
        pass
    
    pass

