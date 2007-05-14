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

# Confix package version

CONFIX_VERSION = '2.0.0pre26'

# the default name of interface files
CONFIX2_DIR = 'Confix2.dir'
CONFIX2_PKG = 'Confix2.pkg'

# the name of our auxiliary files directory

AUXDIR = 'confix-admin'

# the name of the include directory that mimics the include directory
# structure before the files are installed in $(includedir). (this
# directory is located in $(top_builddir).)

LOCAL_INCLUDE_DIR = 'confix_include'

# name of the per-directory file which contains the list of
# automatically generated sources (the pseudo hand-written generated
# files)

PSEUDO_HANDWRITTEN_LIST_FILENAME = '.confix-pseudo-handwritten'
