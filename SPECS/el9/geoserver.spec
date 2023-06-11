%global geoserver_major_version %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global geoserver_minor_version %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global geoserver_major_minor %{geoserver_major_version}.%{geoserver_minor_version}

%global geoserver_cache %{_var}/cache/geoserver
%global geoserver_data %{_sharedstatedir}/geoserver
%global geoserver_logs %{_var}/log/geoserver
%global geoserver_webapp %{_sharedstatedir}/tomcat/webapps/geoserver
%global geoserver_source_base_url https://prdownloads.sourceforge.net/geoserver/GeoServer/%{rpmbuild_version}
%global geoserver_source_url %{geoserver_source_base_url}/extensions/geoserver-%{rpmbuild_version}
%global geoserver_community_url https://build.geoserver.org/geoserver/%{geoserver_major_minor}.x/community-latest/geoserver-%{geoserver_major_minor}-SNAPSHOT
%global tomcat_confd %{_sysconfdir}/tomcat/conf.d

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

Source0:        %{geoserver_source_base_url}/geoserver-%{version}-war.zip
Source1:        %{geoserver_source_url}-app-schema-plugin.zip
Source2:        %{geoserver_source_url}-authkey-plugin.zip
Source4:        %{geoserver_source_url}-charts-plugin.zip
Source5:        %{geoserver_source_url}-control-flow-plugin.zip
Source6:        %{geoserver_source_url}-css-plugin.zip
Source10:       %{geoserver_source_url}-dxf-plugin.zip
Source11:       %{geoserver_source_url}-excel-plugin.zip
Source12:       %{geoserver_source_url}-feature-pregeneralized-plugin.zip
Source13:       %{geoserver_source_url}-gdal-plugin.zip
Source15:       %{geoserver_source_url}-geofence-server-plugin.zip
Source16:       %{geoserver_source_url}-geofence-wps-plugin.zip
Source17:       %{geoserver_source_url}-geopkg-output-plugin.zip
Source20:       %{geoserver_source_url}-h2-plugin.zip
Source21:       %{geoserver_source_url}-imagemap-plugin.zip
Source22:       %{geoserver_source_url}-importer-plugin.zip
Source26:       %{geoserver_source_url}-mapml-plugin.zip
Source27:       %{geoserver_source_url}-mbstyle-plugin.zip
Source30:       %{geoserver_source_url}-monitor-plugin.zip
Source31:       %{geoserver_source_url}-mysql-plugin.zip
Source34:       %{geoserver_source_url}-ogr-wfs-plugin.zip
Source35:       %{geoserver_source_url}-ogr-wps-plugin.zip
Source36:       %{geoserver_source_url}-oracle-plugin.zip
Source37:       %{geoserver_source_url}-params-extractor-plugin.zip
Source38:       %{geoserver_source_url}-printing-plugin.zip
Source39:       %{geoserver_source_url}-pyramid-plugin.zip
Source40:       %{geoserver_source_url}-querylayer-plugin.zip
Source41:       %{geoserver_source_url}-sldservice-plugin.zip
Source42:       %{geoserver_source_url}-sqlserver-plugin.zip
Source43:       %{geoserver_source_url}-vectortiles-plugin.zip
Source45:       %{geoserver_source_url}-web-resource-plugin.zip
Source46:       %{geoserver_source_url}-wmts-multi-dimensional-plugin.zip
Source48:       %{geoserver_source_url}-wps-download-plugin.zip
Source50:       %{geoserver_source_url}-wps-plugin.zip
Source51:       %{geoserver_source_url}-xslt-plugin.zip
Source52:       %{geoserver_source_url}-ysld-plugin.zip

# GeoNode's version of the archive.
Source60:       https://artifacts.geonode.org/geoserver/%{version}/geoserver.war

# These libraries are necessary for GeoFence server plugin to work and were extracted from the
# geonode/geoserver:2.23.1 docker image:
#  https://osgeo-org.atlassian.net/jira/core/projects/GEOS/issues/GEOS-9548
Source61:       https://maven.geo-solutions.it/org/hibernatespatial/hibernate-spatial-postgis/1.1.3.2/hibernate-spatial-postgis-1.1.3.2.jar
Source62:       https://repo1.maven.org/maven2/org/postgis/postgis-jdbc/1.3.3/postgis-jdbc-1.3.3.jar

