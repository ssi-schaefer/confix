assert False

# Copyright (C) 2007 Joerg Faschingbauer

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

def initialize_directory(confix2_dir_builder, dir_builder, package):
    assert package is not None
    initial = package.get_initial_builders()
    if confix2_dir_builder is not None:
        confix2_dir_builder.add_iface_proxies(initial.iface_proxies())
        dir_builder.add_builder(confix2_dir_builder)
        pass
    dir_builder.add_builders(initial.builders())
    pass
