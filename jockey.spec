%global jockey_version 0.9.3

Name:           jockey
Version:        %{jockey_version}
Release:        1%{?dist}
Summary:        Jockey driver manager

License:        GPLv2+
URL:            https://launchpad.net/jockey
Source0:        http://launchpad.net/jockey/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Source1:        fedora-%{name}-%{version}.tar.bz2
Patch0:         jockey-0.9.3-execfix.patch

BuildArch:      noarch 
BuildRequires:  python2-devel python-distutils-extra gettext
Requires:       dbus-python polkit PackageKit

%description
Jockey provides an user interface and desktop integration for installation 
and upgrade of third-party drivers. It is written in a distribution agnostic 
way, and to be easily portable to different front-ends (GNOME, KDE, 
command line).

%package gtk
Summary:        GTK front-end for Jockey driver manager
Requires:       %{name} = %{version}-%{release}
Requires:       dbus-python polkit-gnome gdk-pixbuf2 gtk3 
Requires:       gobject-introspection libnotify python-xkit

%description gtk
This package provides a GTK interface for Jockey.

Jockey provides an user interface and desktop integration for installation 
and upgrade of third-party drivers. It is written in a distribution agnostic 
way, and to be easily portable to different front-ends (GNOME, KDE, 
command line).

%package kde
Summary:        KDE front-end for Jockey driver manager
Requires:       %{name} = %{version}-%{release}
Requires:       dbus-python polkit-kde PyQt4 PyKDE4

%description kde
This package provides a KDE interface for Jockey.

Jockey provides an user interface and desktop integration for installation 
and upgrade of third-party drivers. It is written in a distribution agnostic 
way, and to be easily portable to different front-ends (GNOME, KDE, 
command line).

%global selinux_variants mls targeted
%package selinux
Summary:        SELinux module for Jockey driver manager
Version:        1.0.0
BuildRequires:  checkpolicy selinux-policy-devel hardlink
BuildRequires:  /usr/share/selinux/devel/policyhelp
Requires:       %{name} = %{version}-%{release}
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post):   /usr/sbin/semodule
Requires(postun): /usr/sbin/semodule

%description selinux
This package provides an SELinux module for Jockey driver manager.
You should install this package if you are using SELinux, so that Jockey
can be run in enforcing mode.

%global version %{jockey_version}

%prep
%setup -q -a 1
%patch0 -p1 -b .execfix
cp fedora-%{name}-%{version}/%{name}/* %{name}/

%build
%{__python} setup.py build

# building SELinux module
cd fedora-%{name}-%{version}/selinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv %{name}.pp %{name}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

%install
%{__python} setup.py install -O1 --root %{buildroot}
rm -r %{buildroot}/%{_datadir}/doc

# install fedora extra files
cp -a fedora-%{name}-%{version}/modaliases \
      fedora-%{name}-%{version}/handlers \
      %{buildroot}/%{_datadir}/%{name}

# install the selinux module
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 \
    fedora-%{name}-%{version}/selinux/%{name}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{name}.pp
done
/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux

# validate desktop files
desktop-file-validate %{buildroot}/%{_datadir}/applications/jockey-gtk.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/jockey-kde.desktop

desktop-file-validate %{buildroot}/%{_datadir}/autostart/jockey-gtk.desktop
desktop-file-validate %{buildroot}/%{_datadir}/autostart/jockey-kde.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post selinux
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING README.txt
%{_bindir}/jockey-text
%{python_sitelib}/*
%{_datadir}/%{name}/%{name}-backend
%{_datadir}/%{name}/modaliases
%{_datadir}/%{name}/handlers
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/dbus-1/system-services/*
%{_datadir}/polkit-1/actions/*
%{_sysconfdir}/dbus-1/system.d/*

%files gtk
%{_bindir}/jockey-gtk
%{_datadir}/%{name}/%{name}-gtk.ui
%{_datadir}/applications/jockey-gtk.desktop
%{_datadir}/autostart/jockey-gtk.desktop
%{_datadir}/dbus-1/services/*

%files kde
%{_bindir}/jockey-kde
%{_datadir}/%{name}/LicenseDialog.ui
%{_datadir}/%{name}/ManagerWindowKDE4.ui
%{_datadir}/%{name}/ProgressDialog.ui

%{_datadir}/applications/jockey-kde.desktop
%{_datadir}/autostart/jockey-kde.desktop
%{_datadir}/kde4/apps/jockey/jockey.notifyrc

%files selinux
%doc fedora-%{name}-%{version}/selinux/*te
%{_datadir}/selinux/*/%{name}.pp

%changelog
* Thu Jul 28 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 0.9.3-1
- Initial version

