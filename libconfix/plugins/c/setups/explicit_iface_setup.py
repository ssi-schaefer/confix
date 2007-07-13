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

from libconfix.core.machinery.setup import Setup
from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor

from libconfix.plugins.c.explicit_iface import ExplicitInterfaceProxy

class ExplicitInterface_Confix2_dir(Confix2_dir_Contributor):
    def __init__(self, use_libtool):
        Confix2_dir_Contributor.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def get_iface_proxies(self):
        return [ExplicitInterfaceProxy(object=self.parentbuilder(), use_libtool=self.__use_libtool)]
    def locally_unique_id(self):
        return str(self.__class__)
    pass

class ExplicitInterfaceSetup(Setup):
    def __init__(self, use_libtool):
        Setup.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def initial_builders(self):
        ret = super(ExplicitInterfaceSetup, self).initial_builders()
        ret.append(ExplicitInterface_Confix2_dir(use_libtool=self.__use_libtool))
        return ret
    pass
