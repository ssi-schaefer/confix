dnl @synopsis ACLTX_CONVERTING_JPG_EPS([ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl this macro find a way to convert jpg to eps file If the way is
dnl found, set jpg_to_eps to this way else set jpg_to_eps to no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_CONVERTING_JPG_EPS],[
ACLTX_PROG_JPEGTOPNM([AC_MSG_WARN([Unable to locate a jpegtopnm application to convert jpg file])])
ACLTX_PROG_PNMTOPS([AC_MSG_WARN([Unable to locate a pnmtops application to convert jpg file])])
AC_MSG_CHECKING(for a way to convert jpg file to eps file)
jpg_to_eps='no'; export jpg_to_eps;
if test "$jpegtopnm" != "no" -a "$pnmtops" != "no" ; then
    jpg_to_eps="%.eps : %.jpg ; $jpegtopnm \[$]*.jpg | pnmtops -noturn -nocenter -scale 1.00 - >\[$]*.eps"
fi;
AC_MSG_RESULT($jpg_to_eps)
AC_SUBST(jpg_to_eps)
ifelse($#,0,[],$#,1,[
    if test "$jpg_to_eps" = "yes" ;
    then
        $1
    fi
],$#,2,[
    ifelse($1,[],[
        if test "$jpg_to_eps" = "no" ;
        then
            $2
        fi
    ],[
        if test "$jpg_to_eps" = "yes" ;
        then
            $1
        else
            $2
        fi
    ])
])
])
