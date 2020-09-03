dnl @synopsis AX_WITH_APXS([value-if-not-found], [path])
dnl
dnl Locates an installed apxs binary, placing the result in the
dnl precious variable $APXS. Accepts a preset $APXS, then --with-apxs,
dnl and failing that searches for apxs in the given path (which
dnl defaults to the system path). If apxs is found, $APXS is set to the
dnl full path of the binary; otherwise it is set to VALUE-IF-NOT-FOUND,
dnl which defaults to apxs.
dnl
dnl Example:
dnl
dnl   AX_WITH_APXS(missing)
dnl
dnl @category InstalledPackages
dnl @author Dustin Mitchell <dustin@cs.uchicago.edu>
dnl @version 2005-01-22
dnl @license GPLWithACException

AC_DEFUN([AX_WITH_APXS],
[
  AC_ARG_VAR([APXS])

  dnl unless APXS was supplied to us (as a precious variable)
  if test -z "$APXS"
  then
    AC_MSG_CHECKING(for --with-apxs)
    AC_ARG_WITH(apxs,
                AC_HELP_STRING([--with-apxs=APXS],
                               [absolute path name of apxs executable]),
                [ if test "$withval" != "yes"
                  then
                    APXS="$withval"
                    AC_MSG_RESULT($withval)
                  else
                    AC_MSG_RESULT(no)
                  fi
                ],
                [ AC_MSG_RESULT(no)
                ])
  fi

  dnl if it's still not found, check the paths, or use the fallback
  if test -z "$APXS"
  then
    AC_PATH_PROG([APXS], apxs, m4_ifval([$1],[$1],[apxs]), $2)
  fi
])
