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

import os
import types

from libconfix.core.automake import helper_automake
from libconfix.core.automake.rule import Rule
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.utils import const, helper
from libconfix.core.utils.error import Error

from dependency import Provide_CInclude
from h import HeaderBuilder
import buildinfo

class DefaultInstaller(Builder):

    class InstallPathConflict(Error):
        def __init__(self, msg):
            Error.__init__(self, msg)
            pass
        pass
                           
    def __init__(self):
        Builder.__init__(self)
        self.__global_installdir = None
        self.__files_installed_as = {}
        self.__buildinfo_passed = False
        pass

    def shortname(self):
        return 'C.DefaultInstaller'

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def set_installdir(self, dir):
        assert type(dir) is list
        self.__global_installdir = dir
        pass

    def installpath_of_headerfile(self, filename):
        # for testing
        return self.__files_installed_as[filename]

    def enlarge(self):
        super(DefaultInstaller, self).enlarge()
        
        for b in self.parentbuilder().builders():
            if not isinstance(b, HeaderBuilder):
                continue
            new_instdir = self.__calc_install_path(b)
            old_instdir = self.__files_installed_as.get(b.file().name())
            if old_instdir is None:
                # seeing it for the first time.
                self.__files_installed_as[b.file().name()] = new_instdir
                
                # provide it.

                # we potentially have to provide ourselves in a
                # twofold way:

                # in any case, we provide it to the outside world. for
                # example, if the file is named "file.h", and its
                # install path is "some/directory", then we have to
                # provide the file like "some/directory/file.h". if
                # its install path is empty, we'll provide the file as
                # "file.h", of course. in short, we provide the file
                # as it is included by OTHERS: they'll say, #include
                # <some/directory/file.h>, or #include <file.h>,
                # respectively.

                # on the other hand, local users - those which reside
                # in the same directory as we do - have to say
                # #include "file.h", regardless where it is installed.

                filename = b.file().name()
                outside_name = '/'.join([d for d in new_instdir] + [filename])
                self.add_provide(Provide_CInclude(outside_name))
                
                if outside_name != filename:
                    self.add_internal_provide(Provide_CInclude(filename))
                    pass
                pass
            else:
                assert old_instdir == new_instdir
                pass
            pass
        if not self.__buildinfo_passed:
            if len(self.__files_installed_as):
                self.add_buildinfo(buildinfo.singleton_buildinfo_cincludepath_nativelocal)
                self.__buildinfo_passed = True
                pass
            pass
        pass

    def output(self):
        super(DefaultInstaller, self).output()
        for filename, instdir in self.__files_installed_as.iteritems():
            # fixme: is it right to not distinguish between public and
            # private?
            self.parentbuilder().file_installer().add_public_header(filename=filename, dir=instdir)
            self.parentbuilder().file_installer().add_private_header(filename=filename, dir=instdir)
            pass
        pass

    def __calc_install_path(self, b):
        ret = None
        defined_in = []

        iface = b.iface_install_path()
        glob = self.__global_installdir
        property = b.property_install_path()

        if iface is not None:
            ret = iface
            defined_in.append(('file interface', iface))
            pass
        if glob is not None:
            ret = glob
            defined_in.append(('Confix2.dir', glob))
            pass
        if property is not None:
            ret = property
            defined_in.append(('file property', property))
            pass

        if len(defined_in) > 1:
            raise DefaultInstaller.InstallPathConflict(
                'Install path ambiguously defined: '+\
                ','.join([msg+'('+'/'.join(loc)+')' for msg, loc in defined_in]))
        
        if ret is None:
            ret = b.namespace_install_path()
            pass
        if ret is None:
            ret = ''
            pass

        return ret

    pass        

class DefaultInstallerInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('INSTALLDIR_H', getattr(self, 'INSTALLDIR_H'))
        pass
    def INSTALLDIR_H(self, dir):
        try:
            the_dir = helper.make_path(dir)
        except Error, e:
            raise Error('INSTALLDIR_H(): dir argument must either '
                        'be a string or a list of path components', [e])
        self.__object.set_installdir(the_dir)
        pass
    pass

class DefaultInstallerSetup(Setup):
    def setup_directory(self, directory_builder):
        super(DefaultInstallerSetup, self).setup_directory(directory_builder)

        installer = DefaultInstaller()
        directory_builder.add_builder(installer)
        
        if directory_builder.configurator() is not None:
            directory_builder.configurator().add_method(
                DefaultInstallerInterfaceProxy(object=installer))
            pass
        pass
    pass
