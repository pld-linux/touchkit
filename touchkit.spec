#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	eGalax TouchKit drivers and utilities
Summary(pl):	Sterowniki i narzêdzia do paneli dotykowych eGalax TouchKit
Name:		touchkit
Version:	1.0.0
%define	_rel	1
Release:	%{_rel}
License:	?  Copyright(c) 2000 - 2002, eGalax Inc. All Right Reserved.
Group:		Applications/System
# is it distributable???
#URL list on	http://www.egalax.com.tw/Download.htm
Source0:	http://www.egalax.com.tw/Linux_1.0.0.exe
Source1:	http://www.egalax.com.tw/NEWTouchKitv31.exe
Source2:	http://www.egalax.com.tw/TouchKitManualv2_5.exe
Source3:	http://www.egalax.com.tw/SoftwareProgrammingGuidev1_1.exe
Patch0:		%{name}-lessmess.patch
Patch1:		%{name}-2.4.20.patch
URL:		http://www.egalax.com.tw/
BuildRequires:	XFree86-devel
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
BuildRequires:	sharutils
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	tcl
BuildRequires:	unrar
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eGalax TouchKit drivers and utilities.

%description -l pl
Sterowniki i narzêdzia do paneli dotykowych eGalax TouchKit.

%package utils
Summary:	eGalax TouchKit utilities
Summary(pl):	Narzêdzia do paneli dotykowych eGalax TouchKit
Group:		Applications/System
Requires:	tk

%description utils
eGalax TouchKit utilities (both command line and GUI).

%description utils -l pl
Narzêdzia do paneli dotykowych eGalax TouchKit (dzia³aj±ce z linii
poleceñ oraz z graficznym interfejsem).

%package -n kernel-usb-touchkit
Summary:	Linux driver for eGalax TouchKit USB panels
Summary(pl):	Sterownik Linuksa dla paneli dotykowych USB eGalax TouchKit
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-usb-touchkit
Linux driver for eGalax TouchKit panels with USB connector.

%description -n kernel-usb-touchkit -l pl
Sterownik Linuksa dla paneli dotykowych eGalax TouchKit w wersji
pod³±czanej przez USB.

%package -n kernel-smp-usb-touchkit
Summary:	Linux SMP driver for eGalax TouchKit USB panels
Summary(pl):	Sterownik Linuksa SMP dla paneli dotykowych USB eGalax TouchKit
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-usb-touchkit
Linux SMP driver for eGalax TouchKit panels with USB connector.

%description -n kernel-smp-usb-touchkit -l pl
Sterownik Linuksa SMP dla paneli dotykowych eGalax TouchKit w wersji
pod³±czanej przez USB.

%prep
%setup -q -c -T -n %{name}
# has anybody seen more strange way of providing Linux drivers?
for f in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} ; do
	unrar x $f
done
uudecode Linux/touchkit.setup.sh -o /dev/stdout | tar xzf - -C ..
%patch0 -p1
%patch1 -p1

# no spaces please
mv -f 'Software Programming Guide v1_1.pdf' Software_Programming_Guide_v1_1.pdf
mv -f 'TouchKit Manual v2.5.pdf' TouchKit_Manual_v2.5.pdf

%build
%{__make} rebuild \
	CC="%{__cc}" \
	KGCC="%{kgcc}" \
	OPT="%{rpmcflags}" \
	LINUX_PATH="%{_kernelsrcdir}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install usb/tkusb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install usb/tkusb-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/tkusb.o

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

%files utils
%defattr(644,root,root,755)
%doc *.pdf
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/usbpnpd.conf
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

%files -n kernel-usb-touchkit
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/tkusb.o*

%files -n kernel-smp-usb-touchkit
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/tkusb.o*
