# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

class DebugSetup(Setup):
    def __init__(self, parameters):
        pass
    def initial_builders(self):
        ret = super(DebugSetup, self).initial_builders()
        ret.append(DebugBuilder())
        return ret
    pass

class DebugBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__round = 0
        pass

    def shortname(self):
        return 'Confix.DebugBuilder'        
        
    def enlarge(self):
        super(DebugBuilder, self).enlarge()
        if not self.parentbuilder() is self.package().rootbuilder():
            return
        print('ENLARGE ROUND #'+str(self.__round))
        self.__round += 1
        self.__output_builders(directory_builder=self.parentbuilder(), indent=0)
        pass

    def __output_builders(self, directory_builder, indent):
        print(' '*indent + directory_builder.shortname())

        recursive_builders = []
        leaf_builders = []

        for b in directory_builder.builders():
            if isinstance(b, DirectoryBuilder):
                recursive_builders.append(b)
            else:
                leaf_builders.append(b)
                pass
            pass

        for b in leaf_builders:
            print(' '*(indent+2)+b.shortname())
            pass
        for b in recursive_builders:
            self.__output_builders(directory_builder=b, indent=indent+2)
            pass
        pass

    pass
