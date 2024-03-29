%define __provides_exclude_from '%{py_platsitedir}/(.*)\\.so$'

%define oname pwquality
%define major 1
%define libname %mklibname %{oname}
%define oldlibname %mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

# Workaround for libtool messing up badly on crosscompiles
# (spaces in $CC)
%if %{cross_compiling}
%define prefer_gcc 1
%endif

%bcond_without python

Summary:	Library for password quality checking and generating random passwords
Name:		libpwquality
Version:	1.4.5
Release:	2
License:	BSD
Group:		System/Libraries
Url:		https://github.com/libpwquality/libpwquality/
Source0:	https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/%{name}-%{version}.tar.bz2
Source1:	pw_quality.pamd
Patch0:		libpwquality-1.4.4-fix-python-linking.patch
Patch1:		libpwquality-1.4.5-fix-python-cflags.patch
BuildRequires:	libcrack-devel
BuildRequires:	pam-devel
%if %{with python}
BuildRequires:	pkgconfig(python3)
%endif

%description
The libpwquality library purpose is to provide common functions for password
quality checking and also scoring them based on their apparent randomness.

The library also provides a function for generating random passwords with good
pronounceability. The library supports reading and parsing of a configuration
file.

%package tools
Summary:	Tools for password quality checking and generating random passwords
Group:		System/Base
Requires:	cracklib-dicts
Provides:	%{oname} = %{version}-%{release}

%description tools
This package contains the tools for password quality checking and generation.

%package common
Summary:	Data files for password quality checking and generating random passwords
Group:		System/Base
BuildArch:	noarch
Conflicts:	libpwquality-tools < 1.1.1-2

%description common
This package contains the data files for %{name}.

%package -n pam_pwquality
Summary:	PAM module for %{oname}
Group:		System/Libraries
Requires:	cracklib-dicts
Requires:	pam
Conflicts:	%{_lib}pwquality1 < 1.1.1-2
Conflicts:	libpwquality-tools < 1.1.1-2

%description -n pam_pwquality
This package contains the PAM module for %{name}.

%package -n %{libname}
Summary:	Shared libraries for %{oname}
Group:		System/Libraries
Requires:	%{name}-common >= %{version}-%{release}
%rename %{oldlibname}

%description -n %{libname}
The libpwquality library purpose is to provide common functions for password
quality checking and also scoring them based on their apparent randomness.

%package -n %{devname}
Summary:	Files needed for developing PAM-aware applications and modules for PAM
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{devname}
Files needed for development of applications using the libpwquality library.

%package -n python-pwquality
Summary:	Python bindings for the libpwquality library
Group:		Development/Python

%description -n python-pwquality
This is pwquality Python module that provides Python bindings for the
libpwquality library. These bindings can be used for easy password quality
checking and generation of random pronounceable passwords from Python
applications.

%prep
%autosetup -p1

%build
%configure \
	--with-securedir=%{_libdir}/security \
%if %{with python}
	--with-pythonsitedir=%{py_platsitedir} \
%else
	--disable-python-bindings \
%endif
	--enable-pam \

%make_build CFLAGS="%{optflags}"

%install
%make_install
%if %{with python}
# (tpg) 2023-04-26 TEST FAILED: /builddir/build/BUILDROOT/libpwquality-1.4.5-2.x86_64/usr/lib64/python3.11/site-packages/ does NOT support .pth files
export SETUPTOOLS_USE_DISTUTILS=stdlib
# make install seems to forget about this...
cd python
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
cd ..
rm -f %{buildroot}%{py_platsitedir}/*.egg
%endif

install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/pw_quality

%find_lang %{name}

%files tools -f %{name}.lang
%{_bindir}/pwmake
%{_bindir}/pwscore
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*

%files common
%config(noreplace) %{_sysconfdir}/security/%{oname}.conf
%doc %{_mandir}/man5/pwquality.conf.5*

%files -n pam_pwquality
%{_sysconfdir}/pam.d/pw_quality
%{_libdir}/security/pam_pwquality.so
%doc %{_mandir}/man8/pam_pwquality.8*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{oname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{oname}.pc

%if %{with python}
%files -n python-pwquality
%{py_platsitedir}/%{oname}.*.so
%{py_platsitedir}/%{oname}-%{version}-py%{py_ver}.egg-info
%endif
