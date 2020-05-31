%define		subver	2020-05-31
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		eventum
%define		php_min_version 5.3.0
Summary:	DokuWiki Eventum Plugin
Summary(pl.UTF-8):	Wtyczka Include (dołączania) dla Eventum
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/eventum/dokuwiki-plugin-eventum/releases/download/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	ec8c68dfe305855105e8f15048f64bf9
URL:		https://www.dokuwiki.org/plugin:eventum
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
Requires:	dokuwiki >= 20101107
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php-pear-XML_RPC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		dokucache	/var/cache/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}
%define		_noautoreq_pear	class.Eventum_RPC.php

%description
Adds Eventum link button to edit toolbar.

Also adds extra info to Eventum interwiki links fetched from Eventum
via XML_RPC.

%prep
%setup -qc
mv %{plugin}/* .

version=$(awk '/date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{plugindir},%{dokucache}}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm -r $RPM_BUILD_ROOT%{plugindir}/XML
rm $RPM_BUILD_ROOT%{plugindir}/README.md
touch $RPM_BUILD_ROOT%{dokucache}/%{plugin}.cache

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi
# purge eventum cache
rm -f %{dokucache}/%{plugin}.cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/*.css
%{plugindir}/conf
%{plugindir}/images
%ghost %{dokucache}/%{plugin}.cache
