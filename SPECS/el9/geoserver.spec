%global geoserver_data %{_sharedstatedir}/geoserver
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
Source10:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-dxf-plugin.zip
Source11:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-excel-plugin.zip
Source12:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-feature-pregeneralized-plugin.zip
Source13:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-gdal-plugin.zip
Source14:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-plugin.zip
Source15:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-server-plugin.zip
Source16:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geofence-wps-plugin.zip
Source17:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-geopkg-output-plugin.zip
Source20:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-h2-plugin.zip
Source21:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-imagemap-plugin.zip
Source22:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-importer-plugin.zip
Source24:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-jp2k-plugin.zip
Source26:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mapml-plugin.zip
Source27:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-mbstyle-plugin.zip
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
Source45:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-web-resource-plugin.zip
Source46:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wmts-multi-dimensional-plugin.zip
Source47:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-cluster-hazelcast-plugin.zip
Source48:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-download-plugin.zip
Source50:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-wps-plugin.zip
Source51:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-xslt-plugin.zip
Source52:       %{geoserver_source_url}/%{version}/extensions/geoserver-%{version}-ysld-plugin.zip
Source60:       https://artifacts.geonode.org/geoserver/%{version}/geoserver.war

%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data.
Designed for interoperability, it publishes data from any major spatial data source using open standards.


%package data
Summary:       GeoServer Data
License:       GeoSolutions
Requires:      geoserver = %{version}-%{release}

%description data
Default data for use with a GeoServer instance.


%package geofence
Summary:       GeoServer GeoFence Extension
License:       GPLv2
Requires:      geoserver = %{version}-%{release}

%description geofence
GeoFence is a GeoServer plugin that allows far more advanced security configurations than the default GeoServer Security subsystem, such as rules that combine data and service restrictions.


%package geonode
Summary:       GeoServer GeoNode Extension
License:       ASL 1.1, ASL 2.0, GPLv2, and GPLv3
Requires:      geoserver = %{version}-%{release}

%description geonode
%{summary}


%package oracle
Summary:       GeoServer Oracle Extension
License:       LGPL-2.1 and Oracle FUTC
Requires:      geoserver = %{version}-%{release}

%description oracle
%{summary}


%prep
%autosetup -c
for plugin in app-schema authkey cas charts control-flow css dxf excel feature-pregeneralized gdal geofence geopkg-output geonode h2 imagemap importer jp2k mapml mbstyle monitor mysql ogr-wfs ogr-wps params-extractor printing pyramid querylayer sldservice sqlserver vectortiles web-resource wmts-multi-dimensional wps-cluster hazelcast wps-download wps xslt ysld; do
    %{__mkdir_p} plugins/${plugin}
done
%{__unzip} %{SOURCE1}  -d plugins/app-schema
%{__unzip} %{SOURCE2}  -d plugins/authkey
%{__unzip} %{SOURCE3}  -d plugins/cas
%{__unzip} %{SOURCE4}  -d plugins/charts
%{__unzip} %{SOURCE5}  -d plugins/control-flow
%{__unzip} %{SOURCE6}  -d plugins/css
%{__unzip} %{SOURCE10} -d plugins/dxf
%{__unzip} %{SOURCE11} -d plugins/excel
%{__unzip} %{SOURCE12} -d plugins/feature-pregeneralized
%{__unzip} %{SOURCE13} -d plugins/gdal
%{__unzip} %{SOURCE14} -d plugins/geofence
%{__unzip} -o %{SOURCE15} -d plugins/geofence
%{__unzip} -o %{SOURCE16} -d plugins/geofence
%{__unzip} %{SOURCE17} -d plugins/geopkg-output
%{__unzip} %{SOURCE20} -d plugins/h2
%{__unzip} %{SOURCE21} -d plugins/imagemap
%{__unzip} %{SOURCE22} -d plugins/importer
%{__unzip} %{SOURCE24} -d plugins/jp2k
%{__unzip} %{SOURCE26} -d plugins/mapml
%{__unzip} %{SOURCE27} -d plugins/mbstyle
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
%{__unzip} %{SOURCE45} -d plugins/web-resource
%{__unzip} %{SOURCE46} -d plugins/wmts-multi-dimensional
%{__unzip} %{SOURCE47} -d plugins/wps-cluster-hazelcast
%{__unzip} %{SOURCE48} -d plugins/wps-download
%{__unzip} %{SOURCE50} -d plugins/wps
%{__unzip} %{SOURCE51} -d plugins/xslt
%{__unzip} %{SOURCE52} -d plugins/ysld
%{__unzip} %{SOURCE60} -d plugins/geonode


