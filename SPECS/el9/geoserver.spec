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


%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data.
Designed for interoperability, it publishes data from any major spatial data source using open standards.


%prep
%autosetup -c


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_home}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{_bindir}/unzip geoserver.war -d %{buildroot}%{geoserver_webapp}


%files
%doc README.html target/VERSION.txt
%license license/*.html
%defattr(-, %{geoserver_user}, %{geoserver_user}, -)
%{geoserver_home}
%defattr(0664,%{geoserver_user},%{geoserver_group},0775)
%{geoserver_webapp}


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
