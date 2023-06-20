%global geonode_home %{_sharedstatedir}/geonode
%global geonode_logs %{_var}/log/geonode
%global geonode_root %{_datadir}/geonode
%global geonode_run /run/geonode
%global geonode_user geonode
%global geonode_group tomcat
%global geonode_uid 737
%global geonode_gid 53

# Exclude provides/requires gathering from parts of embedded venv.
%global __provides_exclude_from ^%{geonode_root}/venv/.*$
%global __requires_exclude_from ^%{geonode_root}/venv/bin/.*$

# Prevent duplicate build-ids from copied python3 binary in venv.
%global _build_id_links none


Name:           geonode
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoNode is an open source platform that facilitates the creation, sharing, and collaborative use of geospatial data.
License:        GPLv3
URL:            https://geonode.org
Source0:        https://github.com/GeoNode/geonode/archive/refs/tags/%{version}.tar.gz

BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gdal-devel
BuildRequires:  geos-devel
BuildRequires:  geoserver-geonode
BuildRequires:  geoserver-geonode-data
BuildRequires:  lapack-devel
BuildRequires:  lcms2-devel
BuildRequires:  libffi-devel
BuildRequires:  libimagequant-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libmemcached-awesome-devel
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
Provides:       bundled(python3-google-crc32c)
Provides:       bundled(python3-gunicorn)
Provides:       bundled(python3-lxml)
Provides:       bundled(python3-numpy)
Provides:       bundled(python3-pillow)
Provides:       bundled(python3-psycopg2)
Provides:       bundled(python3-pylibmc)
Provides:       bundled(python3-pyproj)
Provides:       bundled(python3-PyYAML)
Provides:       bundled(python3-shapely)
Provides:       bundled(uwsgi)

Requires:       postgresql%{postgres_version}
Requires:       python3-gdal

%description
GeoNode is a web-based application and platform for developing geospatial information systems (GIS) and for deploying spatial data infrastructures (SDI).


%prep
%autosetup


%build
%{_bindir}/python3 -m venv venv
./venv/bin/python3 -m pip install pip --upgrade
./venv/bin/python3 -m pip install setuptools wheel --upgrade
./venv/bin/python3 -m pip install \
  --no-binary cffi,gevent,google-crc32c,gunicorn,lxml,numpy,psycopg2,pylibmc,pyproj,Pillow,PyYAML,Shapely,uWSGI \
  -v -r requirements.txt


%install
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

# Link geonode module into the virtual environment site modules.
%{__ln_s} %{geonode_root}/geonode \
 %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages

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
  %{buildroot}%{geonode_root}/venv/bin/b* \
  %{buildroot}%{geonode_root}/venv/bin/c* \
  %{buildroot}%{geonode_root}/venv/bin/d* \
  %{buildroot}%{geonode_root}/venv/bin/f* \
  %{buildroot}%{geonode_root}/venv/bin/g* \
  %{buildroot}%{geonode_root}/venv/bin/i* \
  %{buildroot}%{geonode_root}/venv/bin/j* \
  %{buildroot}%{geonode_root}/venv/bin/m* \
  %{buildroot}%{geonode_root}/venv/bin/n* \
  %{buildroot}%{geonode_root}/venv/bin/pa* \
  %{buildroot}%{geonode_root}/venv/bin/pip* \
  %{buildroot}%{geonode_root}/venv/bin/py* \
  %{buildroot}%{geonode_root}/venv/bin/r* \
  %{buildroot}%{geonode_root}/venv/bin/s* \
  %{buildroot}%{geonode_root}/venv/bin/t* \
  %{buildroot}%{geonode_root}/venv/bin/u* \
  %{buildroot}%{geonode_root}/venv/bin/w* \
  %{buildroot}%{geonode_root}/venv/bin/x* \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/bin/django-admin.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/conf/project_template/manage.py-tpl \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/rdflib/plugins/parsers/notation3.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/sqlparse/cli.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/proto/wandb_internal_codegen.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/sdk/lib/fsm.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/vendor/watchdog_0_9_0/wandb_watchdog/watchmedo.py

# Prevent following error and trying to provide python3 from venv.
#   failed: mode 100755 Bad magic format `version %%#x (MVP)' (bad format char: #)
%{__chmod} a-x \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/bin/django-admin.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/django/conf/project_template/manage.py-tpl \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/geonode_mapstore_client/static/mapstore/dist/cesium/ThirdParty/basis_transcoder.wasm \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/geonode_mapstore_client/static/mapstore/dist/cesium/ThirdParty/draco_decoder.wasm \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/rdflib/plugins/parsers/notation3.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/sqlparse/cli.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/proto/wandb_internal_codegen.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/sdk/lib/fsm.py \
  %{buildroot}%{geonode_root}/venv/lib/python%{__default_python3_version}/site-packages/wandb/vendor/watchdog_0_9_0/wandb_watchdog/watchmedo.py


%files
%doc AUTHORS README.md SECURITY.md
%license license.txt
%{geonode_root}
%{_usr}/lib/tmpfiles.d/%{name}.conf
%defattr(-, %{geonode_user}, %{geonode_group}, -)
%dir %{geonode_logs}
%dir %{geonode_home}
%dir %{geonode_run}


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
