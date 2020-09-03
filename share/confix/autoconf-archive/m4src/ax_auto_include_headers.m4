dnl @synopsis AX_AUTO_INCLUDE_HEADERS(INCLUDE-FILE ...)
dnl
dnl Given a space-separated list of INCLUDE-FILEs,
dnl AX_AUTO_INCLUDE_HEADERS will output a conditional #include for each
dnl INCLUDE-FILE. The following example demonstrates how
dnl AX_AUTO_INCLUDE_HEADERS's might be used in a configure.ac script:
dnl
dnl     AH_BOTTOM([
dnl       AX_AUTO_INCLUDE_HEADERS([sys/resource.h invent.h sys/sysinfo.h])dnl
dnl     ])
dnl
dnl The preceding invocation instructs autoheader to put the following
dnl code at the bottom of the config.h file:
dnl
dnl     #ifdef HAVE_SYS_RESOURCE_H
dnl     # include <sys/resource.h>
dnl     #endif
dnl     #ifdef HAVE_INVENT_H
dnl     # include <invent.h>
dnl     #endif
dnl     #ifdef HAVE_SYS_SYSINFO_H
dnl     # include <sys/sysinfo.h>
dnl     #endif
dnl
dnl Note that AX_AUTO_INCLUDE_HEADERS merely outputs
dnl #ifdef/#include/#endif blocks. The configure.ac script still needs
dnl to invoke AC_CHECK_HEADERS to #define the various HAVE_*_H
dnl preprocessor macros.
dnl
dnl Here's an easy way to get from config.h a complete list of header
dnl files who existence is tested by the configure script:
dnl
dnl    cat config.h | perl -ane '/ HAVE_\S+_H / && do {$_=$F[$#F-1]; s/^HAVE_//; s/_H/.h/; s|_|/|g; tr/A-Z/a-z/; print "$_ "}'
dnl
dnl You can then manually edit the resulting list and incorporate it
dnl into one or more calls to AX_AUTO_INCLUDE_HEADERS.
dnl
dnl @category Misc
dnl @author Scott Pakin <scott+ac@pakin.org>
dnl @version 2005-01-21
dnl @license AllPermissive

AC_DEFUN([AX_AUTO_INCLUDE_HEADERS], [dnl
AC_FOREACH([AX_Header], [$1], [dnl
m4_pushdef([AX_IfDef], AS_TR_CPP(HAVE_[]AX_Header))dnl
[#]ifdef AX_IfDef
[#] include <AX_Header>
[#]endif
m4_popdef([AX_IfDef])dnl
])])
