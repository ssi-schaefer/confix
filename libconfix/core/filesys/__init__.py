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

""" A file system abstraction which is used throughout the project.

Rather than accessing the operating system's real file system, we use
an abstraction that allows us to simulate files and directories,
without them being physically present on disk. This is really
meaningless when reading a source tree (which obviously has to be
present on disk) in real life. For automatic tests, on the other hand,
this is an excellent vehicle: one can create an entire source tree in
memory, generate Makefile.am's all over it, examine them to see if
they're ok, and then simply forget about the whole tree.

(Take a look at the tests, they are full of `filesys.FileSystem`,
`file.File`, and `directory.Directory` usage.)

.. classtree:: filesys.Entry

"""
