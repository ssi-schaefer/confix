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

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.automake.configure_ac import Configure_ac

from compiled import CompiledCBuilder
from buildinfo import BuildInfo_CXXFLAGS

class CXXBuilder(CompiledCBuilder):
    def __init__(self, file):
        CompiledCBuilder.__init__(self, file=file)
        self.__init_buildinfo()
        pass

    def shortname(self):
        return 'C.CXXBuilder('+self.file().name()+')'

    def cxxflags(self):
        return self.__cxxflags
        
    def relate(self, node, digraph, topolist):
        CompiledCBuilder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CXXFLAGS):
                    self.__cxxflags.extend(bi.cxxflags())
                    continue
                pass
            pass
        pass

    def output(self):
        CompiledCBuilder.output(self)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_CXX']),
            order=Configure_ac.PROGRAMS)
        for cxxflag in self.__cxxflags:
            self.parentbuilder().makefile_am().add_am_cxxflags(cxxflag)
            pass
        pass

    def __init_buildinfo(self):
        self.__cxxflags = []
        pass

    pass
