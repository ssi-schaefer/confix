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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils.error import Error

class PKG_CONFIG_LIBRARY_InterfaceProxy(InterfaceProxy, Builder):
    def __init__(self):
        InterfaceProxy.__init__(self)
        Builder.__init__(self)
        self.add_global('PKG_CONFIG_LIBRARY', getattr(self, 'PKG_CONFIG_LIBRARY'))
        pass

    def locally_unique_id(self):
        return str(self.__class__.__name__)

    def PKG_CONFIG_LIBRARY(self, packagename):
        if type(packagename) is not str:
            raise Error("PKG_CONFIG_LIBRARY(): argument 'packagename' must be a string")
        self.parentbuilder().add_builder(PkgConfigLibraryAdapter(packagename=packagename))
        pass
    pass

