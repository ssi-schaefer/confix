dnl @synopsis ACLTX_CONVERTING_PNG_EPS([ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl this macro find a way to convert png to eps file If the way is
dnl found, set png_to_eps to this way else set png_to_eps to no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_CONVERTING_PNG_EPS],[
ACLTX_PROG_PNGTOPNM([AC_MSG_WARN([Unable to locate a pngtopnm application to convert png file])])
ACLTX_PROG_PNMTOPS([AC_MSG_WARN([Unable to locate a pnmtops application to convert png file])])
AC_MSG_CHECKING(for a way to convert png file to eps file)
png_to_eps='no'; export png_to_eps;
if test "$pngtopnm" != "no" -a "$pnmtops" != "no" ; then
    png_to_eps="%.eps : %.png ; $pngtopnm \[$]*.png | pnmtops -noturn -nocenter -scale 1.00 - >\[$]*.eps"
fi;
AC_MSG_RESULT($png_to_eps)
AC_SUBST(png_to_eps)
ifelse($#,0,[],$#,1,[
    if test "$png_to_eps" = "yes" ;
    then
        $1
    fi
],$#,2,[
    ifelse($1,[],[
        if test "$png_to_eps" = "no" ;
        then
            $2
        fi
    ],[
        if test "$png_to_eps" = "yes" ;
        then
            $1
        else
            $2
        fi
    ])
])
])
