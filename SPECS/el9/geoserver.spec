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

License:        ASL 1.1, ASL 2.0, EPL, EPSG, GeoTools, HSQL, GPLv2, GPLv3, LGPL-2.1, OGC, and W3C
URL:            https://geoserver.org

BuildArch:      noarch
BuildRequires:  unzip

Requires:       gdal
Requires:       gdal-java
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


%package oracle
Summary:       GeoServer Oracle Extension
License:       LGPL-2.1 and Oracle FUTC
Requires:      geoserver = %{version}-%{release}

%description oracle
%{summary}


%prep
%autosetup -c
for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output gwc-s3 h2 imagemap importer inspire jp2k libjpeg-turbo mapml mbstyle metadata mongodb monitor mysql ogr-wfs ogr-wps params-extractor printing pyramid querylayer sldservice sqlserver vectortiles wcs2_0-eo web-resource wmts-multi-dimensional wps-cluster hazelcast wps-download wps-jdbc wps xslt ysld; do
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

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-libs.txt

for plugin in app-schema authkey cas charts control-flow css csw-iso csw db2 dxf excel feature-pregeneralized gdal geofence geofence-server geofence-wps geopkg-output gwc-s3 h2 imagemap importer inspire jp2k libjpeg-turbo mapml mbstyle metadata mongodb monitor mysql ogr-wfs ogr-wps params-extractor printing pyramid querylayer sldservice sqlserver vectortiles wcs2_0-eo web-resource wmts-multi-dimensional wps-cluster-hazelcast wps-download wps-jdbc wps xslt ysld; do
    %{_bindir}/find plugins/${plugin} -type f -name \*.jar >> geoserver-libs.txt
    %{__sed} -i -e "s|plugins/${plugin}|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-libs.txt
    %{__install} plugins/${plugin}/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib
done
%{_bindir}/sort geoserver-libs.txt | %{_bindir}/uniq > geoserver-libs-uniq.txt

# Package Oracle separately due to licensing.
%{_bindir}/find plugins/oracle -type f -name \*.jar > geoserver-oracle-libs.txt
%{__sed} -i -e "s|plugins/oracle|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-oracle-libs.txt
%{__install} plugins/oracle/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib


%files -f geoserver-libs-uniq.txt
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


%files -f geoserver-oracle-libs.txt oracle
%doc plugins/oracle/GEOTOOLS_NOTICE.html plugins/oracle/oracle-readme.txt
%license plugins/oracle/LGPL.html plugins/oracle/OracleFUTC.html


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


%post
# Link in correct version og GDAL JAR on post-install.
%{__ln_s} %{_javadir}/gdal/gdal.jar %{geoserver_webapp}/WEB-INF/lib/gdal-$(%{_bindir}/rpm --qf '%%{version}' -q gdal-java).jar


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
