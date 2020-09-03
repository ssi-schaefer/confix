dnl @synopsis AC_SYS_DEV_POLL([ACTION-IF-FOUND], [ACTION-IF-NOT-FOUND])
dnl
dnl This macro tests for the presence of /dev/poll support in the build
dnl environment. It checks that the needed structure (dvpoll) is
dnl available, with the standard fields. /dev/poll is most often seen
dnl under Solaris.
dnl
dnl Note that it does not attempt to actually open /dev/poll -- you
dnl should test for errors when you open it and then fall back to
dnl poll() if it is unavailable.
dnl
dnl @category Misc
dnl @author Dave Benson <daveb@ffem.org>
dnl @version 2003-10-29
dnl @license AllPermissive

AC_DEFUN([AC_SYS_DEV_POLL], [AC_CACHE_CHECK(for /dev/poll support, ac_cv_dev_poll,
    AC_TRY_COMPILE([#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/poll.h>
#include <sys/devpoll.h>],
[
  struct dvpoll p;
  p.dp_timeout = 0;
  p.dp_nfds = 0;
  p.dp_fds = (struct pollfd *) 0;
  return 0;
],
    ac_cv_dev_poll=yes
    [$1],
    ac_cv_dev_poll=no
    [$2]
    )
  )
])
