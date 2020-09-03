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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const

def packageroot(path=None, name=None, version=None):
    mypath = path
    myname = name
    myversion = version
    if mypath is None:
        mypath = ['a', 'b']
        pass
    if myname is None:
        myname = 'blah'
        pass
    if myversion is None:
        myversion = '6.6.6'
        pass
    fs = FileSystem(path=mypath)
    fs.rootdirectory().add(name=const.CONFIX2_PKG,
                           entry=File(lines=['PACKAGE_NAME("'+myname+'")',
                                             'PACKAGE_VERSION("'+myversion+'")']))
    fs.rootdirectory().add(name=const.CONFIX2_DIR,
                           entry=File(lines=[]))
    return fs

def subdir(parent, name):
    dir = Directory()
    dir.add(name=const.CONFIX2_DIR,
            entry=File())
    parent.add(name=name, entry=dir)
    return dir


