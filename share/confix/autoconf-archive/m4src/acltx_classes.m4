dnl @synopsis ACLTX_CLASSES(CLASSESNAMES,VARIABLETOSET[,ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl This class search for the first suitable package in CLASSESNAMES
dnl (comma separated list) and set VARIABLETOSET to the class found or
dnl to no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

define(_ACLTX_CLASSES_INTERNE,[
	ifelse($#,1,[],$#,2,[
		ACLTX_CLASS($2,$1)
	],[
		ACLTX_CLASS($2,$1)
		if test "$$1" = "yes";
		then
			$1=$2 ; export $1 ;
		else
			_ACLTX_CLASSES_INTERNE($1,m4_shift(m4_shift($@)))
		fi;
	])
])

AC_DEFUN([ACLTX_CLASSES],[
	_ACLTX_CLASSES_INTERNE($2,$1)
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
