#specfile originally created for Fedora, modified for Moblin Linux
%define _sbindir /sbin
#define _libdir /%{_lib}

Summary: The GNU disk partition manipulation program
Name:    parted
Version: 0
Release: 1
License: GPLv3+
Group:   Applications/System
URL:     http://www.gnu.org/software/parted

Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

BuildRequires: e2fsprogs-devel
BuildRequires: libuuid-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: libtool
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: gperf

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.

%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
Obsoletes: %{name}-docs

%description doc
Man and info pages for %{name}.

%prep
%setup -q -n %{name}-%{version}

# Build fix - 'gets' is removed in C11
# Chose this over committing this change to Git because gnulib/ is a Git submodule
sed -i '/^_GL_WARN_ON_USE (gets,/s;^;//;' gnulib/lib/stdio.in.h

# This is normally generated from Git history. Cannot be done on OBS.
touch ChangeLog

./bootstrap --skip-po --no-git --gnulib-srcdir=gnulib

%build
%configure --disable-static --disable-device-mapper --with-readline --with-libdir=%{_libdir} --exec-prefix=/usr
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%make_install

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_infodir}/dir
#%{__rm} -rf %{buildroot}%{_bindir}/label
#%{__rm} -rf %{buildroot}%{_bindir}/disk

# TODO: .po files are not included in the Git repo
#%%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post doc
if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%preun doc
if [ $1 = 0 -a -f %{_infodir}/%{name}.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

# TODO: .po files are not included in the Git repo
#%%lang_package

%files 
%defattr(-,root,root,-)
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_libdir}/libparted*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/pkgconfig/libparted.pc

%files doc
%defattr(-,root,root,-)
%{_infodir}/%{name}.*
%{_mandir}/man8/%{name}.*
%{_mandir}/man8/partprobe.*
