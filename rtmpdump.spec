%define major	0
%define libname	%mklibname rtmp %{major}
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
Name:		rtmpdump
Version:	2.3
Release:	7%{?extrarelsuffix}
License:	GPLv2+
Group:		Video
Url:		http://rtmpdump.mplayerhq.hu/
Source0:	http://rtmpdump.mplayerhq.hu/download/%name-%version.tgz
# fix pkgconfig issues
Patch0:		rtmp-pkgconfig-hardcoded.patch
Patch1:		rtmp-pkgconfig-private.patch
# these do not belong to sbindir
Patch2:		rtmp-no-sbindir.patch
# (from upstream) link progs against shared library
Patch3:		rtmp-link-shared.patch
Patch4:		rtmp-link-shared2.patch
BuildRequires:	pkgconfig(zlib)
%if %build_crypto
BuildRequires:	pkgconfig(openssl)
%endif

%description
rtmpdump is a toolkit for RTMP streams.

%notice

%package -n %{libname}
Summary:	Shared library: librtmp
Group:		System/Libraries

%description -n %{libname}
Shared library for handling RTMP streams.

%notice

%package -n %{devname}
Summary:	Development files for librtmp
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	rtmp-devel = %{version}-%{release}

%description -n %{devname}
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
%makeinstall_std prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir}
rm %{buildroot}%{_libdir}/librtmp.a

%files
%doc README ChangeLog
%{_bindir}/rtmpdump
%{_bindir}/rtmpgw
%{_bindir}/rtmpsrv
%{_bindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n %{libname}
%{_libdir}/librtmp.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/librtmp
%{_includedir}/librtmp/*.h
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*

