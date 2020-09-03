dnl @synopsis ACX_FUNC_FORK
dnl
dnl Check to for a working fork. Use to provide a workaround for
dnl systems that don't have a working fork. For example, the workaround
dnl for the fork()/exec() sequence for DOS is to use spawn.
dnl
dnl Defines HAVE_NO_FORK is fork() doesn't work or isn't implemented.
dnl
dnl @category Misc
dnl @author Mark Elbrecht <snowball3@bigfoot.com>
dnl @version 2000-07-19
dnl @license GPLWithACException

AC_DEFUN([ACX_FUNC_FORK],
[AC_MSG_CHECKING(for a working fork)
AC_CACHE_VAL(acx_cv_func_fork_works,
[AC_REQUIRE([AC_TYPE_PID_T])
AC_REQUIRE([AC_HEADER_SYS_WAIT])
AC_TRY_RUN([#include <sys/types.h>
#ifdef HAVE_SYS_WAIT_H
#include <sys/wait.h>
#endif
#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

int main()
{
  int status;
  pid_t child = fork();

  if (child < 0) /* Error */
    return (1);
  else if (child == 0) /* Child */
    return (0);

  /* Parent */
  status = (wait(&status) != child);
  return  (status >= 0) ? 0 : 1;
}
], acx_cv_func_fork_works=yes, acx_cv_func_fork_works=no, acx_cv_func_fork_works=no)
])
AC_MSG_RESULT($acx_cv_func_fork_works)
if test $acx_cv_func_fork_works = no; then
  AC_DEFINE(HAVE_NO_FORK)
fi
])
