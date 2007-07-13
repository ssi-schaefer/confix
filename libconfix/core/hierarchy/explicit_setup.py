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

from explicit_iface import Confix2_dir_ExplicitInterface
from common_iface import CommonDirectoryInterface_Confix2_dir

from libconfix.core.machinery.setup import Setup

class ExplicitDirectorySetup(Setup):
    def initial_builders(self):
        return super(ExplicitDirectorySetup, self).initial_builders() + \
               [Confix2_dir_ExplicitInterface(), CommonDirectoryInterface_Confix2_dir()]
    pass
