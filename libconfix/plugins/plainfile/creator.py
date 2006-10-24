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

import re

from libconfix.core.filesys.file import File
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils.error import Error

from builder import PlainFileBuilder

class PlainFileCreator(Builder):
    def __init__(self, regex, prefixdir, datadir):
        assert (datadir is None or prefixdir is None and \
                datadir is not None or prefixdir is not None), \
                'prefixdir: '+str(prefixdir) + ', datadir: '+str(datadir)
        
        Builder.__init__(self)

        self.__regex = regex
        self.__datadir = datadir
        self.__prefixdir = prefixdir
        self.__handled_entries = set()
        
        try:
            self.compiled_regex_ = re.compile(regex)
        except Exception, e:
            raise Error('Error compiling regex "'+regex+'"', [e])

        pass

    def unique_id(self):
        return str(self.__class__)+'('+self.parentbuilder().unique_id()+','+self.__regex+')'

    def enlarge(self):
        super(PlainFileCreator, self).enlarge()
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, File):
                continue
            if name in self.__handled_entries:
                continue
            if self.compiled_regex_.search(name):
                self.parentbuilder().add_builder(
                    PlainFileBuilder(file=entry,
                                     datadir=self.__datadir,
                                     prefixdir=self.__prefixdir))
                self.__handled_entries.add(name)
                break
            pass
        pass
    pass
