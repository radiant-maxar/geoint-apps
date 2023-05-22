%global geoserver_group tomcat
%global geoserver_user geoserver
%global geoserver_uid 978
%global geoserver_home %{_sharedstatedir}/geoserver
%global geoserver_webapp %{_sharedstatedir}/tomcat/webapps/geoserver
%global geoserver_source_url https://prdownloads.sourceforge.net/geoserver/GeoServer

Name:           geoserver
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoServer is an open source server for sharing geospatial data.

License:        GPLv2
URL:            https://geoserver.org

BuildArch:      noarch
BuildRequires:  unzip

Requires:       tomcat

Source0:        %{geoserver_source_url}/%{version}/geoserver-%{version}-war.zip
Source1:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-app-schema-plugin.zip
Source2:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-authkey-plugin.zip
Source3:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-cas-plugin.zip
Source4:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-charts-plugin.zip
Source5:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-control-flow-plugin.zip
Source6:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-css-plugin.zip
Source7:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-csw-iso-plugin.zip
Source8:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-csw-plugin.zip
Source9:        %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-db2-plugin.zip
Source10:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-dxf-plugin.zip
Source11:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-excel-plugin.zip
Source12:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-feature-pregeneralized-plugin.zip
Source13:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-gdal-plugin.zip
Source14:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-plugin.zip
Source15:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-server-plugin.zip
Source16:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-wps-plugin.zip
Source17:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geopkg-output-plugin.zip
Source18:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-grib-plugin.zip
Source19:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-gwc-s3-plugin.zip
Source20:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-h2-plugin.zip
Source21:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-imagemap-plugin.zip
Source22:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-importer-plugin.zip
Source23:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-inspire-plugin.zip
Source24:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-jp2k-plugin.zip
Source25:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-libjpeg-turbo-plugin.zip
Source26:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mapml-plugin.zip
Source27:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mbstyle-plugin.zip
Source28:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-metadata-plugin.zip
Source29:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mongodb-plugin.zip
Source30:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-monitor-plugin.zip
Source31:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mysql-plugin.zip
Source32:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-netcdf-out-plugin.zip
Source33:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-netcdf-plugin.zip
Source34:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-ogr-wfs-plugin.zip
Source35:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-ogr-wps-plugin.zip
Source36:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-oracle-plugin.zip
Source37:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-params-extractor-plugin.zip
Source38:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-printing-plugin.zip
Source39:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-pyramid-plugin.zip
Source40:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-querylayer-plugin.zip
Source41:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-sldservice-plugin.zip
Source42:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-sqlserver-plugin.zip
Source43:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-vectortiles-plugin.zip
Source44:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wcs2_0-eo-plugin.zip
Source45:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-web-resource-plugin.zip
Source46:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wmts-multi-dimensional-plugin.zip
Source47:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-cluster-hazelcast-plugin.zip
Source48:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-download-plugin.zip
Source49:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-jdbc-plugin.zip
Source50:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-plugin.zip
Source51:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-xslt-plugin.zip
Source52:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-ysld-plugin.zip


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


%package gwc-s3
Summary:       GeoServer GWC S3 Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description gwc-s3
%{summary}


%package h2
Summary:       GeoServer H2 Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description h2
%{summary}


%package imagemap
Summary:       GeoServer Imagemap Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description imagemap
%{summary}


%package importer
Summary:       GeoServer Importer Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description importer
%{summary}


%package inspire
Summary:       GeoServer Inspire Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description inspire
%{summary}


%package jp2k
Summary:       GeoServer JP2K Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description jp2k
%{summary}


%package libjpeg-turbo
Summary:       GeoServer LibJPEG Turbo Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description libjpeg-turbo
%{summary}


%package mapml
Summary:       GeoServer MapML Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description mapml
%{summary}


%package mbstyle
Summary:       GeoServer MBStyle Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description mbstyle
%{summary}


%package metadata
Summary:       GeoServer Metadata Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description metadata
%{summary}


%package mongodb
Summary:       GeoServer MongoDB Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description mongodb
%{summary}


%package monitor
Summary:       GeoServer Monitor Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description monitor
%{summary}


%package mysql
Summary:       GeoServer MySQL Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description mysql
%{summary}


%package netcdf-out
Summary:       GeoServer NetCDF Output Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description netcdf-out
%{summary}


