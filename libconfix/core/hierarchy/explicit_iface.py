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
from confix2_dir_contributor import Confix2_dir_Contributor

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

class Confix2_dir_ExplicitInterface(Confix2_dir_Contributor):

    class DIRECTORY(InterfaceProxy):
        def __init__(self, object):
            InterfaceProxy.__init__(self, object)
            self.add_global('DIRECTORY', getattr(self, 'DIRECTORY'))
            pass
        def DIRECTORY(self, path):
            if type(path) not in (list, tuple):
                raise Error('DIRECTORY('+str(path)+'): path argument must be list or tuple')
            self.object().add_directory(path)
            pass
        pass

    def __init__(self):
        Confix2_dir_Contributor.__init__(self)
        
        # builders that are waiting to be added to our directory in
        # enlarge()
        self.__retained_builders = []
        pass

    def get_iface_proxies(self):
        return [self.DIRECTORY(object=self)]

    def add_directory(self, path):
        directory = self.parentbuilder().directory().find(path=path)
        if directory is None:
            raise Error('DIRECTORY(): could not find directory '+str(path))
        dirbuilder = DirectoryBuilder(directory=directory)

        # initialize directory builder from the package's
        # setup. if we have a Confix2.dir file, then tell him
        # about the interface the setup wants it to have, and add
        # him to the directory builder. finally, add the directory
        # builder to his future parent.

        confix2_dir_builder = None
        confix2_dir_file = directory.get(const.CONFIX2_DIR)
        if confix2_dir_file is not None:
            dirbuilder.add_builder(Confix2_dir(file=confix2_dir_file))
            pass

        self.__retained_builders.append(dirbuilder)
        self.force_enlarge()
        return dirbuilder

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def enlarge(self):
        super(Confix2_dir_Contributor, self).enlarge()
        if len(self.__retained_builders):
            self.parentbuilder().add_builders(self.__retained_builders)
            self.__retained_builders = []
            pass
        pass        
    pass
