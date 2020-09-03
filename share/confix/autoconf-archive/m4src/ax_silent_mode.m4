dnl @synopsis AX_SILENT_MODE(on|off)
dnl
dnl @summary Temporarily disable console output.
dnl
dnl Temporarily disable console output when running Autoconf macros.
dnl For example:
dnl
dnl   AX_SILENT_MODE(on)    dnl disable console output
dnl   AC_PROG_CXX
dnl   AX_SILENT_MODE(off)   dnl enable console output
dnl   AC_PROG_RANLIB
dnl
dnl @category Misc
dnl @author Peter Simons <simons@cryp.to>
dnl @author Paolo Bonzini
dnl @version 2006-06-04
dnl @license AllPermissive

AC_DEFUN([AX_SILENT_MODE],
  [
  case "$1" in
    on)
      exec 6>/dev/null
      ;;
    off)
      exec 6>&1
      ;;
    *)
      AC_MSG_ERROR([Silent mode can only be switched "on" or "off".])
      ;;
  esac
  ])dnl
