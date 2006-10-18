dnl @synopsis AC_NUMERIC_NAMEDLEVEL(VARNAME [,FROMVAR [,DEFAULT [,YESLEVEL]]])
dnl
dnl the levelstring FROMVAR is expanded and checked for verbal names
dnl that will map on to eight different levels - the VARNAME will
dnl receive this numeric level where "all" maps to 7 (lower three bits
dnl set) higher levels for 8 and 9 exist too. This macro is a nice
dnl helper to convert user input of a --with-opt=level into a numeric
dnl form. which can be simply pushed as a #define like with AC_DEFINE
dnl
dnl  default YESLEVEL = 2 /* including unknown levelspec */
dnl  default DEFAULT  = 0 /* when named level is empty */
dnl  default FROMVAR  = VARNAME
dnl
dnl The DEFAULT value is used if the NAMED levelstring has become empty
dnl and it is copied without further conversion - a default of "0" is
dnl used if absent - identical to "no". A "yes" will be set to the
dnl YESLEVEL - and note that "yes" has "2" as its default value not
dnl "1". (which comes from its original use to set a "gcc -O2").
dnl
dnl the mnemonic names are:
dnl
dnl    9| insane |ultrasome|experimentalplus
dnl    8| ultra  |ultra|experimental)
dnl    7| all    |muchmore|somemanymore|manymoreplus
dnl    6| most   |manymore|most)
dnl    5| strict |somemore|almost
dnl    4| more   |more
dnl    3| extra  |manyplus|plusmuch|somemany|plusmany
dnl    2| many   |many|much|(yes)
dnl    1| some   |some|plus
dnl
dnl note that a level can be construcct of (some|plus) = bit-0,
dnl (many|much) = bit-1, (more) = bit-2, (ultra|experimental) = bit-3
dnl atleast in a left-to-right order, ie. plusmanymore=7
dnl
dnl example usage:
dnl
dnl    AC_NUMERIC_NAMEDLEVEL(OPTLEVEL,with_optlevel,1,3)
dnl    AC_DEFINE(OPTLEVEL)
dnl    test "$GCC" = "yes" && CFLAGS="$CFLAGS -O$OPTLEVEL)
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2005-01-21
dnl @license GPLWithACException

AC_DEFUN([AC_NUMERIC_NAMEDLEVEL],
[dnl the names to be defined...
$1="ifelse($1,,[$]$2,[$]$1)" ; $1="[$]$1"
$1="[$]$1" ; $1="[$]$1"
if test "_[$]$1" = "_" ; then
  $1="ifelse([$3],,0,[$3])"
elif test "_[$]$1" = "_yes" ; then
  $1="ifelse([$4],,2,[$4])"
else
  $1=`echo [$]$1 | sed -e 's,some,plus,' -e 's,experimental,ultra,' -e 's,over,ultra,' -e 's,much,many,'`
  case "[$]$1" in
    0*|1*|2*|3*|4*|5*|6*|7*|8*|9*|-*|+*) ;;   # leave as is
    insane|ultraplus|plusultra)                 $1="9" ;;
    ultra)                                      $1="8" ;;
    manymoreplus|manyplusmore|plusmanymore|all) $1="7" ;;
    moremanyplus|moreplusmany|plusmoremany)     $1="7" ;;
    manymore|moremany|most)                     $1="6" ;;
    somemore|moresome|almost)                   $1="5" ;;
    more)                                       $1="4" ;;
    manyplus|plusmany|extra)                    $1="3" ;;
    many)                                       $1="2" ;;
    plus)                                       $1="1" ;;
    no)                                         $1="0" ;;
    yes) $1="ifelse([$4],,2,[$4])" ;;
    *)   $1="ifelse([$3],,1,[$3])" ;; # for other unkown stuff.
  esac
fi
])
