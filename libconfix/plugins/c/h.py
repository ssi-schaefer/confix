# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.depinfo import DependencyInformation
from libconfix.core.machinery.buildinfoset import BuildInformationSet
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
                           '/'.join(header_builder.file().relpath(header_builder.package().rootdirectory()))+'": '+\
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
        self.__property_install_path = None
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

        if self.file() is not None:
            self.__property_install_path = self.file().get_property(HeaderBuilder.PROPERTY_INSTALLPATH)
            pass
        try:        
            self.__namespace_install_path = namespace.find_unique_namespace(self.file().lines())
        except Error, e:
            self.__namespace_error = Error('Could not initialize '+'/'.join(self.file().relpath(dir=self.package())), [e])
            pass
        pass

    def set_iface_install_path(self, path):
        self.__iface_install_path = path
        pass

    def set_external_install_path(self, path):
        assert type(path) in (list, tuple)
        self.__external_install_path = path
        pass

    def iface_pieces(self):
        return super(HeaderBuilder, self).iface_pieces() + [HeaderBuilderInterfaceProxy(object=self)]

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

        outer_name = '/'.join(self.visible_in_directory()+[self.file().name()])
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

        # if the receiver can see the file directly (without doing a
        # local install), then tell him the directory that he has to
        # add to his include path. else, only tell him the local
        # install directory.
        direct_includedir = _get_direct_includedir(
            rootdir=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
            visibledir=self.visible_in_directory())

        if direct_includedir is not None:
            ret.add(BuildInfo_CIncludePath_NativeLocal(include_dir=direct_includedir))
        else:
            ret.add(BuildInfo_CIncludePath_NativeLocal(include_dir=None))
            pass

        return ret

    def output(self):
        super(HeaderBuilder, self).output()
        installdir = self.visible_in_directory()
        self.parentbuilder().file_installer().add_public_header(filename=self.file().name(), dir=installdir)

        # see above: see if we need to locally install the file.
        include_dir = _get_direct_includedir(
            rootdir=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
            visibledir=self.visible_in_directory())
        if include_dir is None:
            self.parentbuilder().file_installer().add_private_header(
                filename=self.file().name(),
                dir=self.visible_in_directory())
            pass
        pass

    def visible_in_directory(self):
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
        if self.__property_install_path is not None:
            if set_by is not None:
                raise self.AmbiguousVisibility(header_builder=self, cur='file property', prev=set_by)
            ret = self.__property_install_path
            set_by = 'file property'
            pass

        if ret is None:
            # bail out if we had an error recognizing the namespace
            if self.__namespace_error is not None:
                raise self.BadNamespace(path=self.file().relpath(self.package().rootdirectory()),
                                        error=self.__namespace_error)
            ret = self.__namespace_install_path
            pass

        if ret is None:
            ret = []
            pass

        return ret
    pass

class HeaderBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object=object)
        self.add_global('INSTALLPATH', getattr(self, 'INSTALLPATH'))
        pass
    def INSTALLPATH(self, path):
        self.object().set_iface_install_path(helper.make_path(path))
        pass
    pass

def _get_direct_includedir(rootdir, visibledir):
    if len(rootdir) < len(visibledir):
        return None
    if rootdir[len(rootdir)-len(visibledir):] == visibledir:
        return rootdir[0:len(rootdir)-len(visibledir)]
    return None
