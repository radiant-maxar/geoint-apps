# Force CMake to use `build` for its directory, tests assume it.
%global _vpath_builddir build

%global osm2pgsql_min_version 1.6.0
%{!?datrie_version: %global datrie_version 0.8.2}
%{!?pyicu_version: %global pyicu_version 2.10.2}

%bcond_without tests

# Variables for Nominatim paths and user/group.
%global nominatim_base %{_datadir}/%{name}
%global nominatim_conf %{_sysconfdir}/%{name}
%global nominatim_home %{_localstatedir}/lib/%{name}
%global nominatim_data %{nominatim_home}/data
%global nominatim_www %{_var}/www/%{name}
%global nominatim_group nominatim
%global nominatim_user nominatim
%global nominatim_uid 972

# Don't provide for embedded dependencies and use Python 3
# for compiling bytecode.
%global __provides_exclude_from ^%{nominatim_base}/lib-python/.*$
%global __python %{__python3}

Name:           nominatim
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Open Source search based on OpenStreetMap data
License:        GPLv2
URL:            https://github.com/openstreetmap/Nominatim

Source0:        https://github.com/openstreetmap/Nominatim/archive/v%{version}/Nominatim-%{version}.tar.gz
Source1:        https://www.nominatim.org/data/country_grid.sql.gz
Source2:        https://www.nominatim.org/data/gb_postcode_data.sql.gz
Source3:        https://www.nominatim.org/data/us_postcode_data.sql.gz
%if %{with tests}
Source4:        https://download.geofabrik.de/europe/monaco-latest.osm.pbf
%endif

Patch0:         nominatim-external-osm2pgsql.patch
Patch1:         nominatim-no-calculate-postcodes.patch
Patch2:         nominatim-legacy-tokenizer.patch
Patch3:         nominatim-tests-run-serial.patch

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  ccache
BuildRequires:  cmake
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  geos-devel
BuildRequires:  libicu-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  osm2pgsql
BuildRequires:  php-cli
BuildRequires:  php-intl
BuildRequires:  php-mbstring
BuildRequires:  php-pear
BuildRequires:  php-pgsql
BuildRequires:  postgresql%{postgres_version}-devel
BuildRequires:  proj-devel
BuildRequires:  python3-devel
BuildRequires:  python3-dotenv
BuildRequires:  python3-jinja2
BuildRequires:  python3-osmium
BuildRequires:  python3-pip
BuildRequires:  python3-psycopg2
BuildRequires:  python3-psutil
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pyyaml
BuildRequires:  zlib-devel

%if %{with tests}
BuildRequires:  libtidy
BuildRequires:  postgis
BuildRequires:  postgresql%{postgres_version}-contrib
BuildRequires:  postgresql%{postgres_version}-server
# These testing dependencies are installed via Dockerfile.
## PHP:
## BuildRequires:  PHP_CodeSniffer
## BuildRequires:  PHPUnit
## Python:
## BuildRequires:  python3-behave
## BuildRequires:  python3-pyicu
## BuildRequires:  python3-pylint
## BuildRequires:  python3-pytidylib
%endif

Requires:       %{name}-data = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       osm2pgsql >= %{osm2pgsql_min_version}
Requires:       postgresql%{postgres_version}
Requires:       python3-dotenv
Requires:       python3-jinja2
Requires:       python3-osmium
Requires:       python3-psutil
Requires:       python3-psycopg2
Requires:       python3-pyyaml
Requires:       php-fpm
Requires:       php-intl
Requires:       php-pear
Requires:       php-pgsql
# These requirements are included in Nominatim's lib-python directory,
# They are not available in any yum repositories.
# Source: https://github.com/osm-search/Nominatim/blob/master/docs/admin/Installation.md#software
Provides:       bundled(python3-datrie) = %{datrie_version}
Provides:       bundled(python3-pyicu) = %{pyicu_version}


%description
Nominatim (from the Latin, 'by name') is a tool to search OpenStreetMap data
by name and address (geocoding) and to generate synthetic addresses of OSM
points (reverse geocoding). An instance with up-to-date data can be found at
https://nominatim.openstreetmap.org. Nominatim is also used as one of the
sources for the Search box on the OpenStreetMap home page.


