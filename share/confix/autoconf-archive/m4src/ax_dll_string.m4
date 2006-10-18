dnl @synopsis AX_DLL_STRING
dnl
dnl @summary Tests for a bug currently in g++ 3.4.4 on Cygwin where passing an empty std::string to a dll will cause a crash on destruction.
dnl
dnl Tests for a bug currently in g++ 3.4.4 on Cygwin (maybe other
dnl targets with statically linked libstdc++?) where passing an empty
dnl std::string to a dll will cause a crash on destruction due to
dnl incorrect memory handling. See bug 24196 in gcc's bugzilla for more
dnl details: http://gcc.gnu.org/bugzilla/show_bug.cgi?id=24196
dnl
dnl @category Cxx
dnl @author Steven Brown <swbrown@variadic.org>
dnl @version 2006-04-08
dnl @license AllPermissive

dnl Plan: compile conftest-dll.cc, conftest-exe.cc.  It has a 'crash' param
dnl that can be passed.  Verify the compile worked and we can run it normally
dnl ok.  Then, pass 'crash', test if it crashed, fail.

AC_DEFUN([AX_DLL_STRING],
[
  AC_MSG_CHECKING(if the dll string test can be compiled)
  cat << EOF > conftest-dll.cc
[
#include <string>
using namespace std;

void testit(std::string (*contentGet)()) {
  contentGet();
}
]
EOF
  cat << EOF > conftest-exe.cc
[
#include <string>
#include <cstring>
using namespace std;

extern void testit(std::string (*contentGet)());

std::string contentGet() {
  return string(""); // Anything other than empty string works.
}

int main(int argc, char *argv[]) {
  if(argc == 2 && strcmp(argv[1], "crash") == 0) {
    testit(&contentGet);
  }
  return 0;
}
]
EOF
  $CXX -shared $CFLAGS $CPPFLAGS conftest-dll.cc -o conftest-dll.dll >&AS_MESSAGE_LOG_FD && $CXX $CFLAGS $CPPFLAGS conftest-exe.cc conftest-dll.dll -o conftest-exe.exe >& AS_MESSAGE_LOG_FD
  if test x"$?" = x"0"; then
    AC_MSG_RESULT(yes)

    dnl Make sure it runs normally first.
    AC_MSG_CHECKING(if the dll string test is usable)
    if /bin/sh -c "(LD_LIBRARY_PATH=\"$PWD\" ./conftest-exe.exe)" >& AS_MESSAGE_LOG_FD 2>&1; then
      AC_MSG_RESULT(yes)

      dnl Now we can check for the bug.
      AC_MSG_CHECKING(if the dll string test is affected by gcc bug 24196)
      if ! /bin/sh -c "(LD_LIBRARY_PATH=\"$PWD\" ./conftest-exe.exe crash)" >& AS_MESSAGE_LOG_FD 2>&1; then
        AC_MSG_RESULT(yes)

        dnl We have the bug, user'll need to fix it.
        AC_MSG_ERROR([*** This toolchain is affected by gcc bug 24196.  For Cygwin as of 4/8/2006, you can downgrade to gcc/g++ 3.3.3 or check if there is a newer compiler available that's fixed.])
      else
        AC_MSG_RESULT(no)
      fi
    else
      AC_MSG_RESULT(no)
    fi
  else
    AC_MSG_RESULT(no)
  fi
])
