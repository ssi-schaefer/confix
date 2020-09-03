dnl @synopsis AX_CONFIG_FEATURE(FEATURE-NAME, FEATURE-DESCRIPTION, DEFINE, DEFINE-DESCRIPTION, [ACTION-IF-ENABLED [, ACTION-IF-NOT-ENABLED]])
dnl
dnl AX_CONFIG_FEATURE is a simple wrapper for AC_ARG_ENABLE, it enables
dnl the feature FEATURE-NAME and AC_DEFINEs the passed DEFINE,
dnl depending on the user choice. DESCRIPTION will be used for
dnl AC_DEFINEs. ACTION-IF-ENABLED and ACTION-IF-NOT-ENABLED are the
dnl actions that will be run. A feature is enabled by default, in order
dnl to change this behaviour use the AX_CONFIG_FEATURE_DEFAULT_ENABLED
dnl and AX_CONFIG_FEATURE_DEFAULT_DISABLED macros.
dnl
dnl A simple example:
dnl
dnl     AX_CONFIG_FEATURE_DEFAULT_ENABLED
dnl     AX_CONFIG_FEATURE(feature_xxxxx, [turns on/off XXXXX support],
dnl     		  HAVE_XXXXX, [Define if you want XXXXX support])
dnl
dnl     ...
dnl
dnl     AX_CONFIG_FEATURE_DEFAULT_DISABLED
dnl     AX_CONFIG_FEATURE(feature_yyyyy, [turns on/off YYYYY support],
dnl                       HAVE_YYYYY, [Define if you want YYYYY support],
dnl     		  [enable_yyyyy="yes"], [enable_yyyyy="no"])
dnl     AM_CONDITIONAL(YYYYY, [test "$enable_yyyyy" = "yes"])
dnl
dnl     AX_CONFIG_FEATURE_DEFAULT_ENABLED
dnl     AX_CONFIG_FEATURE(...)
dnl
dnl     ...
dnl
dnl If you have lot of features and you want a verbose dumping of each
dnl user selection use AX_CONFIG_FEATURE_VERBOSE. Use
dnl AX_CONFIG_FEATURE_SILENT in order to remove a previously
dnl AX_CONFIG_FEATURE_VERBOSE. By default features are silent.
dnl
dnl Use AX_CONFIG_FEATURE_ENABLE or AX_CONFIG_FEATURE_DISABLE in order
dnl to enable or disable a specific feature.
dnl
dnl Another simple example:
dnl
dnl     AS_IF([some_test_here],[AX_CONFIG_FEATURE_ENABLE(feature_xxxxx)],[])
dnl
dnl     AX_CONFIG_FEATURE(feature_xxxxx, [turns on/off XXXXX support],
dnl     		  HAVE_XXXXX, [Define if you want XXXXX support])
dnl     AX_CONFIG_FEATURE(feature_yyyyy, [turns on/off YYYYY support],
dnl                       HAVE_YYYYY, [Define if you want YYYYY support],
dnl     		  [enable_yyyyy="yes"], [enable_yyyyy="no"])
dnl
dnl     ...
dnl
dnl NOTE: AX_CONFIG_FEATURE_ENABLE() must be placed first of the
dnl relative AX_CONFIG_FEATURE() macro ...
dnl
dnl @category Misc
dnl @author Francesco Salvestrini <salvestrini@users.sourceforge.net>
dnl @version 2005-01-22
dnl @license GPLWithACException

AC_DEFUN([AX_CONFIG_FEATURE],[ dnl
m4_pushdef([FEATURE], patsubst([$1], -, _))dnl

AC_ARG_ENABLE([$1],AC_HELP_STRING([--enable-$1],[$2]),[
case "${enableval}" in
   yes)
     ax_config_feature_[]FEATURE[]="yes"
     ;;
   no)
     ax_config_feature_[]FEATURE[]="no"
     ;;
   *)
     AC_MSG_ERROR([bad value ${enableval} for feature --$1])
     ;;
esac
])

AS_IF([test "$ax_config_feature_[]FEATURE[]" = yes],[ dnl
  AC_DEFINE([$3])
  $5
  AS_IF([test "$ax_config_feature_verbose" = yes],[ dnl
    AC_MSG_NOTICE([Feature $1 is enabled])
  ])
],[ dnl
  $6
  AS_IF([test "$ax_config_feature_verbose" = yes],[ dnl
    AC_MSG_NOTICE([Feature $1 is disabled])
  ])
])

AH_TEMPLATE([$3],[$4])

m4_popdef([FEATURE])dnl
])

dnl Feature global
AC_DEFUN([AX_CONFIG_FEATURE_VERBOSE],[ dnl
  ax_config_feature_verbose=yes
])

dnl Feature global
AC_DEFUN([AX_CONFIG_FEATURE_SILENT],[ dnl
  ax_config_feature_verbose=no
])

dnl Feature specific
AC_DEFUN([AX_CONFIG_FEATURE_DEFAULT_ENABLED], [
  ax_config_feature_[]FEATURE[]_default=yes
])

dnl Feature specific
AC_DEFUN([AX_CONFIG_FEATURE_DEFAULT_DISABLED], [
  ax_config_feature_[]FEATURE[]_default=no
])

dnl Feature specific
AC_DEFUN([AX_CONFIG_FEATURE_ENABLE],[ dnl
  ax_config_feature_[]patsubst([$1], -, _)[]=yes
])

dnl Feature specific
AC_DEFUN([AX_CONFIG_FEATURE_DISABLE],[ dnl
  ax_config_feature_[]patsubst([$1], -, _)[]=yes
])
