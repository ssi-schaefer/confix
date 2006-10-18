# $Id: helper_configure_in.py,v 1.1 2005/11/06 22:01:11 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

from paragraph import OrderedParagraphSet, Paragraph

AC_PROG_CXX = OrderedParagraphSet()
AC_PROG_CXX.add(
    paragraph=Paragraph(['AC_PROG_CXX']),
    order=ORDER_PROGRAMS)


AM_PROG_LEX = OrderedParagraphSet()
AM_PROG_LEX.add(
    paragraph=Paragraph(['AM_PROG_LEX']),
    order=ORDER_PROGRAMS)

AC_PROG_YACC = OrderedParagraphSet()
AC_PROG_YACC.add(
    paragraph=Paragraph(['AC_PROG_YACC']),
    order=ORDER_PROGRAMS)
