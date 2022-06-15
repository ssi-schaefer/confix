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

from .dependency import RequireRelocatedHeader

from libconfix.plugins.c.dependency import Provide_CInclude

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.dependency_utils import DependencyInformation

class Slave(Builder):
    def __init__(self, header_builder):
        Builder.__init__(self)
        self.__header_builder = header_builder
        pass

    def __str__(self):
        return str(self.__class__) + ': header_builder='+str(self.__header_builder)
    
    def locally_unique_id(self):
        # we are tempted to use the relative path of the header that
        # we are responsible for. but we simply cannot calculate the
        # relative path because we do not yet know our package (which
        # is where the relative path starts). anyway, it's just an ID,
        # so we use the object ID of the header builder.
        return str(self.__class__)+': '+str(id(self.__header_builder))

    def dependency_info(self):
        ret = DependencyInformation()
        ret.add(super(Slave, self).dependency_info())

        # we require the original header for obvious reasons.
        ret.add_require(RequireRelocatedHeader(
            filename=self.__header_builder.file().name(),
            source_directory=self.__header_builder.parentbuilder().directory().relpath(self.package().rootbuilder().directory())))

        # we steal the dependency info from the original header. FIXME
        # (possibly): what about the "internal provide" stuff?
        ret.add(self.__header_builder.do_really_get_dependency_info())
        
        return ret

    pass
