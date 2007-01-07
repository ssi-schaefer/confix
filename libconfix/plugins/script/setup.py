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

from libconfix.core.machinery.setup import Setup
from libconfix.core.iface.pass_through import MethodPassThrough

from iface import ADD_SCRIPT_InterfaceProxy

class ScriptSetup(Setup):
    def initial_builders(self):
        ret = super(ScriptSetup, self).initial_builders()

        pass_through_builder = MethodPassThrough(id=str(self.__class__))
        proxy = ADD_SCRIPT_InterfaceProxy(object=pass_through_builder)

        ret.add_builder(pass_through_builder)
        ret.add_iface_proxy(proxy)

        return ret
    pass
