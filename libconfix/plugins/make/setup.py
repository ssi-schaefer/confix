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

from libconfix.core.setup import Setup

from iface import CALL_MAKE_AND_RESCAN_InterfaceProxy

class MakeSetup(Setup):
    def setup_directory(self, directory_builder):
        super(MakeSetup, self).setup_directory(directory_builder)
        if directory_builder.configurator() is not None:
            directory_builder.configurator().add_method(
                CALL_MAKE_AND_RESCAN_InterfaceProxy(directory_builder=directory_builder))
            pass
        pass
    pass