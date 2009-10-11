# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.filesys.file import File
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper
from libconfix.core.utils import debug

class ModulesDirectoryBuilder(DirectoryBuilder):
    def __init__(self, directory):
        DirectoryBuilder.__init__(self, directory)
        pass

    def add_module_file(self, name, lines):
        my_lines = helper.normalize_lines(lines)
        existing_file = self.directory().get(name)
        if existing_file is None:
            self.directory().add(name=name, entry=File(lines=my_lines))
        elif helper.md5_hexdigest_from_lines(my_lines) != helper.md5_hexdigest_from_lines(existing_file.lines()):
            debug.warn('Module file '+name+' already exists with different content')
            existing_file.truncate()
            existing_file.add_lines(my_lines)
            pass
        pass

    pass
