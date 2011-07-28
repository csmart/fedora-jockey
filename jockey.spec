Name:           jockey
Version:        0.9.3
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

%prep
%setup -q -a 1
%patch0 -p1 -b .execfix
cp fedora-%{name}-%{version}/%{name}/* %{name}/

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root %{buildroot}
rm -r %{buildroot}/%{_datadir}/doc

# install fedora extra files
cp -a fedora-%{name}-%{version}/modaliases \
      fedora-%{name}-%{version}/handlers \
      %{buildroot}/%{_datadir}/%{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/jockey-gtk.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/jockey-kde.desktop

desktop-file-validate %{buildroot}/%{_datadir}/autostart/jockey-gtk.desktop
desktop-file-validate %{buildroot}/%{_datadir}/autostart/jockey-kde.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
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

%changelog
* Thu Jul 28 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 0.9.3-1
- Initial version

