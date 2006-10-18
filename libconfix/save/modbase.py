# $Id: modbase.py,v 1.63 2006/03/26 19:12:46 jfasch Exp $

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

from core.dependencyset import DependencySet
from core.require import Require
from core.require_string import Require_String
from core.provide import Provide
from core.provide_string import Provide_String
from buildable import Buildable
import core.debug

from sets import Set

class ModuleBase:

    def __init__(self): pass
    def __str__(self): return '.'.join(self.fullname())
    def fullname(self): assert 0, 'abstract'
    def provides(self):

        """ List of Provide objects of this module.
        
        @return: list (at least something the is iterable) of Provide
        objects."""
        
        assert 0, 'abstract'

    def requires(self):

        """ List of Require objects of this module.
        
        @return: list (at least something the is iterable) of Require
        objects."""

        assert 0, 'abstract'

    def buildinfos(self): assert 0, 'abstract'
    def get_featuremacro(self): assert 0, 'abstract'
