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


%prep
%autosetup -c


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_home}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-default-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-default-libs.txt

for plugin in app-schema authkey cas; do
    %{__mkdir_p} plugins/${plugin}
done

%{__unzip} %{SOURCE1} -d plugins/app-schema
%{__unzip} %{SOURCE2} -d plugins/authkey
%{__unzip} %{SOURCE3} -d plugins/cas

for plugin in app-schema authkey cas; do
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
