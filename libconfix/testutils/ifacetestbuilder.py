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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.machinery.interface import CodePiece
from libconfix.core.machinery.interface import InterfaceExecutor

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.setup import Setup

class FileInterfaceTestSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(FileInterfaceTestCreator())
        pass
    pass

class FileInterfaceTestCreator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.handled_entries_ = set()
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def enlarge(self):
        super(FileInterfaceTestCreator, self).enlarge()
        for name, entry in self.parentbuilder().directory().entries():
            if not isinstance(entry, VFSFile):
                continue
            if entry in self.handled_entries_:
                continue
            if name.endswith('.iface'):
                self.parentbuilder().add_builder(FileInterfaceTestBuilder(file=entry))
                self.handled_entries_.add(entry)
                continue
            pass
        pass
    pass

class FileInterfaceTestBuilder(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        self.__node = None
        self.__topolist = None
        self.__successors = None
        self.__relate_calls = 0
        self.__enlarge_calls = 0
        pass

    def initialize(self, package):
        super(FileInterfaceTestBuilder, self).initialize(package)
        lines=self.file().lines()
        if len(lines):
            execer = InterfaceExecutor(iface_pieces=self.iface_pieces())
            execer.execute_pieces([CodePiece(start_lineno=1, lines=lines)])
            pass
        pass
    def node(self):
        return self.__node
    def topolist(self):
        return self.__topolist
    def successors(self):
        return self.__successors
    def enlarge(self):
        self.__enlarge_calls += 1
        return FileBuilder.enlarge(self)
    def relate(self, node, digraph, topolist):
        FileBuilder.relate(self, node, digraph, topolist)
        self.__node = node
        self.__topolist = topolist
        self.__successors = digraph.successors(node)
        self.__relate_calls += 1
        pass
    def iface_pieces(self):
        return FileBuilder.iface_pieces(self)
    def relate_calls(self):
        return self.__relate_calls
    def enlarge_calls(self):
        return self.__enlarge_calls
    pass
