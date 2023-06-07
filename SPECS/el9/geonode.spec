%global geoserver_data %{_sharedstatedir}/geoserver
%global geonode_home %{_sharedstatedir}/geonode
%global geonode_logs %{_var}/log/geonode
%global geonode_root %{_datadir}/geonode
%global geonode_run /run/geonode
%global geonode_user geonode
%global geonode_group tomcat
%global geonode_uid 737
%global geonode_gid 53

# The following macros are also required:
# * geoserver_version
%global geoserver_version_num %(echo %{geoserver_version} | awk -F- '{ print $1 }')
%global geoserver_release %(echo %{geoserver_version} | awk -F- '{ print $2 }')


Name:           geonode
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoNode is an open source platform that facilitates the creation, sharing, and collaborative use of geospatial data.
License:        GPLv3
URL:            https://geonode.org
Source0:        https://github.com/GeoNode/geonode/archive/refs/tags/%{version}.tar.gz
Source1:        https://artifacts.geonode.org/geoserver/%{geoserver_version}/geonode-geoserver-ext-web-app-data.zip


BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gdal-devel
BuildRequires:  geos-devel
BuildRequires:  lapack-devel
BuildRequires:  lcms2-devel
BuildRequires:  libffi-devel
BuildRequires:  libimagequant-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libraqm-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  nodejs-devel
BuildRequires:  proj-devel
BuildRequires:  postgis
BuildRequires:  postgresql%{postgres_version}-contrib
BuildRequires:  postgresql%{postgres_version}-devel
BuildRequires:  python3-devel
BuildRequires:  python3-gdal
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  systemd-rpm-macros
BuildRequires:  tk-devel
BuildRequires:  zlib-devel

Provides:       bundled(python3-cffi)
Provides:       bundled(python3-gevent)
Provides:       bundled(python3-gunicorn)
Provides:       bundled(python3-lxml)
Provides:       bundled(python3-numpy)
Provides:       bundled(python3-psycopg2)
Provides:       bundled(python3-pyproj)
Provides:       bundled(python3-PyYAML)
Provides:       bundled(python3-shapely)

Requires:       postgresql%{postgres_version}
Requires:       python3-gdal

%description
GeoNode is a web-based application and platform for developing geospatial information systems (GIS) and for deploying spatial data infrastructures (SDI).


%package -n geoserver-geonode-data
BuildArch:      noarch
Summary:        GeoServer GeoNode Data
Version:        %{geoserver_version_num}
Release:        %{geoserver_release}%{?dist}
Requires:       geoserver = %{geoserver_version}

%description -n geoserver-geonode-data
GeoServer data for use with a GeoNode instance.


%prep
%autosetup


%build
%{_bindir}/python3 -m venv venv
./venv/bin/python3 -m pip install pip --upgrade
./venv/bin/python3 -m pip install setuptools wheel --upgrade
./venv/bin/python3 -m pip install \
--no-binary cffi,gevent,gunicorn,lxml,numpy,psycopg2,pyproj,Pillow,PyYAML,Shapely,uWSGI \
-v -r requirements.txt


%install
%{__install} -m 0770 -d %{buildroot}%{geoserver_data}
%{__unzip} %{SOURCE1} -d %{buildroot}%{geoserver_data}
%{__install} -d -m 0755 \
 %{buildroot}%{_usr}/lib/tmpfiles.d \
 %{buildroot}%{geonode_root}
%{__install} -d -m 0750 \
 %{buildroot}%{geonode_home} \
 %{buildroot}%{geonode_logs} \
 %{buildroot}%{geonode_run}

# geonode tmpfiles.d entry
echo "d %{geonode_run} 0750 %{geonode_user} %{geonode_group} -" > \
       %{buildroot}%{_usr}/lib/tmpfiles.d/%{name}.conf

# Copy module and virtual environment.
for dir in geonode venv; do
    %{__cp} -rp ${dir} %{buildroot}%{geonode_root}/${dir}
done

# Ensure VIRTUAL_ENV points to the installed location in activation scripts.
%{__sed} -i -e 's|^VIRTUAL_ENV=.*|VIRTUAL_ENV="%{geonode_root}/venv"|g' \
  %{buildroot}%{geonode_root}/venv/bin/activate
%{__sed} -i -e 's|VIRTUAL_ENV ".*"|VIRTUAL_ENV="%{geonode_root}/venv"|g' \
  %{buildroot}%{geonode_root}/venv/bin/activate.{csh,fish}

