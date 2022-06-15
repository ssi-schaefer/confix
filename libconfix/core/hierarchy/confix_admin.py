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

from .dirbuilder import DirectoryBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

def add_confix_admin(package):
    """
    If necessary, add a directory <packageroot>/confix-admin and the
    associated directory builder.

    @return: DirectoryBuilder instance representing the confix-admin
             directory
    """
    admin_builder = package.rootbuilder().find_entry_builder([const.ADMIN_DIR])
    if admin_builder:
        return admin_builder
    admin_dir = package.rootdirectory().get(const.ADMIN_DIR)
    if admin_dir is None:
        admin_dir = package.rootdirectory().add(name=const.ADMIN_DIR, entry=Directory())
        pass
    return package.rootbuilder().add_builder(DirectoryBuilder(directory=admin_dir))
