# $Id: modinst.py,v 1.23 2006/06/21 12:20:11 jfasch Exp $

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

from modbase import ModuleBase
from core.dependencyset import DependencySet
from core.buildinfoset import BuildInformationSet
from core.provide import Provide
from core.provide_string import Provide_String
from core.require import Require
from core.require_string import Require_String
from core.error import Error
from core.marshalling import Marshallable, update_marshalling_data, REPOVERSION_TRACENAME
import core.debug

import types

class InstalledModule(ModuleBase, Marshallable):

    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: InstalledModule,
                Marshallable.VERSIONS: {'InstalledModule': 2},
                Marshallable.ATTRIBUTES: {'fullname': self.fullname_,
                                          'buildinfos': [bi for bi in self.buildinfos_],
                                          'provides': self.provides_,
                                          'requires': self.requires_,
                                          'featuremacro_name': self.featuremacro_name_,
                                          'featuremacro_description': self.featuremacro_description_}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['InstalledModule']
        if version == 1:
            # back in these days the whole information was in the base
            # class. convert it from there.
            assert data[Marshallable.VERSIONS]['ModuleBase'] == 1
            self.fullname_ = [data[Marshallable.ATTRIBUTES]['packagename']] + \
                             data[Marshallable.ATTRIBUTES]['localname']
            self.provides_ = data[Marshallable.ATTRIBUTES]['provides']
            self.requires_ = data[Marshallable.ATTRIBUTES]['requires']
            self.buildinfos_ = BuildInformationSet()
            for bi in data[Marshallable.ATTRIBUTES]['buildinfos']:
                self.buildinfos_.add(bi)
                pass
            self.featuremacro_name_ = data[Marshallable.ATTRIBUTES]['featuremacro_name']
            self.featuremacro_description_ = data[Marshallable.ATTRIBUTES]['featuremacro_description']
            core.debug.trace([REPOVERSION_TRACENAME],
                        'Upgrading InstalledModule '+'.'.join(self.fullname_)+' '
                        'from version 1 to version 2')
            pass
        elif version == 2:
            self.fullname_ = data[Marshallable.ATTRIBUTES]['fullname']
            self.provides_ = data[Marshallable.ATTRIBUTES]['provides']
            self.requires_ = data[Marshallable.ATTRIBUTES]['requires']
            self.buildinfos_ = data[Marshallable.ATTRIBUTES]['buildinfos']
            self.featuremacro_name_ = data[Marshallable.ATTRIBUTES]['featuremacro_name']
            self.featuremacro_description_ = data[Marshallable.ATTRIBUTES]['featuremacro_description']
            pass
        else:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        pass

    def __init__(self,
                 fullname,
                 provides,
                 requires,
                 buildinfos,
                 # argh. remove this bullshit.
                 featuremacro_name,
                 featuremacro_description):
        ModuleBase.__init__(self)

        assert type(provides) is types.ListType
        assert type(requires) is types.ListType
        assert buildinfos.__class__ is BuildInformationSet

        self.fullname_ = fullname
        self.provides_ = provides
        self.requires_ = requires
        self.buildinfos_ = buildinfos
        self.featuremacro_name_ = featuremacro_name
        self.featuremacro_description_ = featuremacro_description
        pass

    def __str__(self): return 'InstalledModule '+'.'.join(self.fullname())

    def fullname(self): return self.fullname_
    def provides(self): return self.provides_
    def requires(self): return self.requires_
    def buildinfos(self): return self.buildinfos_
    def get_featuremacro(self):
        return (self.featuremacro_name_,
                self.featuremacro_description_)

    
