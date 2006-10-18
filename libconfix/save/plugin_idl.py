import core.debug
import libconfix.plugins.idl.dependency
import libconfix.plugins.idl.buildinfo

Require_IDL = libconfix.plugins.idl.dependency.Require_IDL
Provide_IDL = libconfix.plugins.idl.dependency.Provide_IDL
BuildInfo_IDL_NativeInstalled = libconfix.plugins.idl.buildinfo.BuildInfo_IDL_NativeInstalled
BuildInfo_IDL_NativeLocal = libconfix.plugins.idl.buildinfo.BuildInfo_IDL_NativeLocal
BuildInfo_IDL_Native = libconfix.plugins.idl.buildinfo.BuildInfo_IDL_Native

core.debug.warn('class Require_IDL has been moved to libconfix.plugins.idl.dependency')
core.debug.warn('class Provide_IDL has been moved to libconfix.plugins.idl.dependency')
core.debug.warn('class BuildInfo_IDL_NativeInstalled has been moved to libconfix.plugins.idl.buildinfo')
core.debug.warn('class BuildInfo_IDL_NativeLocal has been moved to libconfix.plugins.idl.buildinfo')
core.debug.warn('class BuildInfo_IDL_Native has been moved to libconfix.plugins.idl.buildinfo')
