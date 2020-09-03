dnl @synopsis ACLTX_PACKAGES(PACKAGESNAMES,CLASSNAME,VARIABLETOSET[,ACTION-IF-FOUND[,ACTION-IF-NOT-FOUND]])
dnl
dnl This package search for the first suitable package in PACKAGESNAMES
dnl (comma separated list) with class CLASSNAME and set VARIABLETOSET
dnl the package found or to no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-08-20
dnl @license LGPL

define(_ACLTX_PACKAGE_INTERNE,[
	ifelse($#,0,[],$#,1,[],$#,2,[],$#,3,[
		ACLTX_PACKAGE($3,$2,$1)
	],[
		ACLTX_PACKAGE($3,$2,$1)
		if test "$$1" = "yes";
		then
			$1=$3 ; export $1 ;
		else
			_ACLTX_PACKAGE_INTERNE($1,$2,m4_shift(m4_shift(m4_shift($@))))
		fi;
	])
])

AC_DEFUN([ACLTX_PACKAGES],[
	_ACLTX_PACKAGE_INTERNE($3,$2,$1)
	AC_SUBST($3)
ifelse($#,3,[],$#,4,[
    if test "[$]$3" != "no" ;
    then
        $4
    fi
],$#,5,[
    ifelse($4,[],[
        if test "[$]$3" = "no" ;
        then
            $5
        fi
    ],[
        if test "[$]$3" != "no" ;
        then
            $4
        else
            $5
        fi
    ])
])
])
