%define		plugin		eventum
Summary:	DokuWiki Eventum Plugin
Summary(pl.UTF-8):	Wtyczka Include (dołączania) dla Eventum
Name:		dokuwiki-plugin-%{plugin}
Version:	20100928
Release:	1
License:	GPL v2
Source0:	http://github.com/glensc/%{name}/zipball/master#/%{plugin}.zip
# Source0-md5:	-
Group:		Applications/WWW
URL:		http://www.dokuwiki.org/plugin:eventum
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20080505
Requires:	php-pear-XML_RPC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

# link issue -> eventum icon
install -d $RPM_BUILD_ROOT%{dokudir}/lib/images/interwiki
ln -s eventum.gif $RPM_BUILD_ROOT%{dokudir}/lib/images/interwiki/issue.gif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf

# [[issue>XXX]] icon
%{dokudir}/lib/images/interwiki/issue.gif
