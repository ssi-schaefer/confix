dnl @synopsis AC_PROG_MODPROBE
dnl
dnl This macro searches for a modprobe command, such as can be found on
dnl Linux systems with loadable kernel module support. PATH is checked
dnl first, then the default location(s).
dnl
dnl This is one of several autoconf macros intended to assist in
dnl configuring and installing loadable kernel modules.
dnl
dnl @category InstalledPackages
dnl @author Kaelin Colclasure <kaelin@acm.org>
dnl @version 2000-12-31
dnl @license AllPermissive

AC_DEFUN([AC_PROG_MODPROBE],[
AC_PATH_PROG(MODPROBE, modprobe, , $PATH:/sbin)
if test -z "$MODPROBE"; then
  AC_MSG_WARN([no support for loadable kernel modules])
else
  AC_MSG_CHECKING([for module_prefix])
  module_prefix=`$MODPROBE -c | grep path.kernel.= \
                 | sed -e '2,$d' -e 's/.*=//' -e 's/.kernel//'`
  AC_MSG_RESULT($module_prefix)
  AC_SUBST(module_prefix)
fi
])
