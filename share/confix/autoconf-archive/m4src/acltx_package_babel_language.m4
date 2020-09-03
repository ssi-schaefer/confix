dnl @synopsis ACLTX_PACKAGE_BABEL_LANGUAGE(LANGUAGES,VARIABLETOSET[ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl Check if the package babel exists and support language and set
dnl VARIABLETOSET to yes or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PACKAGE_BABEL_LANGUAGE],[
ACLTX_PACKAGE_BABEL([],[AC_MSG_WARN([Unable to locate babel with $defaultclass])])
AC_CACHE_CHECK([for babel with class $defaultclass and language $1],[ac_cv_latex_babel_langugage_]translit([$1],[-,{}()= ],[________]),[
_ACLTX_TEST([changequote(*, !)dnl
\documentclass{$defaultclass}
\usepackage[$1]{babel}
\begin{document}
\end{document}dnl
changequote([, ])],[ac_cv_latex_babel_langugage_]translit([$1],[-,{}()= ],[________]))
])
$2=$[ac_cv_latex_babel_langugage_]translit([$1],[-,{}()= ],[________]); export $2;
AC_SUBST($2)
ifelse($#,2,[],$#,3,[
    if test "[$]$2" != "no" ;
    then
        $3
    fi
],$#,4,[
    ifelse($3,[],[
        if test "[$]$2" = "no" ;
        then
            $4
        fi
    ],[
        if test "[$]$2" != "no" ;
        then
            $3
        else
            $4
        fi
    ])
])
])
