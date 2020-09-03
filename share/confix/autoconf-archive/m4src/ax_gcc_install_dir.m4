dnl @synopsis AX_GCC_INSTALL_DIR (VARIABLE)
dnl
dnl AX_GCC_INSTALL_DIR (VARIABLE) defines VARIABLE as the gcc install
dnl directory. The install directory will be obtained using the gcc
dnl -print-search-dirs option. This macro requires AX_GCC_OPTION macro.
dnl
dnl @category InstalledPackages
dnl @category C
dnl @author Francesco Salvestrini <salvestrini@users.sourceforge.net>
dnl @version 2005-01-22
dnl @license GPLWithACException

AC_DEFUN([AX_GCC_INSTALL_DIR], [
AC_REQUIRE([AC_PROG_CC])
if test "x$GCC" = "xyes"; then
	AX_GCC_OPTION(GCC_ALL_DIRECTORIES,[-print-search-dirs],[yes],[no])
	if test x"$GCC_ALL_DIRECTORIES" = x"yes"; then
		AC_MSG_CHECKING([gcc install directory])
		ax_gcc_install_dir=`$CC -print-search-dirs | grep install | sed -e "s/^install://" | sed -e "s/\/$//"`
		AC_MSG_RESULT([$ax_gcc_install_dir])
		$1=$ax_gcc_install_dir
	else
		unset $1
	fi
else
        AC_MSG_RESULT([sorry, no gcc available])
	unset $1
fi
])
