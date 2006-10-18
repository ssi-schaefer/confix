dnl @synopsis ACLTX_PACKAGE_BABEL([ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl Check if the package babel exists and set babel to yes or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PACKAGE_BABEL],[
AC_REQUIRE([ACLTX_DEFAULT_CLASS])
AC_CACHE_CHECK([for babel with class $defaultclass],[ac_cv_latex_package_f_babel],[
_ACLTX_TEST([changequote(*, !)dnl
\documentclass{$defaultclass}
\usepackage[english]{babel}
\begin{document}
\end{document}dnl
changequote([, ])],[ac_cv_latex_package_f_babel])
])
babel=$[ac_cv_latex_package_f_babel]; export babel;
AC_SUBST(babel)
ifelse($#,0,[],$#,1,[
    if test "$babel" != "no" ;
    then
        $1
    fi
],$#,2,[
    ifelse($1,[],[
        if test "babel" = "no" ;
        then
            $2
        fi
    ],[
        if test "babel" != "no" ;
        then
            $1
        else
            $2
        fi
    ])
])
])