%install
%{__install} -m 0750 -d %{buildroot}%{geoserver_data}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}
%{__mv} -v %{buildroot}%{geoserver_webapp}/data %{buildroot}%{geoserver_data}
%{__ln_s} %{geoserver_data}/data %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-libs.txt

for plugin in app-schema authkey cas charts control-flow css dxf excel feature-pregeneralized gdal geopkg-output h2 imagemap importer jp2k mapml mbstyle monitor mysql ogr-wfs ogr-wps params-extractor printing pyramid querylayer sldservice sqlserver vectortiles web-resource wmts-multi-dimensional wps-cluster-hazelcast wps-download wps xslt ysld; do
    %{_bindir}/find plugins/${plugin} -type f -name \*.jar >> geoserver-libs.txt
    %{__sed} -i -e "s|plugins/${plugin}|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-libs.txt
    %{__install} plugins/${plugin}/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib
done
%{_bindir}/sort geoserver-libs.txt | %{_bindir}/uniq > geoserver-libs-uniq.txt

# Package Oracle separately due to licensing.
%{_bindir}/find plugins/oracle -type f -name \*.jar > geoserver-oracle-libs.txt
%{__sed} -i -e "s|plugins/oracle|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-oracle-libs.txt
%{__install} plugins/oracle/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib

# Package geofence separately as it requires extra configuration.
pushd plugins/geofence
for jar in $(ls *.jar); do
    # Remove duplicate jars.
    if [ -f %{buildroot}%{geoserver_webapp}/WEB-INF/lib/${jar} ]; then
        %{__rm} ${jar}
    fi
done
popd
%{_bindir}/find plugins/geofence -type f -name \*.jar >> geoserver-geofence-libs.txt
%{__sed} -i -e "s|plugins/geofence|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-geofence-libs.txt
%{__install} plugins/geofence/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib

# Package GeoNode's GeoServer files separately.
pushd plugins/geonode/WEB-INF/lib
for jar in $(ls *.jar); do
    # Remove duplicate jars.
    if [ -f %{buildroot}%{geoserver_webapp}/WEB-INF/lib/${jar} ]; then
        %{__rm} ${jar}
    fi
done
popd
%{_bindir}/find plugins/geonode/WEB-INF/lib -type f -name \*.jar >> geoserver-geonode-libs.txt
%{__sed} -i -e "s|plugins/geonode/WEB-INF/lib|%{geoserver_webapp}/WEB-INF/lib|g" geoserver-geonode-libs.txt
%{__install} plugins/geonode/WEB-INF/lib/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib


%post
# Copy in GDAL jar to a versioned location.
%{__cp} -p %{_javadir}/gdal/gdal.jar %{geoserver_webapp}/WEB-INF/lib/gdal-$(%{_bindir}/rpm --qf '%%{version}' -q gdal-java).jar


%files -f geoserver-libs-uniq.txt
%doc README.html target/VERSION.txt
%license license/*.html
%defattr(-, tomcat, tomcat, -)
%dir %{geoserver_data}
%dir %{geoserver_data}/data
%defattr(0664,tomcat,tomcat,0775)
%{geoserver_webapp}/data
%{geoserver_webapp}/index.html
%{geoserver_webapp}/META-INF
%dir %{geoserver_webapp}/WEB-INF
%{geoserver_webapp}/WEB-INF/*.xml
%dir %{geoserver_webapp}/WEB-INF/classes
%dir %{geoserver_webapp}/WEB-INF/lib

%files data
%defattr(-, tomcat, tomcat, -)
%config(noreplace) %{geoserver_data}/data/*

%files -f geoserver-geofence-libs.txt geofence
%doc plugins/geofence/NOTICE.html
%license plugins/geofence/GPL.html

%files -f geoserver-geonode-libs.txt geonode

%files -f geoserver-oracle-libs.txt oracle
%doc plugins/oracle/GEOTOOLS_NOTICE.html plugins/oracle/oracle-readme.txt
%license plugins/oracle/LGPL.html plugins/oracle/OracleFUTC.html


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
