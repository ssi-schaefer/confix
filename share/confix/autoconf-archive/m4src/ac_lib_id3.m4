dnl @synopsis AC_LIB_ID3([ACTION-IF-TRUE], [ACTION-IF-FALSE])
dnl
dnl This macro will check for the existence of id3lib
dnl (http://id3lib.sourceforge.net/). It does this by checking for the
dnl header file id3.h and the id3 library object file. A --with-id3lib
dnl option is supported as well. The following output variables are set
dnl with AC_SUBST:
dnl
dnl   ID3_CPPFLAGS
dnl   ID3_LDFLAGS
dnl   ID3_LIBS
dnl
dnl You can use them like this in Makefile.am:
dnl
dnl   AM_CPPFLAGS = $(ID3_CPPFLAGS)
dnl   AM_LDFLAGS = $(ID3_LDFLAGS)
dnl   program_LDADD = $(ID3_LIBS)
dnl
dnl Additionally, the C preprocessor symbol HAVE_ID3LIB will be defined
dnl with AC_DEFINE if id3lib is available.
dnl
dnl @category InstalledPackages
dnl @author Oskar Liljeblad <oskar@osk.mine.nu>
dnl @version 2005-04-18
dnl @license GPL2

AC_DEFUN([AC_LIB_ID3], [
  AH_TEMPLATE([HAVE_ID3LIB], [Define if id3lib is available])
  AC_ARG_WITH(id3lib, [  --with-id3lib=DIR       prefix for id3 library files and headers], [
    if test "$withval" = "no"; then
      ac_id3_path=
      $2
    elif test "$withval" = "yes"; then
      ac_id3_path=/usr
    else
      ac_id3_path="$withval"
    fi
  ],[ac_id3_path=/usr])
  if test "$ac_id3_path" != ""; then
    saved_CPPFLAGS="$CPPFLAGS"
    CPPFLAGS="$CPPFLAGS -I$ac_id3_path/include"
    AC_CHECK_HEADER([id3.h], [
      saved_LDFLAGS="$LDFLAGS"
      LDFLAGS="$LDFLAGS -L$ac_id3_path/lib"
      AC_CHECK_LIB(id3, ID3Tag_New, [
        AC_SUBST(ID3_CPPFLAGS, [-I$ac_id3_path/include])
        AC_SUBST(ID3_LDFLAGS, [-L$ac_id3_path/lib])
        AC_SUBST(ID3_LIBS, [-lid3])
	AC_DEFINE([HAVE_ID3LIB])
        $1
      ], [
        :
        $2
      ])
      LDFLAGS="$saved_LDFLAGS"
    ], [
      AC_MSG_RESULT([not found])
      $2
    ])
    CPPFLAGS="$saved_CPPFLAGS"
  fi
])
