# we don't want to provide private python extension libs
%if %{_use_internal_dependency_generator}
%define __noautoprovfiles '%{python_sitearch}/(.*)\\.so$'
%else
%define _exclude_files_from_autoprov ^%{python_sitearch}/.*\\\.so$
%endif

%define oname pwquality

%define major 1
%define libname %mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

Summary:	Library for password quality checking and generating random passwords
Name:		libpwquality
Version:	1.1.1
Release:	1
# The package is BSD licensed with option to relicense as GPL+
# - this option is redundant as the BSD license allows that anyway.
License:	BSD or GPL+
Group:		System/Libraries
URL:		http://libpwquality.fedorahosted.org/
Source0:	http://fedorahosted.org/releases/l/i/libpwquality/libpwquality-%{version}.tar.bz2
BuildRequires:	libcrack-devel
BuildRequires:	pam-devel
BuildRequires:	python-devel

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
Provides:	%{name} = %{version}-%{release}

%description tools
The libpwquality library purpose is to provide common functions for password
quality checking and also scoring them based on their apparent randomness.

The library also provides a function for generating random passwords with good
pronounceability. The library supports reading and parsing of a configuration
file.

%package -n %{libname}
Summary:	Shared libraries for %{oname}
Group:		System/Libraries
Requires:	%{name}-tools >= %{version}-%{release}

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
%setup -q

%build
%configure2_5x \
	--with-securedir=/%{_lib}/security \
	--with-pythonsitedir=%{python_sitearch} \
	--disable-static \
	--disable-rpath

%make

%install
%makeinstall_std

%find_lang %{name}

%files tools -f %{name}.lang
%doc COPYING README NEWS AUTHORS
%config(noreplace) %{_sysconfdir}/security/%{oname}.conf
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
/%{_lib}/security/pam_pwquality.so

%files -n %{devname}
%{_includedir}/%{oname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{oname}.pc

%files -n python-pwquality
%{python_sitearch}/%{oname}.so


%changelog
* Mon Jul 09 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.1-1
+ Revision: 808654
- import libpwquality