# Community plugins.
Source99:       %{geoserver_community_url}-backup-restore-plugin.zip
Source100:      %{geoserver_community_url}-gdal-wcs-plugin.zip
Source101:      %{geoserver_community_url}-gdal-wps-plugin.zip
Source102:      %{geoserver_community_url}-geopkg-plugin.zip
Source103:      %{geoserver_community_url}-ogr-datastore-plugin.zip
Source104:      %{geoserver_community_url}-s3-geotiff-plugin.zip
Source105:      %{geoserver_community_url}-saml-plugin.zip
Source106:      %{geoserver_community_url}-sec-keycloak-plugin.zip
Source107:      %{geoserver_community_url}-sec-oauth2-geonode-plugin.zip
Source108:      %{geoserver_community_url}-sec-oauth2-github-plugin.zip
Source109:      %{geoserver_community_url}-sec-oauth2-google-plugin.zip
Source110:      %{geoserver_community_url}-sec-oauth2-openid-connect-plugin.zip
Source111:      %{geoserver_community_url}-taskmanager-core-plugin.zip
Source112:      %{geoserver_community_url}-taskmanager-s3-plugin.zip
Source113:      %{geoserver_community_url}-vsi-plugin.zip
Source114:      %{geoserver_community_url}-webp-plugin.zip

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
Requires:      geoserver-geofence = %{version}-%{release}
Requires:      geoserver-oracle = %{version}-%{release}

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
for plugin in app-schema authkey backup-restore charts control-flow css dxf excel feature-pregeneralized gdal geofence geopkg geonode h2 imagemap importer mapml mbstyle monitor mysql oauth2 params-extractor printing pyramid querylayer saml s3-geotiff sldservice sqlserver taskmanager vectortiles web-resource webp wmts-multi-dimensional wps xslt ysld; do
    %{__mkdir_p} plugins/${plugin}
done
%{__unzip} %{SOURCE1}  -d plugins/app-schema
%{__unzip} %{SOURCE2}  -d plugins/authkey
%{__unzip} %{SOURCE99}  -d plugins/backup-restore
%{__unzip} %{SOURCE4}  -d plugins/charts
%{__unzip} %{SOURCE5}  -d plugins/control-flow
%{__unzip} %{SOURCE6}  -d plugins/css
%{__unzip} %{SOURCE10} -d plugins/dxf
%{__unzip} %{SOURCE11} -d plugins/excel
%{__unzip} %{SOURCE12} -d plugins/feature-pregeneralized
%{__unzip} %{SOURCE13} -d plugins/gdal
%{__unzip} -o %{SOURCE34} -d plugins/gdal
%{__unzip} -o %{SOURCE35} -d plugins/gdal
%{__unzip} -o %{SOURCE100} -d plugins/gdal
%{__unzip} -o %{SOURCE101} -d plugins/gdal
%{__unzip} -o %{SOURCE103} -d plugins/gdal
%{__unzip} -o %{SOURCE113} -d plugins/gdal
%{__unzip} %{SOURCE15} -d plugins/geofence
%{__unzip} -o %{SOURCE16} -d plugins/geofence
%{__unzip} %{SOURCE60} -d plugins/geonode
%{__unzip} %{SOURCE17} -d plugins/geopkg
%{__unzip} -o %{SOURCE102} -d plugins/geopkg
%{__unzip} %{SOURCE20} -d plugins/h2
%{__unzip} %{SOURCE21} -d plugins/imagemap
%{__unzip} %{SOURCE22} -d plugins/importer
%{__unzip} %{SOURCE26} -d plugins/mapml
%{__unzip} %{SOURCE27} -d plugins/mbstyle
%{__unzip} %{SOURCE30} -d plugins/monitor
%{__unzip} %{SOURCE31} -d plugins/mysql
%{__unzip} %{SOURCE36} -d plugins/oracle
%{__unzip} %{SOURCE37} -d plugins/params-extractor
%{__unzip} %{SOURCE38} -d plugins/printing
%{__unzip} %{SOURCE39} -d plugins/pyramid
%{__unzip} %{SOURCE40} -d plugins/querylayer
%{__unzip} %{SOURCE106} -d plugins/oauth2
%{__unzip} -o %{SOURCE107} -d plugins/oauth2
%{__unzip} -o %{SOURCE108} -d plugins/oauth2
%{__unzip} -o %{SOURCE109} -d plugins/oauth2
%{__unzip} -o %{SOURCE110} -d plugins/oauth2
%{__unzip} %{SOURCE105} -d plugins/saml
%{__unzip} %{SOURCE104} -d plugins/s3-geotiff
%{__unzip} %{SOURCE41} -d plugins/sldservice
%{__unzip} %{SOURCE42} -d plugins/sqlserver
%{__unzip} %{SOURCE111} -d plugins/taskmanager
%{__unzip} -o %{SOURCE112} -d plugins/taskmanager
%{__unzip} %{SOURCE43} -d plugins/vectortiles
%{__unzip} %{SOURCE45} -d plugins/web-resource
%{__unzip} %{SOURCE114} -d plugins/webp
%{__unzip} %{SOURCE46} -d plugins/wmts-multi-dimensional
%{__unzip} %{SOURCE48} -d plugins/wps
%{__unzip} -o %{SOURCE50} -d plugins/wps
%{__unzip} %{SOURCE51} -d plugins/xslt
%{__unzip} %{SOURCE52} -d plugins/ysld


