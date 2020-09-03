dnl @synopsis ETR_SYSV_IPC
dnl
dnl This macro checks for the SysV IPC header files. It only checks
dnl that you can compile a program with them, not whether the system
dnl actually implements working SysV IPC.
dnl
dnl @category Misc
dnl @author Warren Young <warren@etr-usa.com>
dnl @version 2001-05-25
dnl @license AllPermissive

AC_DEFUN([ETR_SYSV_IPC],
[
AC_CACHE_CHECK([for System V IPC headers], ac_cv_sysv_ipc, [
        AC_TRY_COMPILE(
                [
                        #include <sys/types.h>
                        #include <sys/ipc.h>
                        #include <sys/msg.h>
                        #include <sys/sem.h>
                        #include <sys/shm.h>
                ],, ac_cv_sysv_ipc=yes, ac_cv_sysv_ipc=no)
])

        if test x"$ac_cv_sysv_ipc" = "xyes"
        then
                AC_DEFINE(HAVE_SYSV_IPC, 1, [ Define if you have System V IPC ])
        fi
]) dnl ETR_SYSV_IPC
