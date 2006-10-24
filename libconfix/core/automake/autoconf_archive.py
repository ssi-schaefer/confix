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

import os

from libconfix.core.utils.error import Error
from libconfix.core.utils import external_cmd
from libconfix.core.utils import helper

def find_archive_root(argv0):
    dir = os.path.dirname(argv0)

    # accommodate for relative paths.
    if not os.path.isabs(dir):
        dir = os.path.normpath(os.path.join(os.getcwd(), dir))
        pass

    try:
        confix_root = helper.find_confix_root(dir)
    except Error, e:
        raise Error('Cannot find autoconf archive: cannot find confix installation', [e])

    autoconf_dir = os.path.join(confix_root, 'share', 'confix', 'autoconf-archive')
    if not os.path.isdir(autoconf_dir):
        raise Error(autoconf_dir+' is not a directory (Confix installation error?)')
    return autoconf_dir

def include_path(argv0):
    return os.path.join(find_archive_root(argv0), 'm4src')
