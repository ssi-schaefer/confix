dnl @synopsis ACX_CHECK_DOS_FILESYS_LIMITATIONS
dnl
dnl Check if the target is running on DOS. DOS doesn't allow a dot as
dnl the first character, more than one dot, more than eight characters
dnl before a dot, and just three letters after the dot. A DOS VM
dnl running under Windows 9X does not have these restrictions. A DOS
dnl program can be running in either environment, so its important to
dnl code accordingly. Defines HAVE_DOS_FILESYS_LIMITATIONS if under
dnl DOS.
dnl
dnl Use in conjunction with ACX_CHECK_PATHNAME_STYLE_DOS.
dnl
dnl @category Misc
dnl @author Mark Elbrecht <snowball3@bigfoot.com>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([ACX_CHECK_DOS_FILESYS_LIMITATIONS],
[AC_MSG_CHECKING(for potential DOS filename limitations)
AC_CACHE_VAL(acx_cv_dos_limitations,
[AC_REQUIRE([AC_CANONICAL_HOST])
acx_cv_dos_limitations="yes"
case ${host_os} in
  *dos | *djgpp) acx_cv_dos_limitations="yes"
esac
])
AC_MSG_RESULT($acx_cv_dos_limitations)
if test $acx_cv_dos_limitations = "yes"; then
  AC_DEFINE(HAVE_DOS_FILESYS_LIMITATIONS)
fi
])
