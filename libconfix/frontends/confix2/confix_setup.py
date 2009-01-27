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

from libconfix.core.machinery.setup import CompositeSetup
from libconfix.core.machinery.core_setup import CoreSetup
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.plainfile.setup import PlainFileInterfaceSetup
from libconfix.plugins.script.setup import ScriptSetup
from libconfix.plugins.idl.setup import IDLSetup
from libconfix.plugins.make.setup import MakeSetup

from libconfix.plugins.automake.setup import AutomakeSetup

class ConfixSetup(CompositeSetup):
    def __init__(self,
                 use_libtool,
                 short_libnames):
        CompositeSetup.__init__(
            self,
            [CoreSetup(),
             ImplicitDirectorySetup(),
             DefaultCSetup(short_libnames=short_libnames),
             ScriptSetup(),
             IDLSetup(),
             PlainFileInterfaceSetup(),
             MakeSetup(),
             AutomakeSetup(use_libtool=use_libtool)])
        pass

    pass
