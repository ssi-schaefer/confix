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

from libconfix.plugins.c.explicit_iface import ExplicitInterfaceProxy
from libconfix.core.iface.pass_through import MethodPassThrough

class ExplicitInterfaceSetup(Setup):
    def __init__(self, use_libtool):
        Setup.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def initial_builders(self):
        ret = super(ExplicitInterfaceSetup, self).initial_builders()
        pass_through_builder = MethodPassThrough(id=str(self.__class__))
        ret.add_builder(pass_through_builder)
        ret.add_iface_proxy(ExplicitInterfaceProxy(object=pass_through_builder,
                                                   use_libtool=self.__use_libtool))
        return ret
    pass
