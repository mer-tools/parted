#specfile originally created for Fedora, modified for Moblin Linux

Summary: The GNU disk partition manipulation program
Name:    parted
Version: 3.6
Release: 1
License: GPLv3+
URL:     https://github.com/mer-tools/parted
Source0: %{name}-%{version}.tar.gz

BuildRequires: bc
BuildRequires: e2fsprogs-devel
BuildRequires: gettext-devel
BuildRequires: git
BuildRequires: gperf
BuildRequires: libtool
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(readline)
BuildRequires: pkgconfig(uuid)
BuildRequires: rsync
BuildRequires: texinfo

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.

%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%autosetup -n %{name}-%{version}/%{name}

./bootstrap --skip-po --no-git --gnulib-srcdir=gnulib

%build
%configure --disable-static --disable-device-mapper --with-readline --with-libdir=%{_libdir} --exec-prefix=%{_prefix}
%make_build

%install
%make_install

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_libdir}/libparted*.so.*

%files devel
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/libparted-fs-resize.so
%{_libdir}/pkgconfig/libparted.pc
%{_libdir}/pkgconfig/libparted-fs-resize.pc

%files doc
%{_mandir}/man8/%{name}.*
%{_mandir}/man8/partprobe.*