%install
%{__install} -m 0770 -d \
 %{buildroot}%{geoserver_data} \
 %{buildroot}%{geoserver_logs} \
 %{buildroot}%{geoserver_cache}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__install} -m 0755 -d %{buildroot}%{tomcat_confd}
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}

# Install GeoServer data into separate location.
%{__mv} -v %{buildroot}%{geoserver_webapp}/data %{buildroot}%{geoserver_data}
%{__ln_s} %{geoserver_data}/data %{buildroot}%{geoserver_webapp}

%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib -type f -name \*.jar > geoserver-libs.txt
%{__sed} -i -e 's|%{buildroot}||g' geoserver-libs.txt

for plugin in app-schema authkey backup-restore charts control-flow css dxf excel feature-pregeneralized gdal geopkg h2 imagemap importer mapml mbstyle monitor mysql oauth2 params-extractor printing pyramid querylayer saml s3-geotiff sldservice sqlserver vectortiles web-resource webp wmts-multi-dimensional wps xslt ysld; do
    # Rename any jars with "SNAPSHOT" versions in their names.
    %{_bindir}/find plugins/${plugin} -type f -name \*%{geoserver_major_minor}-SNAPSHOT.jar -exec %{__python3} -c "import os; os.rename('{}', '{}'.replace('%{geoserver_major_minor}-SNAPSHOT', '%{version}'))" \;
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
%{__install} %{SOURCE61} %{SOURCE62} %{buildroot}%{geoserver_webapp}/WEB-INF/lib
echo "%{geoserver_webapp}/WEB-INF/lib/$(basename %{SOURCE61})" >> geoserver-geofence-libs.txt
echo "%{geoserver_webapp}/WEB-INF/lib/$(basename %{SOURCE62})" >> geoserver-geofence-libs.txt

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

# Create Tomcat configuration file that will set up the environment.
cat >> %{buildroot}%{tomcat_confd}/geoserver.conf <<EOF
GEOSERVER_DATA_DIR="\${GEOSERVER_DATA_DIR:-%{geoserver_data}/data}"
export GEOSERVER_DATA_DIR

GEOSERVER_ENCODING="\${GEOSERVER_ENCODING:-UTF-8}"
export GEOSERVER_ENCODING

LD_LIBRARY_PATH="\${LD_LIBRARY_PATH:-%{_usr}/lib/java/gdal:%{_libdir}}"
export LD_LIBRARY_PATH

PROXY_BASE_URL="\${PROXY_BASE_URL:-http://localhost:8080/geoserver}"
export PROXY_BASE_URL

