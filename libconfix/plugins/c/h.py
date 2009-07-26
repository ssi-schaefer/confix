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

from base import CBaseBuilder
from dependency import Provide_CInclude
from buildinfo import BuildInfo_CIncludePath_NativeLocal
import namespace

from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.machinery.dependency_utils import DependencyInformation
from libconfix.core.machinery.buildinfo import BuildInformationSet
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper
from libconfix.core.utils import const

import os

class HeaderBuilder(CBaseBuilder):
    PROPERTY_INSTALLPATH = 'INSTALLPATH_CINCLUDE'

    class AmbiguousVisibility(Error):
        def __init__(self, header_builder, cur, prev):
            Error.__init__(self,
                           msg='Ambiguous visibility of header "'+\
                           '/'.join(header_builder.file().relpath(from_dir=header_builder.package().rootdirectory()))+'": '+\
                           cur+'/'+prev)
            pass
        pass

    class BadNamespace(Error):
        def __init__(self, path, error):
            assert isinstance(error, Error)
            Error.__init__(self,
                           msg='Bad namespace in file '+'/'.join(path),
                           list=[error])
            pass
        pass
    
    def __init__(self, file):
        CBaseBuilder.__init__(self, file=file)

        self.__namespace_install_path = None
        self.__namespace_error = None
        self.__iface_install_path = None
        self.__external_install_path = None

        # a flag that makes the public dependency_info() method return
        # nothing. currently only needed for relocating headers, but
        # not necessarily so.
        self.__dependency_info_disabled = False

        pass

    def shortname(self):
        return 'C.HeaderBuilder('+self.file().name()+')'

    def initialize(self, package):
        # let the base class do its work. note that this will use our
        # iface_pieces() method to gather together interface
        # contributions, and thus eventually set
        # self.__iface_install_path.
        super(HeaderBuilder, self).initialize(package)

        try:        
            self.__namespace_install_path = namespace.find_unique_namespace(self.file().lines())
        except Error, e:
            self.__namespace_error = Error('Could not initialize '+'/'.join(self.file().relpath(from_dir=package.rootdirectory())), [e])
            pass
        pass

    def set_iface_install_path(self, path):
        self.force_enlarge()
        self.__iface_install_path = path
        pass

    def set_external_install_path(self, path):
        assert type(path) in (list, tuple)
        self.force_enlarge()
        self.__external_install_path = path
        pass

    def public_visibility(self):
        ret = None
        set_by = None

        if self.__external_install_path is not None:
            if set_by is not None:
                raise self.AmbiguousVisibility(header_builder=self, cur='explicit setting', prev=set_by)
            ret = self.__external_install_path
            set_by = "explicit setting"
            pass

        if self.__iface_install_path is not None:
            if set_by is not None:
                raise self.AmbiguousVisibility(header_builder=self, cur='file interface invocation', prev=set_by)
            ret = self.__iface_install_path
            set_by = 'file interface invocation'
            pass

        property_install_path = self.file().get_property(HeaderBuilder.PROPERTY_INSTALLPATH)
        if property_install_path is not None:
            if set_by is not None:
                raise self.AmbiguousVisibility(header_builder=self, cur='file property', prev=set_by)
            ret = property_install_path
            set_by = 'file property'
            pass

        if ret is None:
            # bail out if we had an error recognizing the namespace
            if self.__namespace_error is not None:
                raise self.BadNamespace(path=self.file().relpath(from_dir=self.package().rootdirectory()),
                                        error=self.__namespace_error)
            ret = self.__namespace_install_path
            pass

        if ret is None:
            ret = []
            pass

        return ret

    LOCAL_INSTALL = 0
    DIRECT_INCLUDE = 1
    def local_visibility(self):
        """
        Decide if we have to 'locally install' the file, in order to
        make it visible to the other nodes in the package.

        Two examples:

        1. A file is declared to be visible as 'a/b/file.h', but is
           physically available as 'c/file.h' (all relative to the
           package root). This file has to be 'locally installed'
           because no-one can set an inclue file to get this file.

        2. If, on the other hand, the file is physically available as
           'c/a/b/file.h', then other can see it by simply adding the
           directory 'c' to the include path.

        Returns a tuple (what, path) where what is either of
        LOCAL_INSTALL or DIRECT_INCLUDE, and path is the respective
        path. Example 1. would return (LOCAL_INSTALL, ['a','b']), to
        indicate that file.h would have to be copied to some directory
        'a/b' under some directory (which then has to be put on the
        include path of the user). Example 2. would return
        (DIRECT_INCLUDE, ['c']) to indicate that the file doesn't need
        a copy to be useful, and that directory 'c' has to be put on
        the user's include path.
        """
        complete_path = self.parentbuilder().directory().relpath(from_dir=self.package().rootdirectory())
        visible_path = self.public_visibility()
        
        if len(complete_path) < len(visible_path):
            return (self.LOCAL_INSTALL, visible_path)
        if complete_path[len(complete_path)-len(visible_path):] == visible_path:
            return (self.DIRECT_INCLUDE, complete_path[0:len(complete_path)-len(visible_path)])
        return (self.LOCAL_INSTALL, visible_path)

    def iface_pieces(self):
        return super(HeaderBuilder, self).iface_pieces() + [HeaderBuilderInterfaceProxy(builder=self)]

    def disable_dependency_info(self):
        """
        Makes the Builder interface's HeaderBuilder.dependency_info()
        method do nothing. The local method
        HeaderBuilder.do_really_get_dependency_info() can then be used
        to get the information you want.
        """
        self.__dependency_info_disabled = True
        pass

    def dependency_info(self):
        """
        Get the dependency information of self, but only if
        disable_dependency_info() has not been called.
        """
        # note that we have to pass the request on to the base, since
        # somebody checks that the base was reached. a good idea
        # otherwise, but here we have to throw the information away
        # and return nothing in case we were instructed to do so.
        ret = self.do_really_get_dependency_info()
        if self.__dependency_info_disabled:
            return DependencyInformation()
        return ret

    def do_really_get_dependency_info(self):
        """
        Get the dependency information, regardles if
        disable_dependency_info() has been called.
        """
        ret = DependencyInformation()
        ret.add(super(HeaderBuilder, self).dependency_info())

        outer_name = '/'.join(self.public_visibility()+[self.file().name()])
        ret.add_provide(Provide_CInclude(filename=outer_name))

        # regardless if we will provide ourselves to the outer world,
        # and regardless of how we will be doing that, we will
        # eventually be included/required by files in the same
        # directory. to neutralize their require objects (a node
        # eliminates require objects the are resolved internally),
        # provide ourselves.
        if outer_name is None or self.file().name() != outer_name:
            ret.add_internal_provide(Provide_CInclude(filename=self.file().name()))
            pass

        return ret

    def buildinfos(self):
        ret = BuildInformationSet()
        ret.merge(super(HeaderBuilder, self).buildinfos())

        local_visibility = self.local_visibility()
        if local_visibility[0] == self.DIRECT_INCLUDE:
            # receiver can see the file directly, by adding a
            # directory of the source package to the path.
            ret.add(BuildInfo_CIncludePath_NativeLocal(include_dir=local_visibility[1]))
        elif local_visibility[0] == self.LOCAL_INSTALL:
            # receiver has to add the directory on the include path
            # where the locally installed files are
            # ($(top_srcdir)/confix_include for the automake backend)
            ret.add(BuildInfo_CIncludePath_NativeLocal(include_dir=None))
        else:
            assert False
            pass
        
        return ret

    pass

class HeaderBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)
        self.__builder = builder
        self.add_global('INSTALLPATH', getattr(self, 'INSTALLPATH'))
        pass
    def INSTALLPATH(self, path):
        self.__builder.set_iface_install_path(helper.make_path(path))
        pass
    pass

