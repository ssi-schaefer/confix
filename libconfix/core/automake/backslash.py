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

""" BACKSLASH_MITIGATOR: we wrap long lines with backslashes, so
that various tools are happy. for example, config.status scans
Makefile.in using grep. on several Unices (AIX, HP-UX I seem to
remember), grep does not accept lines of inifinite length.

certain make macros - AM_CPPFLAGS for example - end up being
long lists of items most of which are autoconf @blah@
substitutions, some of which end up being substituted with the
empty string. if such an empty substitution is on a single line
at the end of such a long list, the previous line contains a
trailing backslash, followed by an empty line. some make
implementations (HP-UX, again) handle this kind of consciousless
and scan through until they find something meaningful, which
they then consider part of th list. argh.

however, the solution is to terminate every list with a macro
that expands to nothing, just to make bogus make's scan
algorithm happy. """

BACKSLASH_MITIGATOR = '$(CONFIX_BACKSLASH_MITIGATOR)'