%package data
Summary:        Nominatim data files
BuildArch:      noarch

%description data
This package contains Nominatim data files.

%package libs
Summary:        Nominatim library

%description libs
This package contains the Nominatim shared library.


%prep
%autosetup -p1 -n Nominatim-%{version}


%build
%if %{with tests}
# CMake needs to find the Dockerfile-installed binaries
export PATH=${HOME}/.local/bin:${PATH}
%endif

%{__cp} -p %{SOURCE1} data/country_osm_grid.sql.gz
%{__cp} -p %{SOURCE2} %{SOURCE3} data

%cmake -DBUILD_API:BOOL=ON \
       -DBUILD_IMPORTER:BOOL=ON \
       -DBUILD_OSM2PGSQL:BOOL=OFF \
       -DBUILD_MODULE:BOOL=ON \
       -DCMAKE_INSTALL_LIBDIR:PATH=%{_datadir}
%cmake_build


%install
%cmake_install
# Python dependencies that aren't available as system packages; first
# install packages with C extensions from *source* and then install
# source-only dependencies.
%{_bindir}/pip3 install --ignore-installed \
  --target %{buildroot}%{nominatim_base}/lib-python \
  --no-binary datrie -v \
  datrie==%{datrie_version} \
  PyICU==%{pyicu_version}
export PYTHONPATH=%{buildroot}%{nominatim_base}/lib-python:%{python3_sitearch}:%{python3_sitelib}

# Database needs to exist to run `nominatim refresh`.
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{_bindir}/rm -fr "${PGDATA}"
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8
echo "shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"
%{_bindir}/pg_ctl -s start
%{_bindir}/createdb nominatim

# Website
## Set up temporary environment.
### Set up `nominatim_properties` table & `tokenizer` row for `nominatim refresh --website`. This is usually done on import.
%{_bindir}/psql --dbname="nominatim" --command="CREATE TABLE nominatim_properties (property TEXT NOT NULL, value TEXT)"
%{_bindir}/psql --dbname="nominatim" --command="INSERT INTO nominatim_properties (property, value) VALUES ('tokenizer', 'icu')"
### This is also usually done on import.
%{__mkdir_p} %{buildroot}%{nominatim_www}
%{__cp} -r %{buildroot}%{nominatim_conf}/country-names %{buildroot}%{nominatim_www}
%{__cp} -r %{buildroot}%{nominatim_conf}/icu-rules %{buildroot}%{nominatim_www}
%{__cp} %{buildroot}%{nominatim_conf}/country_settings.yaml %{buildroot}%{nominatim_www}
%{__cp} %{buildroot}%{nominatim_conf}/env.defaults %{buildroot}%{nominatim_www}/.env
%{__cp} %{buildroot}%{nominatim_conf}/icu_tokenizer.yaml %{buildroot}%{nominatim_www}

## Install 'website' .php files with `nominatim refresh`, database must be running.
%{buildroot}%{_bindir}/nominatim refresh \
 --website \
 --project-dir %{buildroot}%{nominatim_www}

