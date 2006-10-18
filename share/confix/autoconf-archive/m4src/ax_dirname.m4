dnl @synopsis AX_DIRNAME(PATHNAME)
dnl
dnl Parts of the implementation have been taken from AS_DIRNAME from
dnl the main autoconf package in generation 2.5x. However, we do only
dnl use "sed" to cut out the dirname, and we do additionally clean up
dnl some dir/.. parts in the resulting pattern.
dnl
dnl this macro may be used in autoconf 2.13 scripts as well.
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2005-01-21
dnl @license GPLWithACException

AC_DEFUN([AX_DIRNAME],
[echo X[]$1 |
    sed ['s/\/[^\/:][^\/:]*\/..\//\//g
          s/\/[^\/:][^\/:]*\/..\//\//g
          s/\/[^\/:][^\/:]*\/..\//\//g
          s/\/[^\/:][^\/:]*\/..\//\//g
          /^X\(.*[^/]\)\/\/*[^/][^/]*\/*$/{ s//\1/; q; }
          /^X\(\/\/\)[^/].*/{ s//\1/; q; }
          /^X\(\/\/\)$/{ s//\1/; q; }
          /^X\(\/\).*/{ s//\1/; q; }
          s/.*/./; q']])