%package netcdf
Summary:       GeoServer NetCDF Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description netcdf
%{summary}


%package ogr-wfs
Summary:       GeoServer OGR WFS Extension
License:       GPLv2
Requires:      gdal
Requires:      geoserver = %{version}-%{release}

%description ogr-wfs
%{summary}


%package ogr-wps
Summary:       GeoServer OGR WPS Extension
License:       GPLv2
Requires:      gdal
Requires:      geoserver = %{version}-%{release}

%description ogr-wps
%{summary}


%package oracle
Summary:       GeoServer Oracle Extension
License:       LGPL-2.1 and Oracle FUTC
Requires:      geoserver = %{version}-%{release}

%description oracle
%{summary}


%package params-extractor
Summary:       GeoServer Params Extractor Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description params-extractor
%{summary}


%package printing
Summary:       GeoServer Printing Extension
License:       GPLv2 and MapFish
Requires:      geoserver = %{version}-%{release}

%description printing
%{summary}


%package pyramid
Summary:       GeoServer Pyramid Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description pyramid
%{summary}


%package querylayer
Summary:       GeoServer Query Layer Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description querylayer
%{summary}


%package sldservice
Summary:       GeoServer SLD Service Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description sldservice
%{summary}


%package sqlserver
Summary:       GeoServer SQL Server Extension
License:       LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description sqlserver
%{summary}


%package vectortiles
Summary:       GeoServer Vector Tiles Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description vectortiles
%{summary}


%package wcs2_0-eo
Summary:       GeoServer WCS 2.0 EO Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description wcs2_0-eo
%{summary}


%package web-resource
Summary:       GeoServer Web Resource Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description web-resource
%{summary}


%package wmts-multi-dimensional
Summary:       GeoServer WMTS Multi Dimensional Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description wmts-multi-dimensional
%{summary}


%package wps-cluster-hazelcast
Summary:       GeoServer WPS Cluster Hazelcast Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description wps-cluster-hazelcast
%{summary}


%package wps-download
Summary:       GeoServer WPS Download Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description wps-download
%{summary}


%package wps-jdbc
Summary:       GeoServer WPS JDBC Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description wps-jdbc
%{summary}


%package wps
Summary:       GeoServer WPS Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description wps
%{summary}


%package xslt
Summary:       GeoServer XSLT Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description xslt
%{summary}


%package ysld
Summary:       GeoServer YSLD Extension
License:       GPLv2 and LGPL-2.1
Requires:      geoserver = %{version}-%{release}

%description ysld
%{summary}


%prep
%autosetup -c
for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output grib gwc-s3 h2 imagemap importer inspire jp2k libjpeg-turbo mapml mbstyle metadata mongodb monitor mysql netcdf-out netcdf ogr-wfs ogr-wps oracle params-extractor printing pyramid querylayer sldservice sqlserver vectortiles wcs2_0-eo web-resource wmts-multi-dimensional wps-cluster hazelcast wps-download wps-jdbc wps xslt ysld; do
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
%{__unzip} %{SOURCE19} -d plugins/gwc-s3
%{__unzip} %{SOURCE20} -d plugins/h2
%{__unzip} %{SOURCE21} -d plugins/imagemap
%{__unzip} %{SOURCE22} -d plugins/importer
%{__unzip} %{SOURCE23} -d plugins/inspire
%{__unzip} %{SOURCE24} -d plugins/jp2k
%{__unzip} %{SOURCE25} -d plugins/libjpeg-turbo
%{__unzip} %{SOURCE26} -d plugins/mapml
%{__unzip} %{SOURCE27} -d plugins/mbstyle
%{__unzip} %{SOURCE28} -d plugins/metadata
%{__unzip} %{SOURCE29} -d plugins/mongodb
%{__unzip} %{SOURCE30} -d plugins/monitor
%{__unzip} %{SOURCE31} -d plugins/mysql
%{__unzip} %{SOURCE32} -d plugins/netcdf-out
%{__unzip} %{SOURCE33} -d plugins/netcdf
%{__unzip} %{SOURCE34} -d plugins/ogr-wfs
%{__unzip} %{SOURCE35} -d plugins/ogr-wps
%{__unzip} %{SOURCE36} -d plugins/oracle
%{__unzip} %{SOURCE37} -d plugins/params-extractor
%{__unzip} %{SOURCE38} -d plugins/printing
%{__unzip} %{SOURCE39} -d plugins/pyramid
%{__unzip} %{SOURCE40} -d plugins/querylayer
%{__unzip} %{SOURCE41} -d plugins/sldservice
%{__unzip} %{SOURCE42} -d plugins/sqlserver
%{__unzip} %{SOURCE43} -d plugins/vectortiles
%{__unzip} %{SOURCE44} -d plugins/wcs2_0-eo
%{__unzip} %{SOURCE45} -d plugins/web-resource
%{__unzip} %{SOURCE46} -d plugins/wmts-multi-dimensional
%{__unzip} %{SOURCE47} -d plugins/wps-cluster-hazelcast
%{__unzip} %{SOURCE48} -d plugins/wps-download
%{__unzip} %{SOURCE49} -d plugins/wps-jdbc
%{__unzip} %{SOURCE50} -d plugins/wps
%{__unzip} %{SOURCE51} -d plugins/xslt
%{__unzip} %{SOURCE52} -d plugins/ysld


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_home}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-default-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-default-libs.txt

