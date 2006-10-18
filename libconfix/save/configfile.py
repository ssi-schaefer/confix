# $Id: configfile.py,v 1.11 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import sys
from types import *
from core.error import Error, SystemError
from configprofile import ConfigProfile
from core.require_symbol import Require_Symbol

class ConfigFile:
    """
    A class that safely wraps configuration file parsing from the filesystem. If
    the given configuration file doesn't exist, the ConfigFile will return an
    empty (false) configuration set.
    """

    def __init__(self, fullpath):
        """
        Create a ConfigFile instance based on the given filename. Parses the
        given configuration file, if it exists, and sets up a dictionary of
        profiles defined therein.

        @type  fullpath: string
        @param fullpath: a fully qualified path to a configuration file.
        """

        self.profiles_ = {}

        if not os.path.exists(fullpath):
            raise Error('Configuration file "'+fullpath+'" does not exist')

        if not os.path.isfile(fullpath):
            raise Error('Configuration file "'+fullpath+'" exists, but is not a regular file')

        try:
            file = open(fullpath, 'r')
        except Exception, e:
            raise Error("Config file "+fullpath+" exists, "
                        "but cannot be opened due to the following reason:",
                        [SystemError(e, sys.exc_traceback)])

        dict = {
            'Require_Symbol': Require_Symbol,
            'FILENAME_': fullpath
            }

        exec _funcs in dict

        try:
            exec file in dict
        except Exception, e:
            file.close()
            raise Error("Error in config file "+fullpath+":",
                        [SystemError(e, sys.exc_traceback)])

        profs = None
        if dict.has_key('PROFILES'):
            profs = dict['PROFILES']

        if not type(profs) is DictionaryType:
            raise Error('PROFILES must be a dictionary')
        for k in profs.keys():
            try:
                self.profiles_[k] = ConfigProfile(profs[k])
            except Error, e:
                raise Error("Error in profile '"+k+"'", [e])

        file.close()

    def get_profile(self, name):
        """
        Get the profile with a given name from the configuration file. If there
        is no such profile, returns an empty profile.

        @type  name: string
        @param name: the name of the profile to retrieve.
        @rtype: ConfigProfile
        @return: a configuration profile instance containing configuration
          information from the desired profile.
        """

        if self.profiles_.has_key(name):
            return self.profiles_[name]
        else:
            raise Error('Profile "'+name+'" does not exist')


_funcs = """
def REQUIRE_SYMBOL(symbol):

    global FILENAME_

    if not symbol or len(symbol)==0:
        raise Error('REQUIRE_SYMBOL(): need a non-zero symbol parameter')

    return Require_Symbol(symbol, found_in=FILENAME_)

"""
