# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.core.machinery.setup import CompositeSetup
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class C(CompositeSetup):
    def __init__(self):
        CompositeSetup.__init__(self, [ExplicitCSetup()])
        pass
    pass

class AutoC(CompositeSetup):
    def __init__(self, libnamefinder=None, has_undefined_symbols=False):
        CompositeSetup.__init__(self, [DefaultCSetup(libnamefinder, has_undefined_symbols=has_undefined_symbols)])
        pass
    pass
