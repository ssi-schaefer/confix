dnl @synopsis AC_C_VAR_FUNC
dnl
dnl This macro tests if the C complier supports the C9X standard
dnl __func__ indentifier.
dnl
dnl The new C9X standard for the C language stipulates that the
dnl identifier __func__ shall be implictly declared by the compiler as
dnl if, immediately following the opening brace of each function
dnl definition, the declaration
dnl
dnl     static const char __func__[] = "function-name";
dnl
dnl appeared, where function-name is the name of the function where the
dnl __func__ identifier is used.
dnl
dnl @category C
dnl @author Christopher Currie <christopher@currie.com>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([AC_C_VAR_FUNC],
[AC_REQUIRE([AC_PROG_CC])
AC_CACHE_CHECK(whether $CC recognizes __func__, ac_cv_c_var_func,
AC_TRY_COMPILE(,
[int main() {
char *s = __func__;
}],
AC_DEFINE(HAVE_FUNC,,
[Define if the C complier supports __func__]) ac_cv_c_var_func=yes,
ac_cv_c_var_func=no) )
])dnl
