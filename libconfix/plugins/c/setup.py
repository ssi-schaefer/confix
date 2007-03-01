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

from libconfix.core.machinery.setup import CompositeSetup

from clusterer import CClustererSetup
from creator import CreatorSetup
from library_dependencies import LibraryDependenciesFinderSetup
from explicit_install import ExplicitInstallerSetup
from iface import InterfaceSetup
from relocated_headers.setup import RelocatedHeadersSetup
from interix import InterixSetup

def make_core_setups(short_libnames, use_libtool):
    return [CClustererSetup(short_libnames=short_libnames,
                            use_libtool=use_libtool),
            CreatorSetup(),
            InterfaceSetup(),
            RelocatedHeadersSetup(),
            InterixSetup()
            ]

class DefaultCSetup(CompositeSetup):
    def __init__(self,
                 short_libnames,
                 use_libtool):
        setups = make_core_setups(short_libnames=short_libnames, use_libtool=use_libtool)
        setups.append(ExplicitInstallerSetup())
        CompositeSetup.__init__(
            self,
            setups=setups)
        pass
    pass
