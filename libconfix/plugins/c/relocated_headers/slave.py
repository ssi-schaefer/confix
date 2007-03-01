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

from libconfix.plugins.c.dependency import Provide_CInclude

from libconfix.core.machinery.builder import Builder

class Slave(Builder):
    def __init__(self, header_builder, master):
        Builder.__init__(self)
        self.__header_builder = header_builder
        self.__master = master
        pass

    def __str__(self):
        return str(Slave, self) + ': header_builder='+str(self.__header_builder)

    def locally_unique_id(self):
        return str(self.__class__)+':'+'/'.join(self.__header_builder.file().relpath(self.package().rootdirectory()))

    def output(self):
        """
        If the header builder has not yet been actively taken back by
        my master (because he has eventually been asked for output
        before me), give it back.
        """
        super(Slave, self).output()
        if self.__header_builder:
            self.__master.take_back_header_builder(self.__header_builder)
            self.__header_builder = None
            pass
        pass

    pass
