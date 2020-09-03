dnl @synopsis MDL_CXX_FUNCTION_TRY_BLOCKS
dnl
dnl If the C++ compiler supports function try blocks, define
dnl `HAVE_FUNCTION_TRY_BLOCKS'.
dnl
dnl @category Cxx
dnl @author Matthew D. Langston <langston@SLAC.Stanford.EDU>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([MDL_CXX_FUNCTION_TRY_BLOCKS],
[
AC_REQUIRE([AC_PROG_CXX])
changequote(,)dnl
AC_MSG_CHECKING(whether ${CXX} supports function try blocks)
changequote([,])dnl
AC_CACHE_VAL(mdl_cv_have_function_try_blocks,
[
AC_LANG_SAVE
AC_LANG_CPLUSPLUS
AC_TRY_COMPILE([void foo() try{} catch( ... ){}],
[foo();],
mdl_cv_have_function_try_blocks=yes,
mdl_cv_have_function_try_blocks=no)
AC_LANG_RESTORE
])
AC_MSG_RESULT($mdl_cv_have_function_try_blocks)
if test "$mdl_cv_have_function_try_blocks" = yes; then
AC_DEFINE(HAVE_FUNCTION_TRY_BLOCKS)
fi])
