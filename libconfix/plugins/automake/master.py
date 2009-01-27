# Copyright (C) 2008 Joerg Faschingbauer

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

class AutomakeMaster(Builder):
    def __init__(self):
        Builder.__init__(self)

        # move these out into the C setup
        self.__slaves = [
            HeaderOutputBuilder(),
            CompiledOutputBuilder(),
            COutputBuilder(),
            CXXOutputBuilder(),
            LexOutputBuilder(),
            YaccOutputBuilder(),
            LibraryOutputBuilder(use_libtool=self.__use_libtool),
            ExecutableOutputBuilder(use_libtool=self.__use_libtool),
            ]

        self.__bursted = False

        # the (contents of the) Makefile.am we will be writing on
        # output()
        self.__makefile_am = Makefile_am()

        # a helper that we use to install files intelligently (well,
        # more or less so).
        self.__file_installer = FileInstaller()

        pass

    def enlarge(self):
        super(AutomakeMaster, self).enlarge()
        if self.__bursted:
            return
        self.__bursted = True
        for s in self.__slaves:
            self.parentbuilder().add_builder(s)
            pass
        pass

    def output(self):
        super(AutomakeMaster, self).output()

        # before we flush our structures, request our slaves to
        # persist their needs.
        for s in self.__slaves:
            s.automake_output(makefile_am=self.__makefile_am,
                              file_installer=self.__file_installer,
                              configure_ac=self.package().configure_ac(),
                              acinclude_m4=self.__acinclude_m4)
            pass

        # 'make maintainer-clean' should remove the files that we
        # generate
        self.__makefile_am.add_maintainercleanfiles('Makefile.am')
        self.__makefile_am.add_maintainercleanfiles('Makefile.in')

        # request the file installer (have to get rid of this crap) to
        # write his instructions to our Makefile.am
        self.__file_installer.output(makefile_am=self.__makefile_am)

        # finally, write our Makefile.am.
        mf_am = self.parentbuilder().directory().find(['Makefile.am'])
        if mf_am is None:
            mf_am = File()
            self.parentbuilder().directory().add(name='Makefile.am', entry=mf_am)
        else:
            mf_am.truncate()
            pass

        mf_am.add_lines(self.__makefile_am.lines())
        
        pass
    pass
