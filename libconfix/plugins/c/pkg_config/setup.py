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

from adapter import PkgConfigLibraryAdapter

from libconfix.core.utils.error import Error
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.setup import Setup
from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor

class PkgConfigInterface_Confix2_dir(Confix2_dir_Contributor):

    class PKG_CONFIG_LIBRARY(InterfaceProxy):
        def __init__(self, object):
            InterfaceProxy.__init__(self, object)
            self.add_global('PKG_CONFIG_LIBRARY', getattr(self, 'PKG_CONFIG_LIBRARY'))
            pass
        def PKG_CONFIG_LIBRARY(self, packagename):
            if type(packagename) is not str:
                raise Error("PKG_CONFIG_LIBRARY(): argument 'packagename' must be a string")
            self.object().add_pkgconfig_library(packagename)
            pass
        def locally_unique_id(self):
            return str(self.__class__.__name__)
        pass

    def get_iface_proxies(self):
        return [self.PKG_CONFIG_LIBRARY(object=self)]
    def add_pkgconfig_library(self, packagename):
        self.parentbuilder().add_builder(PkgConfigLibraryAdapter(packagename=packagename))
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    pass

class PkgConfigSetup(Setup):
    def initial_builders(self):
        ret = super(PkgConfigSetup, self).initial_builders()
        ret.append((PkgConfigInterface_Confix2_dir()))
        return ret
    pass
