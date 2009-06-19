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

from linked import LinkedBuilder
from buildinfo import BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled

class ExecutableBuilder(LinkedBuilder):

    BIN = 0
    CHECK = 1
    NOINST = 2
    
    def __init__(self,
                 center,
                 exename,
                 what):

        assert what in [ExecutableBuilder.BIN,
                        ExecutableBuilder.CHECK,
                        ExecutableBuilder.NOINST]

        LinkedBuilder.__init__(self)

        LinkedBuilder.add_member(self, center)

        self.__center = center
        self.__exename = exename
        self.__what = what
        pass

    def locally_unique_id(self):
        return str(self.__class__) + ':' + self.__exename + '(' + self.center().file().name() + ')'
 
    def shortname(self):
        return 'C.ExecutableBuilder('+self.exename()+',center='+self.__center.file().name()+')'

    def center(self):
        return self.__center
    def exename(self):
        return self.__exename
    def what(self):
        return self.__what

    pass
