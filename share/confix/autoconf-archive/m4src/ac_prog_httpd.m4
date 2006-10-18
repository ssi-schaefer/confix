dnl @synopsis AC_PROG_HTTPD
dnl
dnl Check for Apache's 'httpd', let script continue if exists & works,
dnl pops up error message if not.
dnl
dnl Testing of functionality is by checking its compile settings
dnl
dnl Besides checking existence, this macro also set these environment
dnl variables upon completion:
dnl
dnl     HTTPD                    = which httpd
dnl     HTTPD_ROOT               = Apache's root directory, specified when compiled / run with -d option
dnl     HTTPD_SERVER_ROOT        = Directory for Apache's essential files, e.g. access logs / error logs / modules / scripts.
dnl     HTTPD_SERVER_CONFIG_FILE = Full-path of the 'httpd.conf' file
dnl     HTTPD_USER               = Which user that httpd runs as
dnl     HTTPD_GROUP              = Which group that httpd runs as
dnl     HTTPD_DOC_HOME           = Document directory, taken as the first DocumentRoot path found in httpd.conf
dnl     HTTPD_SCRIPT_HOME        = CGI script directory, taken as the first ScriptAlias path found in httpd.conf
dnl
dnl @category InstalledPackages
dnl @author Gleen Salmon <gleensalmon@yahoo.com>
dnl @version 2002-10-10
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_HTTPD],[
AC_REQUIRE([AC_EXEEXT])dnl
AC_PATH_PROG(HTTPD, httpd$EXEEXT, nocommand)
if test "$HTTPD" = nocommand; then
        AC_MSG_ERROR([httpd not found in $PATH])
fi
HTTPD_ROOT=`httpd -V | grep HTTPD_ROOT | sed 's/^.*HTTPD_ROOT[[[:blank:]]]*=[[[:blank:]]]*"\(.*\)"$/\1/'`
HTTPD_SERVER_CONFIG_FILE=`httpd -V | grep SERVER_CONFIG_FILE | sed 's/^.*SERVER_CONFIG_FILE[[[:blank:]]]*=[[[:blank:]]]*"\(.*\)"$/\1/'`
if echo $HTTPD_SERVER_CONFIG_FILE | grep ^[[^/]] > /dev/null; then
        HTTPD_SERVER_CONFIG_FILE=$HTTPD_ROOT/$HTTPD_SERVER_CONFIG_FILE
fi
SERVER_ROOT_PATTERN='^[[[:blank:]]]*ServerRoot[[[:blank:]]][[[:blank:]]]*"\([[^"]]*\)"$'
HTTPD_USER_PATTERN='^User[[[:blank:]]][[[:blank:]]]*\([[^[:blank:]]][[^[:blank:]]]*\)$'
HTTPD_GROUP_PATTERN='^Group[[[:blank:]]][[[:blank:]]]*\([[^[:blank:]]][[^[:blank:]]]*\)$'
DOCUMENT_ROOT_PATTERN='^[[[:blank:]]]*DocumentRoot[[[:blank:]]][[[:blank:]]]*"\([[^"]]*\)"$'
SCRIPT_ALIAS_PATTERN='^[[[:blank:]]]*ScriptAlias[[[:blank:]]][[[:blank:]]]*[[^[:blank:]]][[^[:blank:]]]*[[[:blank:]]][[[:blank:]]]*"\([[^"]]*\)"$'
AC_CHECK_FILE($HTTPD_SERVER_CONFIG_FILE,
        [HTTPD_SERVER_ROOT=`grep $SERVER_ROOT_PATTERN $HTTPD_SERVER_CONFIG_FILE | head -n 1 | sed "s/$SERVER_ROOT_PATTERN/\1/" | sed s/[[/]]$//`;
                HTTPD_USER=`grep $HTTPD_USER_PATTERN $HTTPD_SERVER_CONFIG_FILE | sed "s/$HTTPD_USER_PATTERN/\1/"`;
                HTTPD_GROUP=`grep $HTTPD_GROUP_PATTERN $HTTPD_SERVER_CONFIG_FILE | sed "s/$HTTPD_GROUP_PATTERN/\1/"`;
                HTTPD_DOC_HOME=`grep $DOCUMENT_ROOT_PATTERN $HTTPD_SERVER_CONFIG_FILE | head -n 1 | sed "s/$DOCUMENT_ROOT_PATTERN/\1/" | sed s/[[/]]$//`;
                HTTPD_SCRIPT_HOME=`grep $SCRIPT_ALIAS_PATTERN $HTTPD_SERVER_CONFIG_FILE | head -n 1 | sed "s/$SCRIPT_ALIAS_PATTERN/\1/" | sed s/[[/]]$//`],
        AC_MSG_ERROR([httpd server-config-file (detected as $HTTPD_SERVER_CONFIG_FILE by httpd -V) cannot be found]))dnl
])
