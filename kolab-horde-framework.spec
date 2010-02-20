%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Horde framework components tailored for Kolab
Name:		kolab-horde-framework
Version:	2.1.0
Release:	%mkrel 7
License:	GPL
Group:		System/Servers
URL:		http://www.kolab.org/
Source0:	kolab-horde-framework-%{version}.tar.bz2
Requires:	php-pear-File_PDF
Requires:	php-pear-Net_Cyrus
Requires:	php-pear-Net_IMAP
Requires:	php-pear-Net_LMTP
Requires:	php-pear-Net_SMS
Requires:	php-pear-Text_Diff
Requires:	php-pear-VFS
Requires:	php-pear-XML_SVG
BuildRequires:	php-cli
BuildRequires:	php-pear
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Horde framework components tailored for Kolab.

%prep

%setup -q -n %{name}

perl -pi -e "s|\@l_prefix\@|%{_prefix}|g" install-packages.php

# fix attribs
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
	
# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix php path
find . -type f|xargs perl -pi -e "s|/usr/local/bin/php|%{_bindir}/php|g"

# we allready have these as external packages
rm -rf File_PDF
rm -rf Net_Cyrus
rm -rf Net_IMAP
rm -rf Net_LMTP
rm -rf Net_SMS
rm -rf Text_Diff
rm -rf VFS
rm -rf XML_SVG

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/kolab/horde

env PHP_PEAR_PHP_BIN="%{_bindir}/php -d safe_mode=off" %{_bindir}/php -d safe_mode=off install-packages.php --install-dir %{buildroot}%{_datadir}/kolab/horde

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/kolab/horde
