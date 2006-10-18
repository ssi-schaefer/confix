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

from libconfix.core.utils.error import Error
from libconfix.core.builder import Builder
from libconfix.core.filesys.file import File

from builder import PlainFileBuilder

class PlainFileCreator(Builder):
    def __init__(self, parentbuilder, package, regex, prefixdir, datadir):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+regex+')'+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        
        try:
            self.compiled_regex_ = re.compile(regex)
        except Exception, e:
            raise Error('Error compiling regex "'+regex+'"', [e])

        self.datadir_ = datadir
        self.prefixdir_ = prefixdir
        assert (datadir is None or prefixdir is None and \
                datadir is not None or prefixdir is not None), \
                'prefixdir: '+str(prefixdir) + ', datadir: '+str(datadir)

        self.handled_entries_ = set()
        pass

    def enlarge(self):
        super(PlainFileCreator, self).enlarge()
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, File):
                continue
            if name in self.handled_entries_:
                continue
            if self.compiled_regex_.search(name):
                self.parentbuilder().add_builder(
                    PlainFileBuilder(file=entry,
                                     parentbuilder=self.parentbuilder(),
                                     package=self.package(),
                                     datadir=self.datadir_,
                                     prefixdir=self.prefixdir_))
                self.handled_entries_.add(name)
                break
            pass
        pass
    pass
