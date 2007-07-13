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

from libconfix.core.machinery.setup import Setup

from iface import ADD_PLAINFILE_Confix2_dir
from creator import PlainFileCreator

class PlainFileInterfaceSetup(Setup):
    def initial_builders(self):
        ret = super(PlainFileInterfaceSetup, self).initial_builders()
        ret.append(ADD_PLAINFILE_Confix2_dir())
        return ret
    pass

class PlainFileCreatorSetup(Setup):
    def __init__(self, regex, prefixdir=None, datadir=None):
        Setup.__init__(self)
        self.__regex = regex
        self.__prefixdir = prefixdir
        self.__datadir = datadir
        pass
    def initial_builders(self):
        ret = super(PlainFileCreatorSetup, self).initial_builders()
        ret.append(PlainFileCreator(regex=self.__regex,
                                    prefixdir=self.__prefixdir,
                                    datadir=self.__datadir))
        return ret
    pass

