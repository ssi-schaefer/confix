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

from slave import Slave
from dependency import RequireRelocatedHeader, ProvideRelocatedHeader

from libconfix.plugins.c.h import HeaderBuilder

from libconfix.core.machinery.builder import Builder
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error

class Master(Builder):
    def __init__(self, filename, directory):
        Builder.__init__(self)
        self.__filename = filename
        self.__directory = directory
        self.__header_builder = None
        self.__slave = None

        self.__num_retries = 0
        pass

    def locally_unique_id(self):
        return str(self.__class__)+':'+self.__filename

    def take_header_builder(self, header_builder):
        assert self.__header_builder is None
        self.__header_builder = header_builder
        pass

    def enlarge(self):
        super(Master, self).enlarge()

        # see if the builder that is to relocate and the relocation
        # target directory builder both are present. it is not an
        # error if they aren't yet -- they might not have been at this
        # point, or they might not even exist because they will be
        # generated at a future point in time.
        source_header_builder = self.parentbuilder().find_entry_builder([self.__filename])
        if source_header_builder is None:
            self.force_enlarge()
            self.__num_retries += 1
            if self.__num_retries > 20:
                raise Error(self.__filename+' not seen after 20 retries')
            return
        if not isinstance(source_header_builder, HeaderBuilder):
            raise Error('Cannot relocate header '+filename+': not a header file ('+str(source_header_builder)+')')
        
        target_directory_builder = self.package().rootbuilder().find_entry_builder(self.__directory)
        if target_directory_builder is None:
            self.force_enlarge()
            self.__num_retries += 1
            if self.__num_retries > 20:
                raise Error('/'.join(self.__directory)+' not seen after 20 retries')
            return
        if not isinstance(target_directory_builder, DirectoryBuilder):
            raise Error('Cannot relocate header '+filename+': target not a directory ('+str(target_directory_builder)+')')

        # temporarily, move the header builder to the target
        # directory. this is where the dependency work is done. add a
        # slave to take care of it there.
        self.parentbuilder().remove_builder(source_header_builder)
        target_directory_builder.add_builder(source_header_builder)
        self.__slave = Slave(header_builder=source_header_builder, master=self)
        target_directory_builder.add_builder(self.__slave)

        self.__header_builder = None
        
        pass

    def output(self):
        super(Master, self).output()
        if self.__header_builder is None:
            self.__header_builder = self.__slave.steal_header_builder()
            pass
        self.parentbuilder().add_builder(self.__header_builder)
        pass

    pass
        
