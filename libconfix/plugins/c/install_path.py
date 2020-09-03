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

def calc_install_path(self, header_builder):
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
