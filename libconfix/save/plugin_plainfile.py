# $Id: plugin_plainfile.py,v 1.18 2006/06/21 12:20:11 jfasch Exp $

# Copyright (C) 2003 Salomon Automation

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

from core.require_string import Require_String
from core.provide_string import Provide_String
from buildable_single import BuildableSingle
import core.helper
import helper_automake
from buildable_mgr_bases import BuildableCreator
from core.marshalling import Marshallable, MarshalledVersionUnknownError, update_marshalling_data

import os

DIRTYPE_DATA = 0
DIRTYPE_PREFIX = 1
DIRTYPE_TUNNEL = 2

class BuildablePlainFileCreator(BuildableCreator):
    def __init__(self,
                 tunneldir=None,
                 prefixdir=None,
                 datadir=None,

                 name=None, # obsolete
                 installdir=None, # deprecated
                 ):
        BuildableCreator.__init__(self)

        self.type_ = DIRTYPE_DATA
        self.the_dir_ = ''

        the_tunneldir = tunneldir

        if installdir is not None:
            debug.warn('BuildablePlainFileCreator.__init__(): '
                       'installdir is deprecated; use datadir, prefixdir or tunneldir instead')
            the_tunneldir = installdir
            pass

        if name is not None:
            debug.warn('BuildablePlainFileCreator.__init__(): name is obsolete')
            pass

        if the_tunneldir is not None:
            self.type_ = DIRTYPE_TUNNEL
            self.the_dir_ = installdir
            pass
        if prefixdir is not None:
            self.type_ = DIRTYPE_PREFIX
            self.the_dir_ = prefixdir
            pass
        if datadir is not None:
            self.type_ = DIRTYPE_DATA
            self.the_dir_ = datadir
            pass
        pass

    def create_from_file(self, dir, filename, lines):
        return BuildablePlainFile(
            dir=dir,
            filename=filename,
            lines=lines,
            type=self.type_,
            installdir=self.the_dir_)
    pass

class BuildablePlainFile(BuildableSingle):

    """ Provide and installs an arbitrary file. Distributes location
    information (id 'PLAINFILE'), in order for others to find it. """

    def __init__(self,
                 dir,
                 filename,
                 lines,
                 type=DIRTYPE_DATA,
                 installdir=''):

        BuildableSingle.__init__(
            self,
            dir=dir,
            filename=filename,
            lines=lines)

        self.add_public_provide(Provide_PlainFile(
            filename=filename))

        self.installdir_ = installdir
        self.dirtype_ = type

        pass

    def set_am_dir_dirname(self, dir, dirname):
        debug.warn(self.dir()+'/'+self.filename()+': '
                   'BuildablePlainFile.set_am_dir_dirname() is deprecated; '
                   'use set_datadir(), set_prefixdir() or set_tunneldir() instead')
        self.set_tunneldir(dirname)
        pass

    def set_datadir(self, dir):
        self.dirtype_ = DIRTYPE_DATA
        self.installdir_ = dir
        pass
    def set_prefixdir(self, dir):
        self.dirtype_ = DIRTYPE_PREFIX
        self.installdir_ = dir
        pass
    def set_tunneldir(self, dir):
        self.dirtype_ = DIRTYPE_TUNNEL
        self.installdir_ = dir
        pass
    
    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def contribute_makefile_am(self, buildmod):

        BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

        if self.dirtype_ == DIRTYPE_DATA:
            buildmod.file_installer().add_datafile(filename=self.filename(), dir=self.installdir_)
        elif self.dirtype_ == DIRTYPE_PREFIX:
            buildmod.file_installer().add_prefixfile(filename=self.filename(), dir=self.installdir_)
        elif self.dirtype_ == DIRTYPE_TUNNEL:
            buildmod.file_installer().add_tunnelfile(filename=self.filename(), dir=self.installdir_)
        else:
            assert 0
            pass
        pass

    pass

class Require_PlainFile(Require_String):

    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require_String.get_marshalling_data(self),
            generating_class=Require_PlainFile,
            attributes={},
            version={'Require_PlainFile': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require_PlainFile']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Require_String.set_marshalling_data(self, data)
        pass

    def __init__(self, filename):

        fn = core.helper.normalize_filename(filename)
        Require_String.__init__(
            self,
            id=fn,
            string=fn,
            found_in=[])

class Provide_PlainFile(Provide_String):

    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide_String.get_marshalling_data(self),
            generating_class=Provide_PlainFile,
            attributes={},
            version={'Provide_PlainFile': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_PlainFile']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide_String.set_marshalling_data(self, data)
        pass

    EXACT_MATCH = Provide_String.EXACT_MATCH
    PREFIX_MATCH = Provide_String.PREFIX_MATCH
    GLOB_MATCH = Provide_String.GLOB_MATCH

    MATCH_CLASSES = [Require_PlainFile]

    def __init__(self, filename, match=EXACT_MATCH):

        Provide_String.__init__(
            self,
            string=core.helper.normalize_filename(filename),
            match=match)

    def __repr__(self):
        return "PlainFile: "+self.string()

    def can_match_classes(self): return Provide_PlainFile.MATCH_CLASSES
