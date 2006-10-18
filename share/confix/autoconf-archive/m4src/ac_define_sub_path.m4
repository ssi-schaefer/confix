dnl @synopsis AC_DEFINE_SUB_PATH(DEFNAME, varname, description)
dnl
dnl Look at varname and detect the subpath that it contains relative to
dnl $prefix/$exec_prefix. If the path is indeed relative to
dnl $prefix/$exec_prefix, then a single "./" (dotslash) is prepended,
dnl otherwise it can be seen as an absolute path that can not be moved,
dnl which you possibly do for "/etc" files, or even those ending up in
dnl "/lib/modules" or "/winnt/system".
dnl
dnl This macro is not very intelligent, it's just a first try in this
dnl direction. It does currently just look into the current patterns,
dnl and replaces a ${prefix} with a simple dot. Amazingly, it works
dnl quite well for most packages.
dnl
dnl Example (configure.ac):
dnl
dnl    AC_DEFINE_DIR([EPREFIX], [exec_prefix], [--exec-prefix or default])
dnl    AC_DEFINE_SUB_PATH([PATH_LIBDIR], [libdir], [--bindir subdir])
dnl    AC_DEFINE_UNQUOTED([PACKAGE],"$PACKAGE", [Name of package])
dnl
dnl Example (in C):
dnl
dnl    static const char _libdir[] = PATH_LIBDIR; /* configure default */
dnl    char* libdir;
dnl    char* eprefix = getenv (PACKAGE "DIR");
dnl    if (! eprefix) eprefix = EPREFIX; /* default */
dnl    if (*_libdir != '.') libdir = strdup(_libdir);
dnl    else {
dnl       libdir = malloc(strlen(eprefix) + strlen(_libdir) + 2);
dnl       strcpy(libdir, eprefix);
dnl       strcat(libdir, PATH_DELIMITER_STRING);
dnl       strcat(libdir, _libdir);
dnl    }
dnl    ...
dnl    free (libdir);
dnl
dnl The AC_DEFINE_SUB_PATHS(varnames) macro looks for the given various
dnl install-paths that largely depend on either ${prefix} or
dnl ${exec_prefix}. Just cut out the prefix and ac_define the value.
dnl The value is uppercased and PATH_ prepended ie.
dnl ac_define_sub_paths(bindir libdir pkgdatadir) will create the
dnl defines PATH_BINDIR PATH_LIBDIR PATH_PKGDATADIR - see posix'
dnl include/paths.h that creates _PATH_DEV and friends.
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2001-07-26
dnl @license GPLWithACException

AC_DEFUN([AC_DEFINE_SUB_PATH],
[dnl
  test "_$prefix" = _NONE && prefix="$ac_default_prefix"
  test "_$exec_prefix" = _NONE && exec_prefix='${prefix}'
  P=`echo ifelse( $2, , [$]$1, [$]$2) | sed -e 's:^\${[a-z_]*prefix}:.:'`
  ifelse ($3, ,
    AC_DEFINE($1, $P, [sub path $2]),
    AC_DEFINE($1, $P, $3))
])

AC_DEFUN([AC_DEFINE_SUB_PATHS],
[dnl
  test "_$prefix" = _NONE && prefix="$ac_default_prefix"
  test "_$exec_prefix" = _NONE && exec_prefix='${prefix}'
  for i in $1 ; do
  P=`echo \$$i | sed -e 's:^\${[a-z_]*prefix}:.:'`
  V=`echo path_$i | sed -e 'y:abcdefghijklmnopqrstuvwxyz:ABCDEFGHIJKLMNOPQRSTUVWXYZ:'`
    AC_DEFINE($V, $P, [sub path $i]),
])
