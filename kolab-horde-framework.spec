%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Horde framework components tailored for Kolab
Name:		kolab-horde-framework
Version:	2.1.0
Release:	15
License:	GPL
Group:		System/Servers
URL:		https://www.kolab.org/
Source0:	kolab-horde-framework-%{version}.tar.bz2
Patch0:		kolab-horde-framework-CVE-2009-4824.diff
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
AutoReqProv: 0

%description
Horde framework components tailored for Kolab.

%prep

%setup -q -n %{name}
%patch0 -p0

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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-12mdv2011.0
+ Revision: 666034
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-11mdv2011.0
+ Revision: 606267
- rebuild

* Wed May 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-10mdv2010.1
+ Revision: 546114
- P0: security fix for CVE-2009-4824

* Sun Feb 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 2.1.0-9mdv2010.1
+ Revision: 509255
- Bump release

* Sat Feb 20 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 2.1.0-8mdv2010.1
+ Revision: 508718
- No php auto-deps detect

* Sat Feb 20 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.1.0-7mdv2010.1
+ Revision: 508629
- %define _requires_exceptions 	php-pear-Services_Weather(/usr/share/pear/Services/Weather.php)

* Sun Jan 17 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.1.0-6mdv2010.1
+ Revision: 492541
- added %%define _requires_exceptions   php-pear-Services_Weather(/usr/share/pear/Services/Weather.php) because its missing in the Service-Weather package

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.1.0-5mdv2010.0
+ Revision: 425490
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-4mdv2009.0
+ Revision: 221878
- rebuild

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-3mdv2008.1
+ Revision: 150430
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2008.0
+ Revision: 33631
- new mandriva file

* Sat May 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1mdv2008.0
+ Revision: 31473
- Import kolab-horde-framework



* Sat May 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1mdv2007.1
- initial mandriva package
