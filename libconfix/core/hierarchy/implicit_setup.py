# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from .common_iface import DirectoryBuilderInterfaceProxy
from .subdir_recognizer import SubdirectoryRecognizer
from .confix2_dir_creator import Confix2_dir_Creator

from libconfix.core.machinery.setup import Setup

class ImplicitDirectorySetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(DirectoryBuilderInterfaceProxy(dirbuilder=dirbuilder))
        dirbuilder.add_builder(SubdirectoryRecognizer())
        dirbuilder.add_builder(Confix2_dir_Creator())
        pass
    pass
