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

import os

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.automake.configure_ac import Configure_ac

from compiled import CompiledCBuilder

class YaccBuilder(CompiledCBuilder):
    def __init__(self, file):
        CompiledCBuilder.__init__(self, file=file)
        pass
        
    def output(self):
        CompiledCBuilder.output(self)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_YACC']),
            order=Configure_ac.PROGRAMS)
        root, ext = os.path.splitext(self.file().name())
        if ext == '.y':
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CC']),
                order=Configure_ac.PROGRAMS)
            self.parentbuilder().makefile_am().add_built_sources(root + '.c')
        elif ext == '.yy':
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CXX']),
                order=Configure_ac.PROGRAMS)
            self.parentbuilder().makefile_am().add_built_sources(root + '.cc')
            # force Yacc to output files named y.tab.h
            self.parentbuilder().makefile_am().add_am_yflags('-d');
        else:
            assert 0
            pass
        pass

    pass
