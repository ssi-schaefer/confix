dnl @synopsis ACLTX_TEXMF_PATH
dnl
dnl This macros find a suitable path for the local texmf folder. It
dnl this possible to set manually this path using texmfpath=... The
dnl variable texmfpath contains the path found or. If configure is
dnl unable to locate the path, configure exit with a error message.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_TEXMF_PATH],[
AC_ARG_VAR(texmfpath,[specify default local texmf path (for example /usr/TeX/texmf-local/)])
AC_REQUIRE([ACLTX_PROG_LATEX])
AC_REQUIRE([AC_PROG_AWK])
AC_REQUIRE([ACLTX_CLASS_REPORT])
AC_CACHE_CHECK([for texmf local path],[ac_cv_texmfpath_value],[
if test "$ac_cv_env_texmfpath_set" = "set" ; then
    ac_cv_texmfpath_value="$ac_cv_env_texmfpath_value" ; export ac_cv_texmfpath_value;
else
    Base=`$kpsewhich report.cls` ; export Base ;
    Base=`echo $Base | $AWK -F / '{for(i=1;i<NF;i++) {if ($i=="texmf" || $i=="texmf-dist") break; OUT=OUT$i"/";} print OUT}'` ; export Base ;
    if test -x "$Base/texmf.local" ;
    then
        Base="$Base/texmf.local" ; export Base;
    else
        if test -x "$Base/texmf-local" ;
        then
            Base="$Base/texmf-local" ; export Base;
        else
            if test -x "$Base/texmf" ;
            then
                Base="$Base/texmf" ; export Base;
            else
                Base="no"; export Base;
            fi;
        fi;
    fi;
    ac_cv_texmfpath_value="$Base" ; export ac_cv_texmfpath_value;
fi
])
texmfpath=$ac_cv_texmfpath_value ; export texmfpath_value;
if test "$texmfpath" = "no" ;
then
    AC_MSG_ERROR([Unable to find a suitable local texmf folder. Use texmfpath=... to specify it])
fi
AC_SUBST(texmfpath)
])
