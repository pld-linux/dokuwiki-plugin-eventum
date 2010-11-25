%define		subver	2010-11-05
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		eventum
Summary:	DokuWiki Eventum Plugin
Summary(pl.UTF-8):	Wtyczka Include (dołączania) dla Eventum
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	3
License:	GPL v2
Source0:	http://github.com/glensc/dokuwiki-plugin-eventum/zipball/%{subver}#/%{plugin}-%{version}.zip
# Source0-md5:	ff1da92b0781e273eeb8541920c5a08e
Group:		Applications/WWW
URL:		http://www.dokuwiki.org/plugin:eventum
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20080505
Requires:	php-pear-XML_RPC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
Adds Eventum link button to edit toolbar.

Also adds extra info to Eventum interwiki links fetched from Eventum
via XML_RPC.

%prep
%setup -qc
mv *-%{plugin}-*/* .
rm *-%{plugin}-*/.gitignore

version=$(awk '/date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/*.css
%{plugindir}/conf
%{plugindir}/images
