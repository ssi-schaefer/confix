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

import sys, os

from libconfix.core.utils.error import Error
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File, FileState
from libconfix.frontends.confix import cmdline 
from libconfix.frontends.confix import todo 
from libconfix.frontends.confix.configfile import ConfigFile 
from libconfix.frontends.confix.composite_config import CompositeConfiguration 
from libconfix.frontends.confix.default_config import DefaultConfiguration

def main():
    try:
        config = CompositeConfiguration()
        (cmdlinecfg, actions) = cmdline.parse(sys.argv[1:])
        config.add(cmdlinecfg)

        configfile = cmdlinecfg.configfile()
        configfileobj = None

        if configfile is not None:
            configfileobj = FileSystem(path=os.path.dirname(configfile).split(os.sep)).rootdirectory().add(
                name=os.path.basename(configfile),
                entry=File(state=FileState.SYNC_CLEAR))
        else:
            configdir = cmdlinecfg.configdir()
            if configdir is None:
                candidate = os.path.expanduser('~/.confix2')
                if os.path.exists(candidate):
                    configdir = candidate
                    pass
                pass
            if configdir is not None:
                if not os.path.exists(configdir):
                    raise Error('Directory "'+configdir+'" does not exist')
                if not os.path.isdir(configdir):
                    raise Error('"'+configdir+'" exists but is not a directory')
                confixfs = scan_filesystem(path=configdir.split(os.sep))
                configfileobj = confixfs.rootdirectory().find(['config'])
                pass
            pass

        if configfileobj is not None:
            configfile = ConfigFile(file=configfileobj)
            if cmdlinecfg.profile() is not None:
                profilename = cmdlinecfg.profile()
            else:
                profilename = 'default'
                pass
            config.add(configfile.get_profile(profilename))
            pass
        
        config.add(DefaultConfiguration())

        todo.TODO = actions
        todo.CONFIG = config

        # normally todo failures will throw exceptions, but this is in here just
        # as a safety measure.
        if todo.todo():
            sys.exit(1)
            pass
        pass
        
    except Error, e:
        sys.stderr.write('***ERROR***\n')
        sys.stderr.write(str(e)+'\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
