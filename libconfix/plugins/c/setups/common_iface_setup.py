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

from libconfix.plugins.c.common_iface import \
     EXTERNAL_LIBRARY, \
     REQUIRE_H, \
     PROVIDE_H, \
     TESTS_ENVIRONMENT

class CommonInterface_Confix2_dir(Confix2_dir_Contributor):
    def get_iface_proxies(self):
        return [EXTERNAL_LIBRARY(object=self),
                REQUIRE_H(object=self),
                PROVIDE_H(object=self),
                TESTS_ENVIRONMENT(object=self.parentbuilder())]
    def locally_unique_id(self):
        return str(self.__class__)
    pass

class CommonInterfaceSetup(Setup):
    def initial_builders(self):
        return super(CommonInterfaceSetup, self).initial_builders() + \
               [CommonInterface_Confix2_dir()]
    pass
