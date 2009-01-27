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


from makefile_am import Makefile_am

from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.filesys.file import File
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

import os

class AutoconfAuxDirBuilder(DirectoryBuilder):
    def __init__(self, directory):
        DirectoryBuilder.__init__(self, directory=directory)
        pass

    def output(self):
        super(AutoconfAuxDirBuilder, self).output()
        self.package().configure_ac().set_ac_config_aux_dir(
            '/'.join(self.directory().relpath(self.package().rootdirectory())))
        pass

    def eat_file(self, sourcename, mode):
        basename = os.path.basename(sourcename)
        lines = helper.lines_of_file(sourcename)
        destfile = self.directory().find([basename])
        if destfile is None:
            destfile = self.directory().add(
                name=basename,
                entry=File(mode=mode, lines=lines))
        else:
            destfile.truncate()
            destfile.add_lines(lines)
            pass
        self.makefile_am().add_extra_dist(basename)
        pass

    pass

