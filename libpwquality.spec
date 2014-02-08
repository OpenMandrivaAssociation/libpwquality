# we don't want to provide private python extension libs
%if %{_use_internal_dependency_generator}
%define __noautoprovfiles '%{python_sitearch}/(.*)\\.so$'
%else
%define _exclude_files_from_autoprov ^%{python_sitearch}/.*\\\.so$
%endif

%define oname	pwquality
%define major	1
%define libname	%mklibname %{oname} %{major}
%define devname	%mklibname %{oname} -d

Summary:	Library for password quality checking and generating random passwords
Name:		libpwquality
Version:	1.1.1
Release:	3
License:	BSD
Group:		System/Libraries
Url:		http://libpwquality.fedorahosted.org/
Source0:	http://fedorahosted.org/releases/l/i/libpwquality/%{name}-%{version}.tar.bz2
BuildRequires:	libcrack-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(python)

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
Conflicts:	%{_lib}pwquality1 < 1.1.1-2
Conflicts:	libpwquality-tools < 1.1.1-2

%description -n pam_pwquality
This package contains the PAM module for %{name}.

%package -n %{libname}
Summary:	Shared libraries for %{oname}
Group:		System/Libraries
Requires:	%{name}-common >= %{version}-%{release}

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
	--disable-static

%make

%install
%makeinstall_std

%find_lang %{name}

%files tools -f %{name}.lang
%doc COPYING README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_mandir}/man1/*

%files common
%config(noreplace) %{_sysconfdir}/security/%{oname}.conf
%{_mandir}/man5/pwquality.conf.5*

%files -n pam_pwquality
/%{_lib}/security/pam_pwquality.so
%{_mandir}/man8/pam_pwquality.8*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{oname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{oname}.pc

%files -n python-pwquality
%{python_sitearch}/%{oname}.so