## Clean out buildroot from any paths in generated PHP.
%{__sed} -i -e "s|%{buildroot}||g" %{buildroot}%{nominatim_www}/website/*.php

## Clean up temporary environment, and add /etc links.
%{__rm} %{buildroot}%{nominatim_www}/.env
%{__ln_s} %{nominatim_conf}/env.defaults %{buildroot}%{nominatim_www}/.env

%{__rm} %{buildroot}%{nominatim_www}/country_settings.yaml %{buildroot}%{nominatim_www}/icu_tokenizer.yaml
%{__ln_s} %{nominatim_conf}/country_settings.yaml %{buildroot}%{nominatim_www}
%{__ln_s} %{nominatim_conf}/icu_tokenizer.yaml %{buildroot}%{nominatim_www}

%{__rm} -fr %{buildroot}%{nominatim_www}/country-names
%{__ln_s} %{nominatim_conf}/country-names %{buildroot}%{nominatim_www}

%{__rm} -fr %{buildroot}%{nominatim_www}/icu-rules
%{__ln_s} %{nominatim_conf}/icu-rules %{buildroot}%{nominatim_www}

# Data
%{__mkdir_p} %{buildroot}%{nominatim_data}/tiger
%{__cp} -rp data/* %{buildroot}%{nominatim_data}/
%{__rm} %{buildroot}%{nominatim_base}/country_osm_grid.sql.gz \
  %{buildroot}%{nominatim_base}/words.sql
%{__ln_s} %{nominatim_data}/country_osm_grid.sql.gz \
  %{nominatim_data}/gb_postcode_data.sql.gz \
  %{nominatim_data}/us_postcode_data.sql.gz \
  %{nominatim_data}/words.sql \
  %{buildroot}%{nominatim_base}/
%{__ln_s} %{nominatim_data}/country_osm_grid.sql.gz \
  %{nominatim_data}/gb_postcode_data.sql.gz \
  %{nominatim_data}/us_postcode_data.sql.gz \
  %{nominatim_data}/words.sql \
  %{buildroot}%{nominatim_www}/

# Library
%{__mkdir_p} %{buildroot}%{_libdir} %{buildroot}%{nominatim_www}/module
%{__mv} %{buildroot}%{nominatim_base}/module/%{name}.so  %{buildroot}%{_libdir}
%{__ln_s} %{_libdir}/%{name}.so %{buildroot}%{nominatim_base}/module
%{__ln_s} %{_libdir}/%{name}.so %{buildroot}%{nominatim_www}/module

# Destroy database.
%{_bindir}/pg_ctl -m fast -s stop
%{__rm} -fr "${PGDATA}"


%check
%if %{with tests}
# Reinitialize PostgreSQL database.
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr "${PGDATA}"
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
cat >> "${PGDATA}/postgresql.conf" <<EOF
# Memory tuning, high value for maintenance work mem to support index
# creation done by data import.
shared_buffers = 4GB
maintenance_work_mem = 12GB
work_mem = 50MB
# Minimal WAL, no archiving.
wal_level = minimal
archive_mode = off
max_wal_senders = 0
# Speed tuning
fsync = off
full_page_writes = off
synchronous_commit = off
EOF

# Start PostgreSQL
%{_bindir}/pg_ctl -s start
%{_bindir}/createuser -S postgres
%{_bindir}/createuser -S www-data

# In rpmbuild environment have to explicitly set the PYTHONPATH to include the
# user's site packages.
export PYTHONPATH=${HOME}/.local/lib/python%{python3_version}/site-packages:%{python3_sitearch}:%{python3_sitelib}

# Invoke testing/linting runner
%ctest

# Clean up.
%{_bindir}/pg_ctl -m fast -s stop
%endif


%files
%doc AUTHORS ChangeLog CONTRIBUTING.md README.md docs
%license COPYING
%{_mandir}/man1/*.1*
%{_bindir}/nominatim
%{nominatim_base}
%exclude %{nominatim_base}/module
%exclude %{nominatim_base}/*.sql*
%exclude %{_datadir}/munin
%config(noreplace) %{nominatim_conf}/env.defaults
%config %{nominatim_conf}/country-names
%config %{nominatim_conf}/icu-rules
%config %{nominatim_conf}/*.json
%config %{nominatim_conf}/*.style
%config %{nominatim_conf}/*.yaml
# Allow nominatim user access to home, data and www directories.
%defattr(0644,%{nominatim_user},%{nominatim_group},0755)
%{nominatim_www}
%exclude %{nominatim_www}/*.sql*
%exclude %{nominatim_www}/module
%dir %{nominatim_home}
%dir %{nominatim_data}
%dir %{nominatim_data}/tiger


%files data
%defattr(-,%{nominatim_user},%{nominatim_group})
%{nominatim_data}/*.sql*
%{nominatim_base}/*.sql*
%{nominatim_www}/*.sql*


%files libs
%{_libdir}/%{name}.so
%{nominatim_base}/module
%{nominatim_www}/module


%pre data
%{_bindir}/getent group %{nominatim_group} >/dev/null || \
    %{_sbindir}/groupadd \
        --force \
        --gid %{nominatim_uid} \
        --system \
        %{nominatim_group}

%{_bindir}/getent passwd %{nominatim_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{nominatim_uid} \
        --gid %{nominatim_group} \
        --comment "Nominatim User" \
        --shell /sbin/nologin \
        --home-dir %{nominatim_home} \
        --system \
        %{nominatim_user}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
