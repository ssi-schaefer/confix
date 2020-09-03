dnl @synopsis AC_FUNC_ACCEPT_ARGTYPES
dnl
dnl Checks the data types of the three arguments to accept(). Results
dnl are placed into the symbols ACCEPT_TYPE_ARG[123], consistent with
dnl the following example:
dnl
dnl       #define ACCEPT_TYPE_ARG1 int
dnl       #define ACCEPT_TYPE_ARG2 struct sockaddr *
dnl       #define ACCEPT_TYPE_ARG3 socklen_t *
dnl
dnl This macro requires AC_CHECK_HEADERS to have already verified the
dnl presence or absence of sys/types.h and sys/socket.h.
dnl
dnl NOTE: This is just a modified version of the
dnl AC_FUNC_SELECT_ARGTYPES macro. Credit for that one goes to David
dnl MacKenzie et. al.
dnl
dnl @category Misc
dnl @author Daniel Richard G. <skunk@mit.edu>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([AC_FUNC_ACCEPT_ARGTYPES],
[AC_MSG_CHECKING([types of arguments for accept()])
 AC_CACHE_VAL(ac_cv_func_accept_arg1,dnl
 [AC_CACHE_VAL(ac_cv_func_accept_arg2,dnl
  [AC_CACHE_VAL(ac_cv_func_accept_arg3,dnl
   [for ac_cv_func_accept_arg1 in 'int' 'unsigned int'; do
     for ac_cv_func_accept_arg2 in 'struct sockaddr *' 'void *'; do
      for ac_cv_func_accept_arg3 in 'socklen_t *' 'size_t *' 'unsigned int *' 'int *'; do
       AC_TRY_COMPILE(dnl
[#ifdef HAVE_SYS_TYPES_H
#include <sys/types.h>
#endif
#ifdef HAVE_SYS_SOCKET_H
#include <sys/socket.h>
#endif
extern accept ($ac_cv_func_accept_arg1, $ac_cv_func_accept_arg2, $ac_cv_func_accept_arg3);],,dnl
        [ac_not_found=no ; break 3], ac_not_found=yes)
      done
     done
    done
   ])dnl AC_CACHE_VAL
  ])dnl AC_CACHE_VAL
 ])dnl AC_CACHE_VAL
 if test "$ac_not_found" = yes; then
  ac_cv_func_accept_arg1=int
  ac_cv_func_accept_arg2='struct sockaddr *'
  ac_cv_func_accept_arg3='socklen_t *'
 fi
 AC_MSG_RESULT([$ac_cv_func_accept_arg1, $ac_cv_func_accept_arg2, $ac_cv_func_accept_arg3])
 AC_DEFINE_UNQUOTED(ACCEPT_TYPE_ARG1,$ac_cv_func_accept_arg1)
 AC_DEFINE_UNQUOTED(ACCEPT_TYPE_ARG2,$ac_cv_func_accept_arg2)
 AC_DEFINE_UNQUOTED(ACCEPT_TYPE_ARG3,$ac_cv_func_accept_arg3)
])
