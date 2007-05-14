# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

class ExplicitInterfaceProxy(InterfaceProxy):

    """ Implements the DIRECTORY() method of a Confix2.dir file."""
    
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        assert not isinstance(object, DirectoryBuilder), 'assuming a pass-through object'
        self.__object = object
        self.add_global('DIRECTORY', getattr(self, 'DIRECTORY'))
        pass

    def DIRECTORY(self, path):
        if type(path) not in (list, tuple):
            raise Error('DIRECTORY('+str(path)+'): path argument must be list or tuple')
            
        directory = self.__object.parentbuilder().directory().find(path=path)
        if directory is None:
            raise Error('DIRECTORY(): could not find directory '+str(path))
        dirbuilder = DirectoryBuilder(directory=directory)

        # initialize directory builder from the package's setup. if we
        # have a Confix2.dir file, then tell him about the interface
        # the setup wants it to have, and add him to the directory
        # builder. finally, add the directory bilder to his future
        # parent.
        initials = self.__object.package().get_initial_builders()
        dirbuilder.add_builders(initials.builders())

        confix2_dir_file = directory.get(const.CONFIX2_DIR)
        if confix2_dir_file is not None:
            confix2_dir_builder = Confix2_dir(file=confix2_dir_file)
            confix2_dir_builder.add_iface_proxies(initials.iface_proxies())
            dirbuilder.add_builder(confix2_dir_builder)
            pass

        self.__object.parentbuilder().add_builder(dirbuilder)
        return dirbuilder

    pass
