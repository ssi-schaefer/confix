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

class LexBuilder(CompiledCBuilder):
    def __init__(self, file):
        CompiledCBuilder.__init__(self, file=file)
        pass
        
    def output(self):
        CompiledCBuilder.output(self)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_LEX']),
            order=Configure_ac.PROGRAMS)
        root, ext = os.path.splitext(self.file().name())
        if ext == '.l':
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CC']),
                order=Configure_ac.PROGRAMS)
            self.parentbuilder().makefile_am().add_built_sources(root + '.c')
        elif ext == '.ll':
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CXX']),
                order=Configure_ac.PROGRAMS)
            self.parentbuilder().makefile_am().add_built_sources(root + '.cc')
            # argh: when using "%option c++" in the lex source file,
            # flex generates lex.yy.cc, which automake doesn't seem to
            # be aware of. force it to generate the file automake is
            # aware of. this is not supposed to work with other lexers
            # however. but, as the documentation states, it is better
            # to not use the C++ feature of lex since it is inherently
            # non-portable anyway.
            self.parentbuilder().makefile_am().add_am_lflags('-olex.yy.c')
        else:
            assert 0
            pass
        pass

    pass
