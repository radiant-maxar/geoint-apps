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
Source12:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-feature-pregeneralized-plugin.zip
Source13:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-gdal-plugin.zip
Source14:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-geofence-plugin.zip
Source15:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-geofence-server-plugin.zip
Source16:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-geofence-wps-plugin.zip
Source17:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-geopkg-output-plugin.zip
Source18:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-grib-plugin.zip
Source19:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-gwc-s3-plugin.zip
Source20:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-h2-plugin.zip
Source21:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-imagemap-plugin.zip
Source22:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-importer-plugin.zip
Source23:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-inspire-plugin.zip
Source24:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-jp2k-plugin.zip
Source25:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-libjpeg-turbo-plugin.zip
Source26:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-mapml-plugin.zip
Source27:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-mbstyle-plugin.zip
Source28:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-metadata-plugin.zip
Source29:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-mongodb-plugin.zip
Source30:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-monitor-plugin.zip
Source31:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-mysql-plugin.zip
Source32:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-netcdf-out-plugin.zip
Source33:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-netcdf-plugin.zip
Source34:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-ogr-wfs-plugin.zip
Source35:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-ogr-wps-plugin.zip
Source36:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-oracle-plugin.zip
Source37:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-params-extractor-plugin.zip
Source38:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-printing-plugin.zip
Source39:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-pyramid-plugin.zip
Source40:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-querylayer-plugin.zip
Source41:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-sldservice-plugin.zip
Source42:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-sqlserver-plugin.zip
Source43:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-vectortiles-plugin.zip
Source44:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wcs2_0-eo-plugin.zip
Source45:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-web-resource-plugin.zip
Source46:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wmts-multi-dimensional-plugin.zip
Source47:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wps-cluster-hazelcast-plugin.zip
Source48:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wps-download-plugin.zip
Source49:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wps-jdbc-plugin.zip
Source50:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-wps-plugin.zip
Source51:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-xslt-plugin.zip
Source52:       https://prdownloads.sourceforge.net/geoserver/GeoServer/%{version}/extensions/geoserver-%{version}-ysld-plugin.zip


%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data.
Designed for interoperability, it publishes data from any major spatial data source using open standards.


%package app-schema
Summary:       GeoServer Application Schema Support Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description app-schema
%{summary}


%package authkey
Summary:       GeoServer Authkey Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description authkey
%{summary}


%package cas
Summary:       GeoServer CAS Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description cas
%{summary}


%package charts
Summary:       GeoServer Charts Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description charts
%{summary}


%package control-flow
Summary:       GeoServer Control Flow Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description control-flow
%{summary}


%package css
Summary:       GeoServer CSS Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description css
%{summary}


%package csw-iso
Summary:       GeoServer CSW ISO Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description csw-iso
%{summary}


%package csw
Summary:       GeoServer CSW Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description csw
%{summary}


%package db2
Summary:       GeoServer DB2 Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description db2
%{summary}


%package dxf
Summary:       GeoServer DXF Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description dxf
%{summary}


%package excel
Summary:       GeoServer Excel Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description excel
%{summary}


%package feature-pregeneralized
Summary:       GeoServer Feature Pregeneralized Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description feature-pregeneralized
%{summary}


%package gdal
Summary:       GeoServer GDAL Extension
License:       GPLv2 and LGPL-2.1
Requires:      gdal-java
Requires:      geoserver = %{version}-%{release}

%description gdal
%{summary}


%package geofence
Summary:       GeoServer Geofence Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description geofence
%{summary}


%package geofence-server
Summary:       GeoServer Geofence Server Extension
License:       GPLv2
Requires:      geoserver-geofence = %{version}-%{release}

%description geofence-server
%{summary}


%package geofence-wps
Summary:       GeoServer Geofence WPS Extension
License:       GPLv2
Requires:      geoserver-geofence = %{version}-%{release}

%description geofence-wps
%{summary}


%package geopkg-output
Summary:       GeoServer GeoPackage Output Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description geopkg-output
%{summary}


%package grib
Summary:       GeoServer Grib Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description grib
%{summary}


%prep
%autosetup -c
for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output grib; do
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
%{__unzip} %{SOURCE12} -d plugins/feature-pregeneralized
%{__unzip} %{SOURCE13} -d plugins/gdal
%{__unzip} %{SOURCE14} -d plugins/geofence
%{__unzip} %{SOURCE15} -d plugins/geofence-server
%{__unzip} %{SOURCE16} -d plugins/geofence-wps
%{__unzip} %{SOURCE17} -d plugins/geopkg-output
%{__unzip} %{SOURCE18} -d plugins/grib


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_home}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-default-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-default-libs.txt

for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output grib; do
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


%files -f geoserver-db2-libs.txt db2
%doc plugins/db2/GEOTOOLS_NOTICE.html plugins/db2/NOTICE.html
%license plugins/db2/GPL.html plugins/db2/LGPL.html


%files -f geoserver-dxf-libs.txt dxf
%doc plugins/dxf/NOTICE.html
%license plugins/dxf/GPL.html


%files -f geoserver-excel-libs.txt excel
%doc plugins/excel/GEOTOOLS_NOTICE.html plugins/excel/NOTICE.html
%license plugins/excel/GPL.html plugins/excel/LGPL.html


%files -f geoserver-feature-pregeneralized-libs.txt feature-pregeneralized
%doc plugins/feature-pregeneralized/GEOTOOLS_NOTICE.html plugins/feature-pregeneralized/NOTICE.html
%license plugins/feature-pregeneralized/GPL.html plugins/feature-pregeneralized/LGPL.html


%files -f geoserver-gdal-libs.txt gdal
%doc plugins/gdal/GEOTOOLS_NOTICE.html plugins/gdal/NOTICE.html
%license plugins/gdal/GPL.html plugins/gdal/LGPL.html


%files -f geoserver-geofence-libs.txt geofence
%doc plugins/geofence/NOTICE.html
%license plugins/geofence/GPL.html


%files -f geoserver-geofence-server-libs.txt geofence-server
%doc plugins/geofence-server/NOTICE.html
%license plugins/geofence-server/GPL.html


%files -f geoserver-geofence-wps-libs.txt geofence-wps
%doc plugins/geofence-wps/NOTICE.html
%license plugins/geofence-wps/GPL.html


%files -f geoserver-geopkg-output-libs.txt geopkg-output
%doc plugins/geopkg-output/GEOTOOLS_NOTICE.html plugins/geopkg-output/NOTICE.html
%license plugins/geopkg-output/GPL.html plugins/geopkg-output/LGPL.html


%files -f geoserver-grib-libs.txt grib
%doc plugins/grib/GEOTOOLS_NOTICE.html plugins/grib/NOTICE.html
%license plugins/grib/GPL.html plugins/grib/LGPL.html


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
