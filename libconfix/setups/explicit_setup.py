# Copyright (C) 2007-2009 Joerg Faschingbauer

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

from libconfix.core.machinery.setup import CompositeSetup
from libconfix.core.machinery.core_setup import CoreSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.plugins.plainfile.setup import PlainFileInterfaceSetup
from libconfix.plugins.script.setup import ScriptSetup
from libconfix.plugins.idl.setup import IDLSetup
from libconfix.plugins.make.setup import MakeSetup
from libconfix.plugins.automake.setup import AutomakeSetup

class ExplicitSetup(CompositeSetup):
    def __init__(self, use_libtool):
        setups = [CoreSetup(),
                  ExplicitDirectorySetup(),
                  ExplicitCSetup(),
                  ScriptSetup(),
                  IDLSetup(),
                  PlainFileInterfaceSetup(),
                  MakeSetup(),
                  AutomakeSetup(use_libtool=use_libtool),
                  ]
        CompositeSetup.__init__(self, setups)
        pass
    pass
