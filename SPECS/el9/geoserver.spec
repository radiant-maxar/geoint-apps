%global geoserver_group tomcat
%global geoserver_user geoserver
%global geoserver_uid 978
%global geoserver_home %{_sharedstatedir}/geoserver
%global geoserver_webapp %{_sharedstatedir}/tomcat/webapps/geoserver

Name:           geoserver
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoServer is an open source server for sharing geospatial data.

License:        GPLv2
URL:            https://geoserver.org

BuildArch:      noarch
BuildRequires:  unzip

Requires:       tomcat

Source0:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/geoserver-%{version}-war.zip
Source1:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-app-schema-plugin.zip
Source2:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-authkey-plugin.zip
Source3:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-cas-plugin.zip
Source4:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-charts-plugin.zip
Source5:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-control-flow-plugin.zip
Source6:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-css-plugin.zip
Source7:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-csw-iso-plugin.zip
Source8:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-csw-plugin.zip
Source9:        https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-db2-plugin.zip
Source10:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-dxf-plugin.zip
Source11:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-excel-plugin.zip

%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data.
Designed for interoperability, it publishes data from any major spatial data source using open standards.


%package app-schema
Summary:       GeoServer Application Schema Support Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description app-schema
GeoServer Application Schema Support Extension


%package authkey
Summary:       GeoServer Authkey Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description authkey
GeoServer Authkey Extension


%package cas
Summary:       GeoServer CAS Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description cas
GeoServer CAS Extension


%package charts
Summary:       GeoServer Charts Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description charts
GeoServer Charts Extension


%package control-flow
Summary:       GeoServer Control Flow Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description control-flow
GeoServer Control Flow Extension


%package css
Summary:       GeoServer CSS Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description css
GeoServer CSS Extension


%package csw-iso
Summary:       GeoServer CSW ISO Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description csw-iso
GeoServer CSW ISO Extension


%package csw
Summary:       GeoServer CSW Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description csw
GeoServer CSW Extension


%prep
%autosetup -c


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_home}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-default-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-default-libs.txt

for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel; do
    %{__mkdir_p} plugins/${plugin}
done
%{__unzip} %{SOURCE1}  -d plugins/app-schema
%{__unzip} %{SOURCE2}  -d plugins/authkey
%{__unzip} %{SOURCE3}  -d plugins/cas
%{__unzip} %{SOURCE4}  -d plugins/charts
%{__unzip} %{SOURCE5}  -d plugins/control-flow
%{__unzip} %{SOURCE6}  -d plugins/css
%{__unzip} %{SOURCE7}  -d plugins/csw-iso
%{__unzip} %{SOURCE8}  -d plugins/csw
%{__unzip} %{SOURCE8}  -d plugins/db2
%{__unzip} %{SOURCE10} -d plugins/dxf
%{__unzip} %{SOURCE11} -d plugins/excel

for plugin in app-schema authkey cas charts control-flow css csw-iso csw; do
    %{_bindir}/find plugins/${plugin} -type f -name \*.jar > geoserver-${plugin}-libs.txt
    %{__sed} -i -e "s|plugins/${plugin}|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-${plugin}-libs.txt
    %{__install} plugins/${plugin}/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib
done


%files -f geoserver-default-libs.txt
%doc README.html target/VERSION.txt
%license license/*.html
%defattr(-, %{geoserver_user}, %{geoserver_user}, -)
%{geoserver_home}
%defattr(0664,%{geoserver_user},%{geoserver_group},0775)
%{geoserver_webapp}/data
%{geoserver_webapp}/index.html
%{geoserver_webapp}/META-INF
%dir %{geoserver_webapp}/WEB-INF
%{geoserver_webapp}/WEB-INF/*.xml
%dir %{geoserver_webapp}/WEB-INF/classes
%dir %{geoserver_webapp}/WEB-INF/lib


%files -f geoserver-app-schema-libs.txt app-schema
%doc plugins/app-schema/app-schema-README.txt plugins/app-schema/GEOTOOLS_NOTICE.html
%license plugins/app-schema/app-schema-LICENSE.txt plugins/app-schema/LGPL.html


%files -f geoserver-authkey-libs.txt authkey
%doc plugins/authkey/NOTICE.html
%license plugins/authkey/GPL.html


%files -f geoserver-cas-libs.txt cas
%doc plugins/cas/cas-readme.txt plugins/cas/NOTICE.html
%license plugins/cas/GPL.html


%files -f geoserver-charts-libs.txt charts
%doc plugins/charts/GEOTOOLS_NOTICE.html
%license plugins/charts/LGPL.html


%files -f geoserver-control-flow-libs.txt control-flow
%doc plugins/control-flow/NOTICE.html
%license plugins/control-flow/GPL.html


%files -f geoserver-css-libs.txt css
%doc plugins/css/GEOTOOLS_NOTICE.html plugins/css/NOTICE.html
%license plugins/css/GPL.html plugins/css/LGPL.html


%files -f geoserver-csw-iso-libs.txt csw-iso
%doc plugins/csw-iso/NOTICE.html
%license plugins/csw-iso/GPL.html


%files -f geoserver-csw-libs.txt csw
%doc plugins/csw/GEOTOOLS_NOTICE.html plugins/csw/NOTICE.html
%license plugins/csw/GPL.html plugins/csw/LGPL.html


%pre
%{_bindir}/getent passwd %{geoserver_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{geoserver_uid} \
        --gid %{geoserver_group} \
        --comment "GeoServer User" \
        --shell /sbin/nologin \
        --home-dir %{geoserver_home} \
        --system \
        %{geoserver_user}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
