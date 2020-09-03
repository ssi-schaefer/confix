dnl @synopsis VL_PROG_FIG2DEV
dnl
dnl If `fig2dev' is found, sets the output variable `FIG2DEV' to
dnl `fig2dev', and `FIG2DEV_ESPLANG' to the graphics language which can
dnl be used to produce Encapsulated PostScript. Older versions of
dnl `fig2dev' produce EPS with `-Lps' and new versions with `-Leps',
dnl this macro finds out the correct language option automatically.
dnl
dnl @category InstalledPackages
dnl @author Ville Laurikari <vl@iki.fi>
dnl @version 2002-04-04
dnl @license AllPermissive

AC_DEFUN([VL_PROG_FIG2DEV], [
  AC_CHECK_PROG(FIG2DEV, fig2dev, fig2dev)
  if test "x$FIG2DEV" != "x"; then
    AC_CACHE_CHECK(how to produce EPS with fig2dev,
                   vl_cv_sys_fig2dev_epslang, [
      if "$FIG2DEV" -Leps /dev/null 2>&1 | grep Unknown > /dev/null; then
        vl_cv_sys_fig2dev_epslang=ps
      else
        vl_cv_sys_fig2dev_epslang=eps
      fi
    ])
    FIG2DEV_EPSLANG=$vl_cv_sys_fig2dev_epslang
    AC_SUBST(FIG2DEV_EPSLANG)
  fi
])