for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output grib gwc-s3 h2 imagemap importer inspire jp2k libjpeg-turbo mapml mbstyle metadata mongodb monitor mysql netcdf-out netcdf ogr-wfs ogr-wps oracle params-extractor printing pyramid querylayer sldservice sqlserver vectortiles wcs2_0-eo web-resource wmts-multi-dimensional wps-cluster-hazelcast wps-download wps-jdbc wps xslt ysld; do
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


%files -f geoserver-gwc-s3-libs.txt gwc-s3
%doc plugins/gwc-s3/NOTICE.html
%license plugins/gwc-s3/GPL.html


%files -f geoserver-h2-libs.txt h2
%doc plugins/h2/GEOTOOLS_NOTICE.html plugins/h2/NOTICE.html
%license plugins/h2/GPL.html plugins/h2/LGPL.html


%files -f geoserver-imagemap-libs.txt imagemap
%doc plugins/imagemap/NOTICE.html
%license plugins/imagemap/GPL.html


%files -f geoserver-importer-libs.txt importer
%doc plugins/importer/GEOTOOLS_NOTICE.html plugins/importer/NOTICE.html
%license plugins/importer/GPL.html plugins/importer/LGPL.html


%files -f geoserver-inspire-libs.txt inspire
%doc plugins/inspire/NOTICE.html
%license plugins/inspire/GPL.html


%files -f geoserver-jp2k-libs.txt jp2k
%doc plugins/jp2k/GEOTOOLS_NOTICE.html plugins/jp2k/NOTICE.html
%license plugins/jp2k/GPL.html plugins/jp2k/LGPL.html


%files -f geoserver-libjpeg-turbo-libs.txt libjpeg-turbo
%doc plugins/libjpeg-turbo/NOTICE.html
%license plugins/libjpeg-turbo/GPL.html


%files -f geoserver-mapml-libs.txt mapml
%doc plugins/mapml/NOTICE.html
%license plugins/mapml/GPL.html


%files -f geoserver-mbstyle-libs.txt mbstyle
%doc plugins/mbstyle/GEOTOOLS_NOTICE.html plugins/mbstyle/NOTICE.html
%license plugins/mbstyle/GPL.html plugins/mbstyle/LGPL.html


%files -f geoserver-metadata-libs.txt metadata
%doc plugins/metadata/NOTICE.html
%license plugins/metadata/GPL.html


%files -f geoserver-mongodb-libs.txt mongodb
%doc plugins/mongodb/GEOTOOLS_NOTICE.html plugins/mongodb/NOTICE.html
%license plugins/mongodb/GPL.html plugins/mongodb/LGPL.html


%files -f geoserver-monitor-libs.txt monitor
%doc plugins/monitor/NOTICE.html
%license plugins/monitor/GPL.html


%files -f geoserver-mysql-libs.txt mysql
%doc plugins/mysql/mysql-readme.txt


%files -f geoserver-netcdf-out-libs.txt netcdf-out
%doc plugins/netcdf-out/GEOTOOLS_NOTICE.html plugins/netcdf-out/NOTICE.html
%license plugins/netcdf-out/GPL.html plugins/netcdf-out/LGPL.html


