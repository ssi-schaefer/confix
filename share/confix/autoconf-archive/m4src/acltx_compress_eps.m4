dnl @synopsis ACLTX_COMPRESS_EPS([ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl this macro find a way to compress eps file, using Makefile target.
dnl If the way is found, set compress_eps to this way else set
dnl compress_eps to no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_COMPRESS_EPS],[
ACLTX_PROG_GZIP([AC_MSG_WARN([Unable to locate a gzip application to compress eps file])])
compress_eps=''; export compress_eps;
if test "$gzip" = "no" ; then
    AC_MSG_CHECKING(for a way to compress eps)
    AC_MSG_RESULT(no)
else
    AC_CHECK_PROGS(grep,grep,no)
    AC_MSG_CHECKING(for a way to compress eps)
    if test "$grep" = "no" ; then
    AC_MSG_RESULT(no)
    else
        compress_eps="%.eps.gz %.eps.bb : %.eps ; cat \[$]*.eps | grep \"%%BoundingBox\" > \[$]*.eps.bb ; rm -f \[$]*.eps.gz ; gzip \[$]*.eps"; export compress_eps
        AC_MSG_RESULT($compress_eps)
    fi;
fi;
AC_SUBST(compress_eps)
ifelse($#,0,[],$#,1,[
    if test "$compress_eps" != "no" ;
    then
        $1
    fi
],$#,2,[
    ifelse($1,[],[
        if test "$compress_eps" = "no" ;
        then
            $2
        fi
    ],[
        if test "$compress_eps" != "no" ;
        then
            $1
        else
            $2
        fi
    ])
])
])
