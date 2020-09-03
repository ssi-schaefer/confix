dnl @synopsis ACLTX_PACKAGE_FONTENC([ACTION-IF-NOT-FOUND])
dnl
dnl Check if the package fontenc exists and try to use T1 or OT1 and
dnl set fontenc to T1, OT1 or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

define(_ACLTX_PACKAGE_FONTENC_INTERNE,[changequote(*, !)dnl
\documentclass{$defaultclass}
\usepackage[$1]{fontenc}
\begin{document}
\end{document}dnl
changequote([, ])])

AC_DEFUN([ACLTX_PACKAGE_FONTENC],[
    AC_REQUIRE([ACLTX_DEFAULT_CLASS])
    ACLTX_PACKAGE_LOCATION(fontenc.sty,fontenc_location)
    AC_CACHE_CHECK([for fontenc],[ac_cv_latex_package_fontenc_opt],[
        _ACLTX_TEST([_ACLTX_PACKAGE_FONTENC_INTERNE(T1)],[ac_cv_latex_package_fontenc_opt])
        if test $ac_cv_latex_package_fontenc_opt = "yes" ;
        then
            ac_cv_latex_package_fontenc_opt="T1"; export ac_cv_latex_package_fontenc_opt;
        else
            _ACLTX_TEST([_ACLTX_PACKAGE_FONTENC_INTERNE(OT1)],[ac_cv_latex_package_fontenc_opt])
            if test $ac_cv_latex_package_fontenc_opt = "yes" ;
            then
                ac_cv_latex_package_fontenc_opt="OT1"; export ac_cv_latex_package_fontenc_opt;
            fi
        fi

    ])
    if test $ac_cv_latex_package_fontenc_opt = "no" ;
    then
        m4_ifval([$1],$1,[AC_MSG_ERROR([Unable to use fontenc with T1 nor OT1])])
    fi
    fontenc=$ac_cv_latex_package_fontenc_opt ; export fontenc ;
    AC_SUBST(fontenc)
])
