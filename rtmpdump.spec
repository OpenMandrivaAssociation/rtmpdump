%define snap 20190721
%define rel 2

%define major 1
%define libname %mklibname rtmp %major
%define devname %mklibname rtmp -d

%define build_crypto 1

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
Version:	2.4
License:	GPLv2+
Group:		Video
%if %{snap}
Release:	0.git%{snap}.%{rel}%{?extrarelsuffix}
%else
Release:	%rel%{?extrarelsuffix}
%endif
URL:		https://rtmpdump.mplayerhq.hu/
%if %{snap}
# rm -rf rtmpdump && git clone git://git.ffmpeg.org/rtmpdump && cd rtmpdump/
# git archive --prefix=rtmpdump-$(date +%Y%m%d)/ --format=tar HEAD | xz > ../rtmpdump-$(date +%Y%m%d).tar.xz
Source0:	%{name}-%{snap}.tar.xz
%else
Source0:	http://rtmpdump.mplayerhq.hu/download/%{name}-%{version}.tgz
%endif
# fix pkgconfig issues
Patch1:		rtmp-pkgconfig-private.patch
# these do not belong to sbindir
Patch2:		rtmp-no-sbindir.patch
Patch3:		https://github.com/JudgeZarbi/RTMPDump-OpenSSL-1.1/commit/a5f4d8e3f5302b44e240ecf07f2a9525b5469dfb.patch
Patch4:		https://github.com/JudgeZarbi/RTMPDump-OpenSSL-1.1/commit/1c745717ff7d7391266522705143298f3563ad40.patch
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
# FIXME remove once rpm's pkgconfig dependency generator has been fixed to
# handle dependencies indicated in the *.pc files automatically
Requires:	pkgconfig(libssl)
Requires:	pkgconfig(libcrypto)

%description -n %{devname}
The development files that are needed to build software depending
on librtmp.

%prep
%if %{snap}
%setup -q -n %{name}-%{snap}
%else
%setup -q
%endif
%autopatch -p1

%build
%set_build_flags
%make_build CC=%{__cc} XCFLAGS="%{optflags}" LDFLAGS="%{ldflags}" \
%if !%build_crypto
	CRYPTO=
%endif
# empty line

%install
%make_install prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir}
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
