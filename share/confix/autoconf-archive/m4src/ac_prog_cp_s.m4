dnl @synopsis AC_PROG_CP_S
dnl
dnl Check how to make a copy by creating a symbolic link to the
dnl original - it defines the variable CP_S for further use, which you
dnl should in fact treat like it used to be with be LN_S. The actual
dnl value is assured to be either LN_S (if the filesystem supports
dnl symbolic links) or CP (if the filesystem does not know about
dnl symbolic links and you need a copy of original file to have the
dnl same text in both places). In a gnu environment it will simply set
dnl CP_S="cp -s" since the gnu "cp"-command has the "-s" flag. You
dnl shall not try to use this command on directories since it would
dnl require a "-r" in the case of a copy that is not supported
dnl explicitly here. (I'm not sure if some "cp"-commands out there
dnl would barf at usage of "-r" on a normal file).
dnl
dnl Use CP_S to create a copy of read-only data - if your filesystem
dnl supports it then a symbolic link is created - a process that is
dnl quicker and space-saving. However, if the target fs does not
dnl support symbolic links, just copy the data. Unlike ac_prog_ln_s
dnl this macro will never fail to set the CP_S ac_subst to something
dnl that works.
dnl
dnl @category InstalledPackages
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2003-10-29
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_CP_S],
[AC_REQUIRE([AC_PROG_LN_S])dnl
AC_MSG_CHECKING(whether cp -s works)
AC_CACHE_VAL(ac_cv_prog_CP_S,
[rm -f conftestdata
if cp -s X conftestdata 2>/dev/null
then
  rm -f conftestdata
  ac_cv_prog_CP_S="cp -s"
else
  ac_cv_prog_CP_S=cp
fi
if test "$LN_S" = "ln -s" ; then
  ac_cv_prog_CP_S="ln -s"
fi])dnl
CP_S="$ac_cv_prog_CP_S"
if test "$ac_cv_prog_CP_S" = "ln -s"; then
  AC_MSG_RESULT(using ln -s)
elif test "$ac_cv_prog_CP_S" = "cp -s"; then
  AC_MSG_RESULT(yes)
else
  AC_MSG_RESULT(no, using cp)
fi
AC_SUBST(CP_S)dnl
])
