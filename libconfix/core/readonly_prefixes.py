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

from libconfix.core.utils.paragraph import Paragraph

incdirs_var = 'readonly_prefixes_incdirs'
incdirs_subst = '@'+incdirs_var+'@'

incpath_var = 'readonly_prefixes_incpath'
incpath_subst = '@'+incpath_var+'@'

libdirs_var = 'readonly_prefixes_libdirs'
libdirs_subst = '@'+libdirs_var+'@'

libpath_var = 'readonly_prefixes_libpath'
libpath_subst = '@'+libpath_var+'@'

commandline_option_paragraph = Paragraph([
    'AC_ARG_WITH(readonly-prefixes,',
    '            AC_HELP_STRING([--with-readonly-prefixes=<comma-separated list of prefixes>],',
    '                           [blah]),',
    '                           [',
    '                           if test x$withval != xno; then',
    '                               '+incdirs_var+'=',
    '                               '+incpath_var+'=',
    '                               '+libdirs_var+'=',
    '                               '+libpath_var+'=',
    '                               for loc in `echo $withval | sed \'s/,/ /g\'`; do',
    '                                   '+incdirs_var+'="${'+incdirs_var+'} $loc/include"',
    '                                   '+incpath_var+'="${'+incpath_var+'} -I$loc/include"',
    '                                   '+libdirs_var+'="${'+libdirs_var+'} $loc/lib"',
    '                                   '+libpath_var+'="${'+libpath_var+'} -L$loc/lib"',
    '                               done',
    '                               AC_SUBST('+incdirs_var+')',
    '                               AC_SUBST('+incpath_var+')',
    '                               AC_SUBST('+libdirs_var+')',
    '                               AC_SUBST('+libpath_var+')',
    '                           fi',
    '                           ]',
    '                           )'
    ])
