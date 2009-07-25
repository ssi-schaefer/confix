# Copyright (C) 2008-2009 Joerg Faschingbauer

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

from iface import AutomakeInterfaceSetup
from out_automake import AutomakeBackendOutputBuilder
from c.setup import CSetup
from script.setup import AutomakeScriptSetup
from plainfile.setup import AutomakePlainfileSetup

from libconfix.core.machinery.setup import CompositeSetup
from libconfix.core.machinery.setup import Setup

class AutomakeSetup(CompositeSetup):
    def __init__(self, use_libtool):
        CompositeSetup.__init__(
            self,
            setups=[AutomakeInterfaceSetup(),
                    CSetup(use_libtool=use_libtool),
                    AutomakeScriptSetup(),
                    AutomakePlainfileSetup(),
                    InfraStructureSetup()])
        pass
    pass

class InfraStructureSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_backend_dirbuilder(AutomakeBackendOutputBuilder())
        pass
    pass
