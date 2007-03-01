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

from iface import RelocatorInterface

from libconfix.core.machinery.setup import Setup

class RelocatedHeadersSetup(Setup):
    def __init__(self):
        pass
    def initial_builders(self):
        ret = super(RelocatedHeadersSetup, self).initial_builders()
        relocator_iface = RelocatorInterface()
        ret.add_builder(relocator_iface)
        ret.add_iface_proxy(relocator_iface)
        return ret
    pass
