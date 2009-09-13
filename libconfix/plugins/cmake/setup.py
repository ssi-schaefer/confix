# Copyright (C) 2009 Joerg Faschingbauer

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


from out_cmake import CMakeBackendOutputBuilder
from out_c import COutputSetup
from iface import CMakeInterfaceSetup

from libconfix.core.machinery.setup import CompositeSetup
from libconfix.core.machinery.setup import Setup

class CMakeSetup(CompositeSetup):
    def __init__(self):
        CompositeSetup.__init__(
            self,
            setups=[CMakeCSetup(),
                    CMakeInterfaceSetup(),
                    InfraStructureSetup()])
        pass
    pass

class InfraStructureSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_backend_dirbuilder(CMakeBackendOutputBuilder())
        pass
    pass

class CMakeCSetup(CompositeSetup):
    def __init__(self):
        CompositeSetup.__init__(self, setups=[COutputSetup()])
        pass
    pass
