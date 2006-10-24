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

from libconfix.core.machinery.setup import Setup
from libconfix.core.hierarchy.setup import DirectorySetup

from libconfix.plugins.c.setup import DefaultCSetup
from libconfix.plugins.plainfile.setup import PlainFileInterfaceSetup
from libconfix.plugins.script.setup import ScriptSetup
from libconfix.plugins.idl.setup import IDLSetup
from libconfix.plugins.make.setup import MakeSetup

class ConfixSetup(Setup):
    def __init__(self,
                 use_libtool,
                 short_libnames):
        Setup.__init__(self)
        self.setups_ = [DirectorySetup(),
                        DefaultCSetup(short_libnames=short_libnames, use_libtool=use_libtool),
                        ScriptSetup(),
                        IDLSetup(),
                        PlainFileInterfaceSetup(),
                        MakeSetup()]
        pass

    def setup_directory(self, directory_builder):
        Setup.setup_directory(self, directory_builder)
        for setup in self.setups_:
            setup.setup_directory(directory_builder)
            pass
        pass
    pass