# Correct shebang path for files in virtualenv directory.
%{__sed} -i \
  -e '1s|#!/usr/bin/env python|#!%{geonode_root}/venv/bin/python3|' \
  -e '1s|#!/.*/venv/bin/python3|#!%{geonode_root}/venv/bin/python3|' \
  %{buildroot}%{geonode_root}/venv/bin/automat* \
  %{buildroot}%{geonode_root}/venv/bin/celery* \
  %{buildroot}%{geonode_root}/venv/bin/cftp* \
  %{buildroot}%{geonode_root}/venv/bin/ckeygen* \
  %{buildroot}%{geonode_root}/venv/bin/con* \
  %{buildroot}%{geonode_root}/venv/bin/coverage* \
  %{buildroot}%{geonode_root}/venv/bin/create* \
  %{buildroot}%{geonode_root}/venv/bin/csv2rdf* \
  %{buildroot}%{geonode_root}/venv/bin/django-admin* \
  %{buildroot}%{geonode_root}/venv/bin/dotenv* \
  %{buildroot}%{geonode_root}/venv/bin/f2py* \
  %{buildroot}%{geonode_root}/venv/bin/faker* \
  %{buildroot}%{geonode_root}/venv/bin/flake* \
  %{buildroot}%{geonode_root}/venv/bin/futurize* \
  %{buildroot}%{geonode_root}/venv/bin/geolinks* \
  %{buildroot}%{geonode_root}/venv/bin/gunicorn* \
  %{buildroot}%{geonode_root}/venv/bin/inv* \
  %{buildroot}%{geonode_root}/venv/bin/ipython* \
  %{buildroot}%{geonode_root}/venv/bin/jp.py* \
  %{buildroot}%{geonode_root}/venv/bin/jsonschema* \
  %{buildroot}%{geonode_root}/venv/bin/ma* \
  %{buildroot}%{geonode_root}/venv/bin/normalizer* \
  %{buildroot}%{geonode_root}/venv/bin/pasteurize* \
  %{buildroot}%{geonode_root}/venv/bin/pip* \
  %{buildroot}%{geonode_root}/venv/bin/py* \
  %{buildroot}%{geonode_root}/venv/bin/rdf* \
  %{buildroot}%{geonode_root}/venv/bin/report* \
  %{buildroot}%{geonode_root}/venv/bin/slugify* \
  %{buildroot}%{geonode_root}/venv/bin/sqlformat* \
  %{buildroot}%{geonode_root}/venv/bin/stone* \
  %{buildroot}%{geonode_root}/venv/bin/tkconch* \
  %{buildroot}%{geonode_root}/venv/bin/tldextract* \
  %{buildroot}%{geonode_root}/venv/bin/tqdm* \
  %{buildroot}%{geonode_root}/venv/bin/trial* \
  %{buildroot}%{geonode_root}/venv/bin/twist* \
  %{buildroot}%{geonode_root}/venv/bin/uwsgi* \
  %{buildroot}%{geonode_root}/venv/bin/wandb* \
  %{buildroot}%{geonode_root}/venv/bin/wb* \
  %{buildroot}%{geonode_root}/venv/bin/wheel* \
  %{buildroot}%{geonode_root}/venv/bin/wsdump* \
  %{buildroot}%{geonode_root}/venv/bin/xml2json* \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/bin/django-admin.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/conf/project_template/manage.py-tpl \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/rdflib/plugins/parsers/notation3.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/sqlparse/cli.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/proto/wandb_internal_codegen.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/sdk/lib/fsm.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/vendor/watchdog_0_9_0/wandb_watchdog/watchmedo.py

# Prevent following error:
#   failed: mode 100755 Bad magic format `version %%#x (MVP)' (bad format char: #)
%{__chmod} a-x \
   %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/geonode_mapstore_client/static/mapstore/dist/cesium/ThirdParty/basis_transcoder.wasm \
   %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/geonode_mapstore_client/static/mapstore/dist/cesium/ThirdParty/draco_decoder.wasm


%files
%doc AUTHORS README.md SECURITY.md
%license license.txt
%{geonode_root}
%{_usr}/lib/tmpfiles.d/%{name}.conf
%defattr(-, %{geonode_user}, %{geonode_group}, -)
%dir %{geonode_logs}
%dir %{geonode_home}
%dir %{geonode_run}

%files -n geoserver-geonode-data
%defattr(0664,tomcat,tomcat,0775)
%config(noreplace) %{geoserver_data}/data/*


%pre
%{_bindir}/getent group %{geonode_group} >/dev/null || \
    %{_sbindir}/groupadd \
        --force \
        --gid %{geonode_gid} \
        --system \
        %{geonode_group}

%{_bindir}/getent passwd %{geonode_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{geonode_uid} \
        --gid %{geonode_group} \
        --comment "GeoNode User" \
        --shell %{_sbindir}/nologin \
        --home-dir %{geonode_home} \
        --no-create-home \
        --system \
        %{geonode_user}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
