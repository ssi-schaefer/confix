# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from linked import LinkedBuilder
from buildinfo import BuildInfo_CLibrary_NativeLocal

import types

class LibraryBuilder(LinkedBuilder):
    def __init__(self,
                 basename,
                 libtool_version_info,
                 libtool_release_info):

        # libtool version information; to be passed to libtool
        # -version-info <current>:<revision>:<age>

        # jjj get rid of that since it is automaek specific.
        assert libtool_version_info is None or \
               type(libtool_version_info) in [types.ListType, types.TupleType] and len(libtool_version_info) == 3

        # libtool release information; to be passed as -release
        # <package-version>

        # jjj get rid of that since it is automaek specific.
        assert libtool_release_info is None or \
               type(libtool_release_info) is types.StringType
        
        LinkedBuilder.__init__(self)

        self.__basename = basename
        self.__libtool_version_info = libtool_version_info
        self.__libtool_release_info = libtool_release_info

        self.__buildinfo_added = False
        
        pass

    def locally_unique_id(self):
        # careful: we cannot have basename as part of the builder's
        # id. basename can be manipulated at will by the user during
        # the lifetime of the object. but we can be sure that there's
        # only one library being built in one directory (at least for
        # the time being - maybe this constraint will go away in the
        # future, but then we will know), so it is sufficient to have
        # our class to distinguish.
        return str(self.__class__)

    def shortname(self):
        return 'C.LibraryBuilder('+self.basename()+')'

    def basename(self):
        return self.__basename

    def enlarge(self):
        super(LibraryBuilder, self).enlarge()
        if self.__buildinfo_added:
            return
        self.__buildinfo_added = True
        self.add_buildinfo(BuildInfo_CLibrary_NativeLocal(
            dir=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
            name=self.__basename))
        pass

    # jjj
    def set_libtool_version_info(self, version_info):
        self.__libtool_version_info = version_info
        pass

    # jjj
    def set_libname(self, name):
        self.__basename = name
        pass

    # jjj
    def libtool_version_info(self):
        return self.__libtool_version_info

    # jjj
    def libtool_release_info(self):
        return self.__libtool_release_info

    pass
