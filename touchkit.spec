#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
#
Summary:	eGalax TouchKit drivers and utilities
Summary(pl.UTF-8):	Sterowniki i narzędzia do paneli dotykowych eGalax TouchKit
Name:		touchkit
Version:	1.0.2.2013
%define	rel	1
Release:	%{rel}
License:	?  Copyright(c) 2000 - 2003, eGalax Inc. All Right Reserved.
Group:		Applications/System
# is it distributable???
#URL list on	http://www.egalax.com.tw/Download.htm
Source0:	http://www.egalax.com.tw/Beta/TouchKit_Linux_%{version}.zip
# NoSource0-md5:	e9c65210577003948eb676a84712589c
Source1:	http://www.egalax.com.tw/NEWTouchKitv33.pdf
# NoSource1-md5:	1df5e69c04747d0e34cb8b68cdcccb93
Source2:	http://www.egalax.com.tw/Document/TouchKit%20Manual%20for%20Linux%20v3.1.4.pdf
# NoSource2-md5:	c6a78751d6f2c5d789d90533651d17d6
Source3:	http://www.egalax.com.tw/SoftwareProgrammingGuide_1.1.pdf
# NoSource3-md5:	7c9d12b5ef9aec190748d00b351728c8
# no license information anywhere... don't know if distributable :/
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
Patch0:		%{name}-lessmess.patch
Patch1:		%{name}-gcc33.patch
URL:		http://www.egalax.com.tw/
BuildRequires:	XFree86-Xserver-devel > 4.3.99.902-0.1
BuildRequires:	XFree86-devel
%if %{with kernel}
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:	kernel-headers < 2.5}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	sharutils
BuildRequires:	tcl
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eGalax TouchKit drivers and utilities.

%description -l pl.UTF-8
Sterowniki i narzędzia do paneli dotykowych eGalax TouchKit.

%package utils
Summary:	eGalax TouchKit utilities
Summary(pl.UTF-8):	Narzędzia do paneli dotykowych eGalax TouchKit
Group:		Applications/System
Requires:	tk

%description utils
eGalax TouchKit utilities (both command line and GUI).

%description utils -l pl.UTF-8
Narzędzia do paneli dotykowych eGalax TouchKit (działające z linii
poleceń oraz z graficznym interfejsem).

%package -n XFree86-input-touchkit
Summary:	XFree86 input driver module for eGalax TouchKit panels
Summary(pl.UTF-8):	Moduł sterownika wejściowego XFree86 dla paneli dotykowych eGalax TouchKit
Group:		X11
%{requires_eq_to XFree86-modules XFree86-Xserver-devel}

%description -n XFree86-input-touchkit
XFree86 input driver module for eGalax TouchKit panels.

%description -n XFree86-input-touchkit -l pl.UTF-8
Moduł sterownika wejściowego XFree86 dla paneli dotykowych eGalax
TouchKit.

%package -n kernel-usb-touchkit
Summary:	Linux driver for eGalax TouchKit USB panels
Summary(pl.UTF-8):	Sterownik Linuksa dla paneli dotykowych USB eGalax TouchKit
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-usb-touchkit
Linux driver for eGalax TouchKit panels with USB connector.

%description -n kernel-usb-touchkit -l pl.UTF-8
Sterownik Linuksa dla paneli dotykowych eGalax TouchKit w wersji
podłączanej przez USB.

%package -n kernel-smp-usb-touchkit
Summary:	Linux SMP driver for eGalax TouchKit USB panels
Summary(pl.UTF-8):	Sterownik Linuksa SMP dla paneli dotykowych USB eGalax TouchKit
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-usb-touchkit
Linux SMP driver for eGalax TouchKit panels with USB connector.

%description -n kernel-smp-usb-touchkit -l pl.UTF-8
Sterownik Linuksa SMP dla paneli dotykowych eGalax TouchKit w wersji
podłączanej przez USB.

%prep
%setup -q -n TouchKit_Linux
uudecode touchkit.setupr8nm.sh -o /dev/stdout | tar xzf -
%patch -P0 -p0
%patch -P1 -p0

cp %{SOURCE1} %{SOURCE3} .
# no spaces please
cp %{SOURCE2} TouchKit_Manual_for_Linux_v3.1.4.pdf

rm -f touchkit/xf86drv/bin/*

echo 'puts 401' > touchkit/utility/xversion.tcl

%build
%{__make} rebuild -C touchkit \
	SUBDIRS=include

%if %{with kernel}
%{__make} do_build_module -C touchkit/usb \
	KGCC="%{kgcc}" \
	OPT="%{rpmcflags}" \
	LINUX_PATH="%{_kernelsrcdir}"
%endif

%if %{with userspace}
%{__make} usbpnpd -C touchkit/usb \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%{__make} rebuild -C touchkit \
	SUBDIRS="driver utility diag" \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

cp -f touchkit/xf86drv/Imakefile{.401a,}
# note: "/" at the end is important
%{__make} -C touchkit/xf86drv Makefile touchkit_drv.o \
	XF86SRC.401=/usr/X11R6/include/X11/Xserver/ \
	CDEBUGFLAGS="%{rpmcflags} -I/usr/X11R6/include/X11"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install -C touchkit \
	DESTDIR=$RPM_BUILD_ROOT

V="0123 3823 3823 0EEF 0EEF"
P="0001 0001 0002 0001 0002"
cat > $RPM_BUILD_ROOT/etc/usbpnpd.conf <<EOF
#Device = VendorID, ProductID, ActionIfPlugIn
Device = 0x0123, 0x0001, insmod tkusb vidlist="$V" pidlist="$P"; /usr/bin/tpaneld &
Device = 0x3823, 0x0001, insmod tkusb vidlist="$V" pidlist="$P"; /usr/bin/tpaneld &
Device = 0x3823, 0x0002, insmod tkusb vidlist="$V" pidlist="$P"; /usr/bin/tpaneld &
Device = 0x0EEF, 0x0001, insmod tkusb vidlist="$V" pidlist="$P"; /usr/bin/tpaneld &
Device = 0x0EEF, 0x0002, insmod tkusb vidlist="$V" pidlist="$P"; /usr/bin/tpaneld &
EOF
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install touchkit/usb/tkusb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install touchkit/usb/tkusb-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/tkusb.o
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-usb-touchkit
%depmod %{_kernel_ver}

%postun	-n kernel-usb-touchkit
%depmod %{_kernel_ver}

%post	-n kernel-smp-usb-touchkit
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-usb-touchkit
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files utils
%defattr(644,root,root,755)
%doc *.pdf
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/usbpnpd.conf
%dir %{_libdir}/TouchKit
%attr(755,root,root) %{_libdir}/TouchKit/touchcfg
%attr(755,root,root) %{_libdir}/TouchKit/tpaneld
%attr(755,root,root) %{_libdir}/TouchKit/usbpnpd
%dir %{_libdir}/TouchKit/diag
%attr(755,root,root) %{_libdir}/TouchKit/diag/*pcal
%attr(755,root,root) %{_libdir}/TouchKit/diag/drawtest
%attr(755,root,root) %{_libdir}/TouchKit/diag/*.tcl
%{_libdir}/TouchKit/diag/*.txt
%{_libdir}/TouchKit/image
%{_libdir}/TouchKit/include
%attr(755,root,root) %{_libdir}/TouchKit/utility

%files -n XFree86-input-touchkit
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/lib/modules/input/touchkit_drv.o
%endif

%if %{with kernel}
%files -n kernel-usb-touchkit
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/tkusb.o*

%files -n kernel-smp-usb-touchkit
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/tkusb.o*
%endif
