%global geoserver_data %{_sharedstatedir}/geoserver

Name:           geoserver-geonode-data
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
BuildArch:      noarch
Summary:        GeoServer GeoNode Data
License:        GPLv3
URL:            https://geonode.org
Source0:        https://artifacts.geonode.org/geoserver/%{version}/geonode-geoserver-ext-web-app-data.zip

Conflicts:      geoserver-data
Requires:       geoserver-geonode = %{version}-%{release}


%description
GeoServer data for use with a GeoNode instance.


%install
%{__install} -d %{buildroot}%{geoserver_data}
%{__unzip} %{SOURCE0} -d %{buildroot}%{geoserver_data}


%files
%defattr(0664,tomcat,tomcat,0775)
%config(noreplace) %{geoserver_data}/data/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}