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

from master import Master

from libconfix.core.utils.error import Error
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor

class Relocator_Confix2_dir(Confix2_dir_Contributor):
    class RelocatorInterfaceProxy(InterfaceProxy):
        def __init__(self, object):
            assert isinstance(object, DirectoryBuilder)
            InterfaceProxy.__init__(self, object)
            self.add_global('RELOCATE_HEADER', getattr(self, 'RELOCATE_HEADER'))
            pass
        def RELOCATE_HEADER(self, filename, directory):
            if not type(filename) is str:
                raise Error('RELOCATE_HEADER(): filename parameter must be a string')
            if not type(directory) in (list, tuple):
                raise Error('RELOCATE_HEADER(): directory parameter must be list or tuple')
            self.object().add_builder(
                Master(filename, directory))
            pass
        pass

    def get_iface_proxies(self):
        return [self.RelocatorInterfaceProxy(object=self.parentbuilder())]

    def locally_unique_id(self):
        return str(self.__class__)


    pass
