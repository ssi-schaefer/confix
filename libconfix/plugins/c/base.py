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
import re
import types

from libconfix.core.filebuilder import FileBuilder
from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.iface.code_piece import CodePiece
from libconfix.core.require import Require
from libconfix.core.utils.error import Error
from libconfix.core.depinfo import DependencyInformation

from dependency import Require_CInclude
from iface import \
     REQUIRE_H_InterfaceProxy, \
     PROVIDE_H_InterfaceProxy
import helper

# argh: '$' does not hit doze-like carriage return, but rather leaves
# it at the end of the match.

_re_confix = re.compile('//\s*CONFIX:([^\r\n]*)')

class CBaseBuilder(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)

        self.eval_iface_()
        
        pass

    def dependency_info(self):
        ret = DependencyInformation()
        ret.add(super(CBaseBuilder, self).dependency_info())
        for h_file in helper.extract_requires(self.file().lines()):
            ret.add_require(
                Require_CInclude(filename=h_file,
                                 found_in='/'.join(self.file().relpath(self.package().rootdirectory()))))
            pass
        return ret

    def iface_pieces(self):
        return FileBuilder.iface_pieces(self) + \
               [REQUIRE_H_InterfaceProxy(object=self),
                PROVIDE_H_InterfaceProxy(object=self)]
    
    def eval_iface_(self):

        # extract python lines from the file and evaluate them. search
        # for 'CONFIX:' lines, gathering blocks of consecutive
        # lines. 'blocks' is a dictionary, with the key being the
        # starting line number, and the value being a list of lines.

        lines = self.file().lines()

        codepieces = []

        lineno = 0
        current_startline = -1
        current_lines = None

        for l in lines:
            lineno = lineno + 1
            match = _re_confix.match(l)

            if match:
                # start new block if we don't yet have one
                if current_startline == -1:
                    current_startline = lineno
                    current_lines = []
                    pass
                current_lines.append(match.group(1))
            else:
                # terminate current block if any
                if current_startline != -1:
                    codepieces.append(CodePiece(start_lineno=current_startline, lines=current_lines))
                    current_startline = -1
                    current_lines = None
                    pass
                pass
            pass
        if current_startline != -1:
            codepieces.append(CodePiece(start_lineno=current_startline, lines=current_lines))
            pass

        try:
            InterfaceExecutor(iface_pieces=self.iface_pieces()).execute_pieces(pieces=codepieces)
        except Error, e:
            raise Error('Could not execute Confix code in '+\
                        '/'.join(self.file().relpath(self.package().rootdirectory())), [e])

        pass
    pass

