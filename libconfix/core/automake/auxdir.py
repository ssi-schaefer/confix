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


from makefile_am import Makefile_am

from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.filesys.file import File
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

import os

class AutoconfAuxDir(DirectoryBuilder):
    def __init__(self, directory):
        DirectoryBuilder.__init__(self, directory=directory)

        mf_am = self.directory().find(['Makefile.am'])
        if mf_am:
            mf_am.truncate()
        else:
            mf_am = File()
            self.directory().add(name='Makefile.am', entry=mf_am)
            pass
        self.makefile_am_ = Makefile_am()
        pass

    def output(self):
        DirectoryBuilder.output(self)
        self.package().configure_ac().set_ac_config_aux_dir(
            '/'.join(self.directory().relpath(self.package().rootdirectory())))
        pass

    def eat_file(self, sourcename, mode):
        assert 0, 'how do we copy_file_if_changed() when we sail up in the air?'
        basename = os.path.basename(sourcename)
        helper.copy_file_if_changed(sourcename=sourcename,
                                    targetname=os.path.join(self.abspath_, basename),
                                    mode=mode)
        self.makefile_am_.add_extra_dist(basename)
        pass

    pass