JDK_JAVA_OPTIONS="\${JDK_JAVA_OPTIONS} \\
-Dfile.encoding=UTF8 \\
-Dgeoserver.xframe.shouldSetPolicy=\${GEOSERVER_XFRAME_OPTIONS:-true} \\
-Dgwc.context.suffix=gwc \\
-Djava.awt.headless=true \\
-Djavax.servlet.request.encoding=\${GEOSERVER_ENCODING} \\
-Djavax.servlet.response.encoding=\${GEOSERVER_ENCODING} \\
-Djts.overlay=ng \\
-Dorg.geotools.coverage.jaiext.enabled=true \\
-Dorg.geotools.localDateTimeHandling=true \\
-Dorg.geotools.referencing.forceXY=true \\
-Dorg.geotools.shapefile.datetime=\${GEOSERVER_SHAPEFILE_DATETIME:-true} \\
-Duser.timezone=\${GEOSERVER_TIMEZONE:-GMT} \\
-Duser.language=\${GEOSERVER_LANGUAGE:-en} \\
-Duser.region=\${GEOSERVER_REGION:-US} \\
-Duser.country=\${GEOSERVER_COUNTRY:-US} \\
-Dsun.java2d.renderer.pixelsize=8192 \\
-Dsun.java2d.renderer.useThreadLocal=false \\
-Dsun.java2d.renderer=org.marlin.pisces.PiscesRenderingEngine \\
-DALLOW_ENV_PARAMETRIZATION=true \\
-DENABLE_JSONP=\${GEOSERVER_ENABLE_JSONP:-true} \\
-DGEOSERVER_CSRF_DISABLED=\${GEOSERVER_CSRF_DISABLED:-false} \\
-DGEOSERVER_CSRF_WHITELIST=\${GEOSERVER_CSRF_WHITELIST:-} \\
-DGEOSERVER_DATA_DIR=\${GEOSERVER_DATA_DIR} \\
-DGEOSERVER_FILEBROWSER_HIDEFS=\${GEOSERVER_FILEBROWSER_HIDEFS:-false} \\
-DGEOSERVER_LOG_LOCATION=\${GEOSERVER_LOG_LOCATION:-%{geoserver_logs}/geoserver.log} \\
-DGS-SHAPEFILE-CHARSET=\${GEOSERVER_ENCODING} \\
-DPRINT_BASE_URL=\${PROXY_BASE_URL}/pdf \\
-DPROXY_BASE_URL=\${PROXY_BASE_URL} \\
-Xbootclasspath/a:%{geoserver_webapp}/WEB-INF/lib/marlin-0.9.3.jar \\
-Xms\${GEOSERVER_MINIMUM_MEMORY:-512m} \\
-Xmx\${GEOSERVER_MAXIMUM_MEMORY:-2048m} \\
-XX:ConcGCThreads=5 \\
-XX:MaxGCPauseMillis=200 \\
-XX:NewRatio=2 \\
-XX:ParallelGCThreads=20 \\
-XX:PerfDataSamplingInterval=500 \\
-XX:SoftRefLRUPolicyMSPerMB=36000 \\
-XX:+CMSClassUnloadingEnabled \\
-XX:+UseG1GC \\
-server"
export JDK_JAVA_OPTIONS
EOF


%post
# Copy in GDAL jar to a versioned location.
%{__cp} -p %{_javadir}/gdal/gdal.jar %{geoserver_webapp}/WEB-INF/lib/gdal-$(%{_bindir}/rpm --qf '%%{version}' -q gdal-java).jar


%files -f geoserver-libs-uniq.txt
%doc README.html target/VERSION.txt
%license license/*.html
# Exclude duplicate JAR from community plugin.
%exclude %{geoserver_webapp}/WEB-INF/lib/bcprov-jdk15-1.46.jar
%{geoserver_webapp}/data
%{geoserver_webapp}/index.html
%{geoserver_webapp}/META-INF
%{tomcat_confd}/geoserver.conf
%dir %{geoserver_webapp}/WEB-INF
%{geoserver_webapp}/WEB-INF/*.xml
%dir %{geoserver_webapp}/WEB-INF/classes
%dir %{geoserver_webapp}/WEB-INF/lib
%defattr(-, tomcat, tomcat, -)
%dir %{geoserver_cache}
%dir %{geoserver_logs}
%dir %{geoserver_data}
%dir %{geoserver_data}/data
%defattr(-, root, root, -)

%files data
%defattr(0664,tomcat,tomcat,0775)
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
