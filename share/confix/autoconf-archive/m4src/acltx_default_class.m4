dnl @synopsis ACLTX_DEFAULT_CLASS([OTHER-DEFAULT-CLASS])
dnl
dnl This class search for the first suitable class in book report
dnl article and set defaultclass to this value If no one of this
dnl classes are found, fail
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_DEFAULT_CLASS],[
    if test "$acltx_cv_latex_class_default" = "" ; then
        ACLTX_CLASSES([m4_ifval([$1],[$1,])book,report,article],defaultclass)
    fi
    AC_MSG_CHECKING([for a default class in m4_ifval([$1],[$1,])book,report,article])
    AC_CACHE_VAL(acltx_cv_latex_class_default,[
        acltx_cv_latex_class_default=$defaultclass;
    ])
    AC_MSG_RESULT($defaultclass)
    AC_SUBST(defaultclass)
    if test "$defaultclass" = "no" ; then
        AC_MSG_ERROR([Unable to locate a default class])
    fi
])
