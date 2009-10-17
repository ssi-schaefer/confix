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

from libconfix.core.machinery.buildinfo import BuildInformationSet

import types

class LibraryBuilder(LinkedBuilder):
    def __init__(self,
                 basename,
                 version,
                 default_version):

        # library version. passed to libtool as "-version-info
        # <current>:<revision>:<age>", for example.
        assert version is None or type(version) in [types.ListType, types.TupleType] and len(version) == 3

        # default library version. passed to libtool as "-release
        # <package-version>"
        assert default_version is None or type(default_version) is types.StringType
        
        LinkedBuilder.__init__(self)

        self.__basename = basename
        self.__version = version
        self.__default_version = default_version

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

    def iter_buildinfos(self):
        for bi in super(LibraryBuilder, self).iter_buildinfos():
            yield bi
            pass
        yield BuildInfo_CLibrary_NativeLocal(
            dir=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
            basename=self.__basename)
        pass

    def set_version(self, version):
        self.__version = version
        pass

    def set_basename(self, name):
        self.__basename = name

        # people may have seen the original basename, so we have to
        # trigger another round.
        super(LibraryBuilder, self).force_enlarge()
        pass

    def version(self):
        return self.__version

    def default_version(self):
        return self.__default_version

    pass
