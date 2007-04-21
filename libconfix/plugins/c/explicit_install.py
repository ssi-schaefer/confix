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

from h import HeaderBuilder

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

class ExplicitInstaller(Builder):
    """
    Sit around and wait for user request like,
    "Ey man, tell all HeaderBuilders that come along to install their files to 'some/directory'".

    User request are usually those from an interface proxy sitting in
    Confix2.dir.
    """

    def __init__(self):
        Builder.__init__(self)
        self.__installdir = None
        self.__seen_header_builders = set()
        pass

    def locally_unique_id(self):
        return str(self.__class__.__name__)

    def set_installdir(self, path):
        if self.__installdir is not None:
            raise Error('Header install directory has already been set to '+'/'.join(self.__installdir))
        self.__installdir = path
        pass

    def enlarge(self):
        super(ExplicitInstaller, self).enlarge()
        if self.__installdir is None:
            return
        for b in self.parentbuilder().builders():
            if not isinstance(b, HeaderBuilder):
                continue
            if b in self.__seen_header_builders:
                continue
            b.set_external_install_path(self.__installdir)
            pass
        pass

class ExplicitInstallerInterfaceProxy(InterfaceProxy):
    def __init__(self, explicit_installer):
        InterfaceProxy.__init__(self)
        self.__explicit_installer = explicit_installer
        self.add_global('INSTALLDIR_H', getattr(self, 'INSTALLDIR_H'))
        pass
    def INSTALLDIR_H(self, dir):
        try:
            the_dir = helper.make_path(dir)
        except Error, e:
            raise Error('INSTALLDIR_H(): dir argument must either '
                        'be a string or a list of path components', [e])
        self.__explicit_installer.set_installdir(the_dir)
        pass
    pass

class ExplicitInstallerSetup(Setup):
    def initial_builders(self):
        ret = super(ExplicitInstallerSetup, self).initial_builders()

        installer = ExplicitInstaller()
        proxy = ExplicitInstallerInterfaceProxy(explicit_installer=installer)

        ret.add_builder(installer)
        ret.add_iface_proxy(proxy)

        return ret
    pass
