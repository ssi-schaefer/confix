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

from linked import LinkedBuilder
from buildinfo import BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled

from libconfix.core.machinery.builder import BuilderSet

class ExecutableBuilder(LinkedBuilder):

    BIN = 0
    CHECK = 1
    NOINST = 2
    
    def __init__(self,
                 center,
                 exename,
                 what,
                 use_libtool):

        assert what in [ExecutableBuilder.BIN,
                        ExecutableBuilder.CHECK,
                        ExecutableBuilder.NOINST]

        LinkedBuilder.__init__(self, use_libtool=use_libtool)

        LinkedBuilder.add_member(self, center)

        self.__center = center
        self.__exename = exename
        self.__what = what
        pass

    def unique_id(self):
        # careful: we cannot have exename as part of the builder's
        # id. exename can be manipulated at will by the user during
        # the lifetime of the object.
        return str(self.__class__)+'('+self.parentbuilder().unique_id()+','+self.center().unique_id()+')'

    def shortname(self):
        return 'C.ExecutableBuilder('+self.exename()+',center='+self.__center.file().name()+')'

    def center(self):
        return self.__center
    def exename(self):
        return self.__exename
    def what(self):
        return self.__what

    def output(self):
        LinkedBuilder.output(self)

        mf_am = self.parentbuilder().makefile_am()

        if self.__what == ExecutableBuilder.BIN:
            mf_am.add_bin_program(self.__exename)
        elif self.__what == ExecutableBuilder.CHECK:
            mf_am.add_check_program(self.__exename)
        elif self.__what == ExecutableBuilder.NOINST:
            mf_am.add_noinst_program(self.__exename)
        else: assert 0

        for m in self.members():
            mf_am.add_compound_sources(self.__exename, m.file().name())
            pass

        for fragment in LinkedBuilder.get_linkline(self):
            mf_am.add_compound_ldadd(
                compound_name=self.__exename,
                lib=fragment)
            pass
        pass
        
    pass