%files -f geoserver-netcdf-libs.txt netcdf
%doc plugins/netcdf/GEOTOOLS_NOTICE.html plugins/netcdf/NOTICE.html plugins/netcdf/netCDF.html
%license plugins/netcdf/GPL.html plugins/netcdf/LGPL.html


%files -f geoserver-ogr-wfs-libs.txt ogr-wfs
%doc plugins/ogr-wfs/NOTICE.html plugins/ogr-wfs/ogr-README.txt
%license plugins/ogr-wfs/GPL.html


%files -f geoserver-ogr-wps-libs.txt ogr-wps
%doc plugins/ogr-wps/NOTICE.html plugins/ogr-wps/ogr-README.txt
%license plugins/ogr-wps/GPL.html


%files -f geoserver-oracle-libs.txt oracle
%doc plugins/oracle/GEOTOOLS_NOTICE.html plugins/oracle/oracle-readme.txt
%license plugins/oracle/LGPL.html plugins/oracle/OracleFUTC.html


%files -f geoserver-params-extractor-libs.txt params-extractor
%doc plugins/params-extractor/NOTICE.html
%license plugins/params-extractor/GPL.html


%files -f geoserver-printing-libs.txt printing
%doc plugins/printing/NOTICE.html
%license plugins/printing/GPL.html plugins/printing/MAPFISH-LICENSE.txt


%files -f geoserver-pyramid-libs.txt pyramid
%doc plugins/pyramid/GEOTOOLS_NOTICE.html
%license plugins/pyramid/LGPL.html


%files -f geoserver-querylayer-libs.txt querylayer
%doc plugins/querylayer/NOTICE.html
%license plugins/querylayer/GPL.html


%files -f geoserver-sldservice-libs.txt sldservice
%doc plugins/sldservice/NOTICE.html
%license plugins/sldservice/GPL.html


%files -f geoserver-sqlserver-libs.txt sqlserver
%doc plugins/sqlserver/GEOTOOLS_NOTICE.html
%license plugins/sqlserver/LGPL.html


%files -f geoserver-vectortiles-libs.txt vectortiles
%doc plugins/vectortiles/NOTICE.html
%license plugins/vectortiles/GPL.html


%files -f geoserver-wcs2_0-eo-libs.txt wcs2_0-eo
%doc plugins/wcs2_0-eo/NOTICE.html
%license plugins/wcs2_0-eo/GPL.html


%files -f geoserver-web-resource-libs.txt web-resource
%doc plugins/web-resource/NOTICE.html
%license plugins/web-resource/GPL.html


%files -f geoserver-wmts-multi-dimensional-libs.txt wmts-multi-dimensional
%doc plugins/wmts-multi-dimensional/NOTICE.html
%license plugins/wmts-multi-dimensional/GPL.html


%files -f geoserver-wps-cluster-hazelcast-libs.txt wps-cluster-hazelcast
%doc plugins/wps-cluster-hazelcast/NOTICE.html
%license plugins/wps-cluster-hazelcast/GPL.html


%files -f geoserver-wps-download-libs.txt wps-download
%doc plugins/wps-download/NOTICE.html
%license plugins/wps-download/GPL.html


%files -f geoserver-wps-jdbc-libs.txt wps-jdbc
%doc plugins/wps-jdbc/GEOTOOLS_NOTICE.html plugins/wps-jdbc/NOTICE.html
%license plugins/wps-jdbc/GPL.html plugins/wps-jdbc/LGPL.html


%files -f geoserver-wps-libs.txt wps
%doc plugins/wps/GEOTOOLS_NOTICE.html plugins/wps/NOTICE.html
%license plugins/wps/GPL.html plugins/ysld/LGPL.html


%files -f geoserver-xslt-libs.txt xslt
%doc plugins/xslt/NOTICE.html
%license plugins/xslt/GPL.html


%files -f geoserver-ysld-libs.txt ysld
%doc plugins/ysld/GEOTOOLS_NOTICE.html plugins/ysld/NOTICE.html
%license plugins/ysld/GPL.html plugins/ysld/LGPL.html


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


%post gdal
# Link in correct version og GDAL JAR on post-install.
%{__ln_s} %{_javadir}/gdal/gdal.jar %{geoserver_webapp}/WEB-INF/lib/gdal-$(%{_bindir}/rpm --qf '%%{version}' -q gdal-java).jar


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
