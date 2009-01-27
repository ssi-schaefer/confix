# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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
import sys
import re

from libconfix.plugins.automake.auxdir import AutoconfAuxDirBuilder
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils import helper
from libconfix.core.utils.error import Error

class KDEHackSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(AutoconfAuxDirWatcher())
        pass
    pass

class AutoconfAuxDirWatcher(Builder):
    """ On enlarge(), if my parent directory is of type
    AutoconfAuxDirBuilder, put the necessary files in it."""

    def locally_unique_id(self):
        # I am supposed to be the only one of my kind in a given
        # directory, so my class suffices as an ID.
        return str(self.__class__)
    
    def enlarge(self):
        super(AutoconfAuxDirWatcher, self).enlarge()
        if not isinstance(self.parentbuilder(), AutoconfAuxDirBuilder):
            return

        try:
            confix_root = helper.find_confix_root(sys.argv[0])
        except Error, e:
            raise Error('Cannot find KDE hack support files', [e])

        kde_hack_dir = os.path.join(confix_root, 'share', 'confix', 'kde-hack')
        conf_change_pl = os.path.join(kde_hack_dir, 'conf.change.pl')
        config_pl = os.path.join(kde_hack_dir, 'config.pl')
        if not os.path.isfile(conf_change_pl):
            raise Error('Cannot apply KDE hack: '+conf_change_pl+' not found')
        if not os.path.isfile(config_pl):
            raise Error('Cannot apply KDE hack: '+config_pl+' not found')

        self.parentbuilder().eat_file(sourcename=conf_change_pl, mode=0755)
        self.parentbuilder().eat_file(sourcename=config_pl, mode=0755)
        pass
    pass
        

def patch_configure_script(packageroot):
    filename = os.sep.join(packageroot+['configure'])
    
    tmp_filename = filename + '.new.' + str(os.getpid())
    re_chmod_config_status = re.compile(r'^\s*chmod\s+.*\+x\s+.*CONFIG_STATUS')

    mode_orig = os.stat(filename).st_mode
    f_orig = file(filename)
    f_tmp = file(tmp_filename, 'w')
    for line in f_orig:
        if re_chmod_config_status.search(line):
            f_tmp.write('\n'
                        '  perl -i.bak $ac_aux_dir/conf.change.pl $CONFIG_STATUS \\\n'
                        '    || mv $CONFIG_STATUS.bak $CONFIG_STATUS\n'
                        '  rm -f $CONFIG_STATUS.bak\n'
                        '\n')
            pass
        f_tmp.write(line)
        pass

    f_tmp.close()
    f_orig.close()
    os.rename(tmp_filename, filename)
    os.chmod(filename, mode_orig)
    pass
