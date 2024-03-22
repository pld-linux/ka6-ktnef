#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.02.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		ktnef
Summary:	ktnef
Name:		ka6-%{kaname}
Version:	24.02.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	6b0d9f95c9e704489550dc43b08c31bb
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Test-devel >= 5.9.0
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-devel
BuildRequires:	ka6-kcalutils-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ktnef library contains an API for the handling of TNEF data. The
API permits access to the actual attachments, the message properties
(TNEF/MAPI), and allows one to view/extract message formatted text in
Rich Text Format format.

%description -l pl.UTF-8
Biblioteka ktnef zawiera API do obsługi danych TNEF. API pozwala na
dostęp do załączników, właściwości wiadomości (TNEF/MAPI) i pozwala
podejrzeć/wyjąć wiadomość w formacie RTF.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6Tnef.so.*.*
%ghost %{_libdir}/libKPim6Tnef.so.6
%{_datadir}/qlogging-categories6/ktnef.categories
%{_datadir}/qlogging-categories6/ktnef.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6
%{_libdir}/cmake/KPim6Tnef
%{_libdir}/libKPim6Tnef.so
