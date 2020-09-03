dnl @synopsis AC_CXX_HAVE_FREEZE_SSTREAM
dnl
dnl Check if the compiler has (need) freeze method call in
dnl stringstream/ strstream. Seems that Win32 and STLPort have it,
dnl libstdc++ not ...
dnl
dnl Eg:
dnl
dnl   #include <sstream>
dnl   #ifdef HAVE_NAMESPACES
dnl   using namespace std;
dnl   #endif
dnl   #ifdef HAVE_SSTREAM
dnl   stringstream message;
dnl   #else
dnl   strstream message;
dnl   #endif
dnl   message << "Hello";
dnl   #ifdef HAVE_FREEZE_SSTREAM
dnl   message.freeze(0);
dnl   #endif
dnl
dnl @category Cxx
dnl @author Alain BARBET <alian@cpan.org>
dnl @version 2002-09-04
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_FREEZE_SSTREAM],
[AC_CACHE_CHECK(whether the compiler has freeze in stringstream,
ac_cv_cxx_have_freeze_sstream,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_REQUIRE([AC_CXX_HAVE_SSTREAM])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <sstream>
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],
[#ifdef HAVE_SSTREAM
stringstream message;
#else
strstream message;
#endif
message << "Hello"; message.freeze(0); return 0;],
  ac_cv_cxx_have_freeze_sstream=yes, ac_cv_cxx_have_freeze_sstream=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_freeze_sstream" = yes; then
   AC_DEFINE(HAVE_FREEZE_SSTREAM,,[define if the compiler has freeze in
stringstream])
fi
])
