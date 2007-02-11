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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.provide_symbol import Provide_Symbol
from libconfix.core.utils import external_cmd
from libconfix.core.filesys import scan

class MakeCaller(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__requested_calls = []

        # FIXME: crap; see below
        self.__crap_force_enlarge_round = 0
        pass

    def locally_unique_id(self):
        return self.__class__.__name__

    def add_call(self, filename, args):
        self.__requested_calls.append((filename, args))
        self.__force_enlarge()
        pass

    def enlarge(self):
        super(MakeCaller, self).enlarge()

        if len(self.__requested_calls) == 0:
            return

        for filename, args in self.__requested_calls:
            external_cmd.exec_program(
                program='make',
                dir=self.parentbuilder().directory().abspath(),
                args=['-f', filename] + args)
            pass

        # make might have had side effects that we don't see
        scan.rescan_dir(self.parentbuilder().directory())

        # just in case it had, we tell the machinery to initiate
        # another round to have them recognized
        # eventually. performancewise, we could see if the directory
        # state changed, and only then reiterate. on the other, we can
        # never know what Makefile writers think and do, and they
        # could generate files in other directories than the current.
        self.__force_enlarge()
        
        self.__requested_calls = []
        
        pass

    def __force_enlarge(self):
        # FIXME: once TRY-jfasch-nonlocal-headers has been merged, use
        # Builder.force_enlarge() instead of this crap

        # force one more enlarge round by pretending that dependency
        # info has changed.
        self.add_provide(
            Provide_Symbol(symbol='Bogus dummy crap: '+self.__class__.__name__+\
                           '(package='+self.package().name()+','
                           'directory='+'/'.join(self.parentbuilder().directory().relpath(self.package().rootdirectory()))+'):'+\
                           str(self.__crap_force_enlarge_round)))
        self.__crap_force_enlarge_round += 1
        pass
    pass
