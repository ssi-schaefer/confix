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
from dependency import ProvideRelocatedHeader

from libconfix.plugins.c.h import HeaderBuilder

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.depinfo import DependencyInformation
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error

class Master(Builder):

    def __init__(self, filename, directory):
        Builder.__init__(self)
        self.__filename = filename
        self.__directory = directory
        self.__header_builder = None
        self.__target_directory_builder = None
        self.__slave = None

        self.__num_retries = 0
        pass

    def locally_unique_id(self):
        return str(self.__class__)+':'+self.__filename

    def enlarge(self):
        super(Master, self).enlarge()

        if self.__slave is not None:
            return

        # first, we collect everything that is necessary to perform
        # the relocation - the header builder and the target directory
        # builder.

        # note that both need not be present from the beginning. they
        # just might not have been seen yet because of indeterminisms
        # in the order in which builders are called, or the respective
        # directory entries might physically not exist because they
        # are subject to be created.

        if self.__header_builder is None:
            self.__header_builder = self.parentbuilder().find_entry_builder([self.__filename])
            if self.__header_builder is None:
                self.force_enlarge()
                self.__num_retries += 1
                if self.__num_retries > 20:
                    raise Error(self.__error_prefix()+': '+self.__filename+' not seen after 20 rounds')
                pass
            elif not isinstance(self.__header_builder, HeaderBuilder):
                raise Error(self.__error_prefix()+': not a header file ('+str(source_header_builder)+')')
            pass

        if self.__target_directory_builder is None:
            self.__target_directory_builder = self.package().rootbuilder().find_entry_builder(self.__directory)
            if self.__target_directory_builder is None:
                self.force_enlarge()
                self.__num_retries += 1
                if self.__num_retries > 20:
                    raise Error(self.__error_prefix()+': '+'/'.join(self.__directory)+' not seen after 20 rounds')
                pass
            elif not isinstance(self.__target_directory_builder, DirectoryBuilder):
                raise Error(self.__error_prefix()+': target not a directory ('+str(self.__target_directory_builder)+')')
            pass

        # once we have everything at hand, create a slave in the
        # target directory and tell our header builder to shut up.

        if self.__header_builder is None or self.__target_directory_builder is None:
            return

        self.__slave = Slave(header_builder=self.__header_builder)
        self.__target_directory_builder.add_builder(self.__slave)
        self.__header_builder.set_not_provided()
        pass

    def dependency_info(self):
        ret = DependencyInformation()
        ret.add(super(Master, self).dependency_info())
        ret.add_provide(
            ProvideRelocatedHeader(filename=self.__header_builder.file().name(),
                                   source_directory=self.parentbuilder().directory().relpath(self.package().rootbuilder().directory())))
        return ret

    def __error_prefix(self):
        return 'Cannot relocate header '+self.__filename

    pass
        
