# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from common_iface_setup import CommonInterfaceSetup

from libconfix.plugins.c.clusterer import CClustererSetup
from libconfix.plugins.c.creator import CCreatorSetup
from libconfix.plugins.c.implicit_iface import ImplicitInterfaceSetup
from libconfix.plugins.c.relocated_headers.setup import RelocatedHeadersSetup

from libconfix.core.machinery.setup import CompositeSetup

def make_core_setups(linkednamefinder):
    return [CClustererSetup(linkednamefinder=linkednamefinder),
            CCreatorSetup(),
            CommonInterfaceSetup(),
            RelocatedHeadersSetup(),
            ]

class DefaultCSetup(CompositeSetup):
    def __init__(self,
                 linkednamefinder=None):
        setups = make_core_setups(linkednamefinder=linkednamefinder)
        setups.append(ImplicitInterfaceSetup())
        CompositeSetup.__init__(
            self,
            setups=setups)
        pass
    pass
