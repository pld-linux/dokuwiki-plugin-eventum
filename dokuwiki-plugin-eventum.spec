%define		plugin		eventum
Summary:	DokuWiki Eventum Plugin
Summary(pl.UTF-8):	Wtyczka Include (dołączania) dla Eventum
Name:		dokuwiki-plugin-%{plugin}
Version:	20080303
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Requires:	dokuwiki >= 20070626
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%define		_cvsroot	:ext:cvs.delfi.ee:/usr/local/cvs
%define		_cvsmodule	dokuwiki/plugin/eventum

%description
Adds eventum link button to edit toolbar.

%prep
%setup -qTc
cd ..
cvs -d %{_cvsroot} co -d %{name}-%{version} %{_cvsmodule}
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
find $RPM_BUILD_ROOT%{plugindir} -name CVS | xargs -r rm -rf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%dir %{plugindir}/lang
%dir %{plugindir}/lang/en
%{plugindir}/lang/en/lang.php
