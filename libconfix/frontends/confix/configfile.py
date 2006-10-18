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

from libconfix.core.utils.error import Error, NativeError

from profile_config import ProfileConfiguration

import sys, os

class ConfigFile:
    def __init__(self, file):
        self.context_ = {}

        # remember filename for subsequent error messages
        self.filename_ = file.abspath()

        try:
            chdirbackto = None
            if file.is_persistent():
                chdirbackto = os.getcwd()
                os.chdir(os.sep.join(file.parent().abspath()))
                execfile(file.name(), self.context_)
                os.chdir(chdirbackto)
                return
            else:
                exec '\n'.join(file.lines()) in self.context_
                return
            pass
        except Exception, e:
            if chdirbackto is not None:
                os.chdir(chdirbackto)
                pass
            raise Error('Error in '+'/'.join(file.abspath()), [NativeError(e, sys.exc_traceback)])

        pass

    def get_profile(self, name):
        profiles_dict = self.context_.get('PROFILES')
        if profiles_dict is None:
            raise Error('PROFILES dictionary not found in '+os.sep.join(self.filename_))
        profile = profiles_dict.get(name)
        if profile is None:
            raise Error('Profile "'+name+'" not found in '+os.sep.join(self.filename_))
        return ProfileConfiguration(profile)

    pass
