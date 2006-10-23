 #!/usr/bin/env python

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

from distutils.core import setup
import os
import sys

def recdir(dir, suffix, result):
    locals = []
    if os.path.isdir(dir):
        for entry in os.listdir(dir):
            fullname = os.path.join(dir, entry)
            if os.path.isfile(fullname) and fullname.endswith(suffix):
                locals.append(fullname)
            elif os.path.isdir(fullname):
                if entry in ['CVS', '.svn']: continue
                recdir(fullname, suffix, result)
                pass
            pass
        pass
    if locals:
        result.append((dir, locals))
        pass
    return result

datafiles = recdir('share', '.m4', [])

# this should be imported from the current directory ...
from libconfix.core.utils import const

setup(
    name="Confix",
    license="LGPL",
    url="http://confix.sf.net/",
    version=const.CONFIX_VERSION,
    description="A Build Tool Based on Automake",
    author="Joerg Faschingbauer",
    author_email="jfasch@users.sourceforge.net",

    # argh. have to name every single subdirectory (at least until I
    # find a better way.)
    packages=['libconfix',
              'libconfix.core',
              'libconfix.core.repo',
              'libconfix.core.digraph',
              'libconfix.core.iface',
              'libconfix.core.utils',
              'libconfix.core.automake',
              'libconfix.core.hierarchy',
              'libconfix.core.filesys',
              'libconfix.frontends',
              'libconfix.frontends.confix',
              'libconfix.plugins',
              'libconfix.plugins.c',
              'libconfix.plugins.idl',
              'libconfix.plugins.plainfile',
              'libconfix.plugins.script',
              'libconfix.plugins.make',
              'libconfix.testutils',
              ],
    data_files=datafiles,
    scripts=['scripts/confix2.py',
             'scripts/writedot.py',
             'scripts/print_module.py',

             # scripts to put in the auxdir. ideally we should not
             # install them as scripts, but rather as regular data
             # files which we accidentally put in auxdir -- but it's
             # simpler this way for the time being.
             
             'scripts/bulk-install.py',
             'scripts/conf.change.pl',
             'scripts/config.pl',
             ],
    )
