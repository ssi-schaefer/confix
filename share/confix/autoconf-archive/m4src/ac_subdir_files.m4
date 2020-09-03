dnl @synopsis AC_SUBDIR_FILES [(SUBDIRS [, CASEPATTERN])]
dnl
dnl look into subdirs and copy the (real) files that match pattern into
dnl the local directory. Preferably we use a symbolic link of course.
dnl existing local files are not overwritten.
dnl
dnl the default casepattern is "*.?|*.cc|*.cpp" the default subdir-list
dnl contains all subdirs available
dnl
dnl (requires AC_PROG_CP_S)
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2003-10-29
dnl @license GPLWithACException

AC_DEFUN([AC_SUBDIR_FILES],
[AC_BEFORE($0,[AC_CP_S])
  for ac_subdir in ifelse([$1], , *, $1) ; do
    if test -d $ac_subdir ; then
      AC_MSG_CHECKING(subdir $ac_subdir)
      for ac_file in $ac_subdir/* ; do
	if test -f $ac_file ; then
	  if test ! -e `basename $ac_file` ; then
	    case `basename $ac_file` in
	      ifelse([$2], , *.?|*.cc|*.cpp,[$1]))
		AC_ECHO_N($ac_file,) ;
                $CP_S $ac_file . ;;
            esac
          fi
        fi
      done
      AC_MSG_RESULT(;)
    fi
  done
])
