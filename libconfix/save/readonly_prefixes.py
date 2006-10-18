# $Id: readonly_prefixes.py,v 1.12 2006/06/21 12:20:11 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

from paragraph import Paragraph

readonly_prefixes_var = 'readonly_prefixes'
readonly_prefixes_subst = '@'+readonly_prefixes_var+'@'

incdirs_var = 'readonly_prefixes_incdirs'
incdirs_subst = '@'+incdirs_var+'@'

libdirs_var = 'readonly_prefixes_libdirs'
libdirs_subst = '@'+libdirs_var+'@'

datadirs_var = 'readonly_prefixes_datadirs'
datadirs_subst = '@'+datadirs_var+'@'

# for backward compatibility with salomon plugins
datapath_var = 'readonly_prefixes_datapath'
datapath_subst = '@'+datapath_var+'@'

incpath_var = 'readonly_prefixes_incpath'
incpath_subst = '@'+incpath_var+'@'

libpath_var = 'readonly_prefixes_libpath'
libpath_subst = '@'+libpath_var+'@'

commandline_option_paragraph = Paragraph([
    'AC_ARG_WITH(readonly-prefixes,',
    '            AC_HELP_STRING([--with-readonly-prefixes=<comma-separated list of prefixes>],',
    '                           [blah]),',
    '                           [',
    '                           if test x$withval != xno; then',
    '                               '+readonly_prefixes_var+'=',
    '                               '+incdirs_var+'=',
    '                               '+libdirs_var+'=',
    '                               '+datadirs_var+'=',
    '                               '+datapath_var+'=',
    '                               '+incpath_var+'=',
    '                               '+libpath_var+'=',
    '                               for loc in `echo $withval | sed \'s/,/ /g\'`; do',
    '                                   '+readonly_prefixes_var+'="${'+readonly_prefixes_var+'} $loc"',
    '                                   '+incdirs_var+'="${'+incdirs_var+'} $loc/include"',
    '                                   '+libdirs_var+'="${'+libdirs_var+'} $loc/lib"',
    '                                   '+datadirs_var+'="${'+datadirs_var+'} $loc/share"',
    '                                   '+datapath_var+'="${'+datapath_var+'} $loc/share"',
    '                                   '+incpath_var+'="${'+incpath_var+'} -I$loc/include"',
    '                                   '+libpath_var+'="${'+libpath_var+'} -L$loc/lib"',
    '                               done',
    '                               AC_SUBST('+readonly_prefixes_var+')',
    '                               AC_SUBST('+incdirs_var+')',
    '                               AC_SUBST('+libdirs_var+')',
    '                               AC_SUBST('+datadirs_var+')',
    '                               AC_SUBST('+datapath_var+')',
    '                               AC_SUBST('+incpath_var+')',
    '                               AC_SUBST('+libpath_var+')',
    '                           fi',
    '                           ]',
    '                           )'
    ])
