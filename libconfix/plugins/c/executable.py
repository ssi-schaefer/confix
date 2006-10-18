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

from libconfix.core.builder import BuilderSet

class ExecutableBuilder(LinkedBuilder):

    BIN = 0
    CHECK = 1
    NOINST = 2
    
    def __init__(self,
                 parentbuilder,
                 package,
                 center,
                 exename,
                 what,
                 use_libtool):

        assert what in [ExecutableBuilder.BIN,
                        ExecutableBuilder.CHECK,
                        ExecutableBuilder.NOINST]

        LinkedBuilder.__init__(
            self,
            id=str(self.__class__)+':'+str(center)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package,
            use_libtool=use_libtool)

        LinkedBuilder.add_member(self, center)

        self.center_ = center
        self.exename_ = exename
        self.what_ = what
        pass

    def center(self):
        return self.center_
    def exename(self):
        return self.exename_
    def what(self):
        return self.what_

    def output(self):
        LinkedBuilder.output(self)

        mf_am = self.parentbuilder().makefile_am()

        if self.what_ == ExecutableBuilder.BIN:
            mf_am.add_bin_program(self.exename_)
        elif self.what_ == ExecutableBuilder.CHECK:
            mf_am.add_check_program(self.exename_)
        elif self.what_ == ExecutableBuilder.NOINST:
            mf_am.add_noinst_program(self.exename_)
        else: assert 0

        for m in self.members():
            mf_am.add_compound_sources(self.exename_, m.file().name())
            pass

        for fragment in LinkedBuilder.get_linkline(self):
            mf_am.add_compound_ldadd(
                compound_name=self.exename_,
                lib=fragment)
            pass
        pass
        
    pass
