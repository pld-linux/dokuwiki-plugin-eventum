%define		plugin		eventum
Summary:	DokuWiki Eventum Plugin
Summary(pl.UTF-8):	Wtyczka Include (dołączania) dla Eventum
Name:		dokuwiki-plugin-%{plugin}
Version:	20090202
Release:	1
License:	GPL v2
Group:		Applications/WWW
URL:		https://cvs.delfi.ee/dokuwiki/plugin/eventum/
Requires:	dokuwiki >= 20080505
Requires:	php-pear-XML_RPC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%define		_cvsroot	:ext:cvs.delfi.ee:/usr/local/cvs
%define		_cvsmodule	dokuwiki/plugin/eventum

%description
Adds Eventum link button to edit toolbar.

Also adds extra info to Eventum interwiki links fetched from Eventum via
XML_RPC.

%prep
# check early if build is ok to be performed
%if %{!?debug:1}%{?debug:0} && %{!?_cvstag:1}%{?_cvstag:0} && %([[ %{release} = *.* ]] && echo 0 || echo 1)
# break if spec is not commited
cd %{_specdir}
if [ "$(cvs status %{name}.spec | awk '/Status:/{print $NF}')" != "Up-to-date" ]; then
	: "Integer build not allowed: %{name}.spec is not up-to-date with CVS"
	exit 1
fi
cd -
%endif
%setup -qTc
cd ..
cvs -d %{_cvsroot} co %{?_cvstag:-r %{_cvstag}} -d %{name}-%{version} -P %{_cvsmodule}
cd -

%build
# skip tagging if we checkouted from tag or have debug enabled
# also make make tag only if we have integer release
%if %{!?debug:1}%{?debug:0} && %{!?_cvstag:1}%{?_cvstag:0} && %([[ %{release} = *.* ]] && echo 0 || echo 1)
# do tagging by version
tag=%{name}-%(echo %{version} | tr . _)-%(echo %{release} | tr . _)

cd %{_specdir}
if [ $(cvs status -v %{name}.spec | egrep -c "$tag[[:space:]]") != 0 ]; then
	: "Tag $tag already exists"
	exit 1
fi
cvs tag $tag %{name}.spec
cd -
cvs tag $tag
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
find $RPM_BUILD_ROOT%{plugindir} -name CVS | xargs -r rm -rf

# link issue -> eventum icon
install -d $RPM_BUILD_ROOT%{dokudir}/lib/images/interwiki
ln -s eventum.gif $RPM_BUILD_ROOT%{dokudir}/lib/images/interwiki/issue.gif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%dir %{plugindir}/lang
%dir %{plugindir}/lang/en
%{plugindir}/lang/en/lang.php

# [[issue>XXX]] icon
%{dokudir}/lib/images/interwiki/issue.gif
