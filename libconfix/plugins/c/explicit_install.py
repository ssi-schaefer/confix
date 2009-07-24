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

from h import HeaderBuilder

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

class ExplicitInstaller(Builder):
    """
    Sit around and wait for user requests like,
    "Ey man, tell all HeaderBuilders that come along to install their files to 'some/directory'".

    User requests are usually those from an interface proxy sitting in
    Confix2.dir.
    """

    def __init__(self, installdir):
        Builder.__init__(self)
        self.__installdir = installdir
        self.__seen_header_builders = set()
        pass

    def locally_unique_id(self):
        return str(self.__class__.__name__)

    def enlarge(self):
        super(ExplicitInstaller, self).enlarge()
        if self.__installdir is None:
            return
        for b in self.parentbuilder().iter_builders():
            if not isinstance(b, HeaderBuilder):
                continue
            if b in self.__seen_header_builders:
                continue
            b.set_external_install_path(self.__installdir)
            self.__seen_header_builders.add(b)
            # we just have modified dependency information, so another
            # round must be made.
            self.force_enlarge()
            pass
        pass
    pass

class INSTALLDIR_H(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('INSTALLDIR_H', getattr(self, 'INSTALLDIR_H'))
        pass
    def INSTALLDIR_H(self, dir):
        try:
            the_dir = helper.make_path(dir)
        except Error, e:
            raise Error('INSTALLDIR_H(): dir argument must either '
                        'be a string or a list of path components', [e])
        self.__dirbuilder.add_builder(ExplicitInstaller(installdir=the_dir))
        pass
    pass

class ExplicitInstallerSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(INSTALLDIR_H(dirbuilder=dirbuilder))
        pass
    pass
