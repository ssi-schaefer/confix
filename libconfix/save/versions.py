# $Id: versions.py,v 1.3 2004/12/04 15:44:52 jfasch Exp $

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

def compare_version_strings(l, r):

    """ Compare two version strings in dotted decimal
    notation. "1.2.3" is greater than "1.2.1" and "1.2", and less than
    "2.0" or simply "2", and equal to "1.2.3.0", for example.

    @return:
       - 0 if both versions are equal

       - -1 if l < r

       - +1 if l > r """


    ll = l.split('.')
    lr = r.split('.')

    # pad until both are equal lengths

    while len(ll) != len(lr):
        if len(ll) > len(lr):
            lr.append(0)
        else:
            ll.append(0)

    # compare

    for i in range(len(ll)):
        if ll[i] > lr[i]: return 1
        if ll[i] < lr[i]: return -1

    return 0
