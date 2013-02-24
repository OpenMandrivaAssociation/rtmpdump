
%define name	rtmpdump
%define version	2.3
%define rel	7

%define major	0
%define libname	%mklibname rtmp %major
%define devname	%mklibname rtmp -d

%define build_crypto 0

%bcond_with plf

%if %with plf
%define build_crypto 1
%define distsuffix plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

%if !%build_crypto
%define notice This version does not contain RTMPE / RTMPS / SWF verification support.
%else
%if %with plf
%define notice This package is in PLF because it contains support for the RTMPE protocol \
which some people may consider to be a DRM protection mechanism.
%else
%define notice %nil
%endif
%endif

Summary:	Toolkit for RTMP streams
Name:		%{name}
Version:	%{version}
Release:	%mkrel %rel%{?extrarelsuffix}
URL:		http://rtmpdump.mplayerhq.hu/
Source:		http://rtmpdump.mplayerhq.hu/download/%name-%version.tgz
# fix pkgconfig issues
Patch0:		rtmp-pkgconfig-hardcoded.patch
Patch1:		rtmp-pkgconfig-private.patch
# these do not belong to sbindir
Patch2:		rtmp-no-sbindir.patch
# (from upstream) link progs against shared library
Patch3:		rtmp-link-shared.patch
Patch4:		rtmp-link-shared2.patch
License:	GPLv2+
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	zlib-devel
%if %build_crypto
BuildRequires:	openssl-devel
%endif
Requires:	%libname >= %{version}

%description
rtmpdump is a toolkit for RTMP streams.

%notice

%package -n %libname
Summary:	Shared library: librtmp
Group:		System/Libraries

%description -n %libname
Shared library for handling RTMP streams.

%notice

%package -n %devname
Summary:	Development files for librtmp
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	rtmp-devel = %{version}-%{release}
Provides:	librtmp-devel = %{version}-%{release}
Requires:	openssl-devel

%description -n %devname
The development files that are needed to build software depending
on librtmp.

%prep
%setup -q
%apply_patches

%build
%make XCFLAGS="%optflags" LDFLAGS="%ldflags" \
%if !%build_crypto
	CRYPTO=
%endif
# empty line

%install
rm -rf %{buildroot}
%makeinstall_std prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir}
rm %{buildroot}%{_libdir}/librtmp.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_bindir}/rtmpdump
%{_bindir}/rtmpgw
%{_bindir}/rtmpsrv
%{_bindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/librtmp.so.%{major}*

%files -n %devname
%defattr(-,root,root)
%dir %{_includedir}/librtmp
%{_includedir}/librtmp/*.h
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*



%changelog
* Mon Feb 20 2012 abf
- The release updated by ABF

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3-4mdv2011.0
+ Revision: 669455
- mass rebuild

  + Anssi Hannula <anssi@mandriva.org>
    - plf: append "plf" to Release on cooker to make plf build have higher EVR
      again with the rpm5-style mkrel now in use

* Wed Jul 21 2010 Götz Waschk <waschk@mandriva.org> 2.3-3mdv2011.0
+ Revision: 556312
- fix devel dep

* Tue Jul 20 2010 Anssi Hannula <anssi@mandriva.org> 2.3-2mdv2011.0
+ Revision: 555462
- add missing provides to the devel package

* Mon Jul 19 2010 Anssi Hannula <anssi@mandriva.org> 2.3-1mdv2011.0
+ Revision: 555024
- initial Mandriva release

