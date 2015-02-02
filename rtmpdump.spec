
%define name	rtmpdump
%define snap 20150202
%define version	2.4
%define rel	1

%define major	1
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
%if %{snap}
Release:	0.git%{snap}.%{rel}%{?extrarelsuffix}
%else
Release:	%rel%{?extrarelsuffix}
%endif
URL:		http://rtmpdump.mplayerhq.hu/
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
%if %{snap}
%setup -q -n %{name}-%{snap}
%else
%setup -q
%endif
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

