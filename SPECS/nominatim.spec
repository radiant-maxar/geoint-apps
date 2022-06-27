%global osm2pgsql_min_version 1.4.0

%{!?datrie_version: %global datrie_version 0.8.2}
%{!?python_dotenv_version: %global python_dotenv_version 0.20.0}
%{!?pyicu_version: %global pyicu_version 2.9}
%{!?pyyaml_version: %global pyyaml_version 6.0}

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
URL:            https://nominatim.org/

Source0:        https://github.com/openstreetmap/Nominatim/archive/v%{version}/Nominatim-%{version}.tar.gz
Source1:        https://www.nominatim.org/data/country_grid.sql.gz
Source2:        https://www.nominatim.org/data/gb_postcode_data.sql.gz
Source3:        https://www.nominatim.org/data/us_postcode_data.sql.gz
%if %{with tests}
Source4:        https://download.geofabrik.de/europe/monaco-latest.osm.pbf
%endif

Patch0:         nominatim-external-osm2pgsql.patch
Patch1:         nominatim-phpunit-resolve-deprecation-warnings.patch
Patch2:         nominatim-no-calculate-postcodes.patch
Patch3:         nominatim-legacy-tokenizer.patch
Patch4:         nominatim-tests-run-serial.patch

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  geos-devel
BuildRequires:  libicu-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  osm2pgsql >= %{osm2pgsql_min_version}
BuildRequires:  postgresql%{postgres_dotless}-devel
BuildRequires:  proj-devel
BuildRequires:  python3-devel
BuildRequires:  python3-osmium
BuildRequires:  python3-pip
BuildRequires:  python3-psycopg2
BuildRequires:  python36-jinja2
BuildRequires:  python36-psutil
BuildRequires:  zlib-devel

%if %{with tests}
BuildRequires:  libtidy
BuildRequires:  postgis
BuildRequires:  postgresql%{postgres_dotless}-contrib
BuildRequires:  postgresql%{postgres_dotless}-server
BuildRequires:  rh-php73-php-cli
BuildRequires:  rh-php73-php-intl
BuildRequires:  rh-php73-php-mbstring
BuildRequires:  rh-php73-php-pear
BuildRequires:  rh-php73-php-pgsql
# These PHP testing dependencies are installed manually.
#BuildRequires:  PHP_CodeSniffer
#BuildRequires:  PHPUnit
# These testing dependencies are installed by pip3 manually.
#BuildRequires:  python3-behave
#BuildRequires:  python3-pytidylib
# Source: https://github.com/osm-search/Nominatim/blob/master/docs/admin/Installation.md#software
#BuildRequires:  python3-dotenv # (required for build as well)
#BuildRequires:  python3-pyicu # (required for build as well)
#BuildRequires:  python3-pylint
#BuildRequires:  python3-pytest
#BuildRequires:  python3-pytest-cov
%endif

Requires:       %{name}-data = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       osm2pgsql >= %{osm2pgsql_min_version}
Requires:       postgresql%{postgres_dotless}
Requires:       python3-osmium
Requires:       python3-psycopg2
Requires:       python36-jinja2
Requires:       python36-psutil
Requires:       rh-php73-php-fpm
Requires:       rh-php73-php-intl
Requires:       rh-php73-php-pear
Requires:       rh-php73-php-pgsql
# These requirements are included in Nominatim's lib-python directory,
# They are not available in any yum repositories.
# Source: https://github.com/osm-search/Nominatim/blob/master/docs/admin/Installation.md#software
Provides:       bundled(python3-datrie) = %{datrie_version}
Provides:       bundled(python3-dotenv) = %{python_dotenv_version}
Provides:       bundled(python3-pyicu) = %{pyicu_version}
Provides:       bundled(python3-PyYAML) = %{pyyaml_version}


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
%autosetup -n Nominatim-%{version} -p1


%build
%if %{with tests}
# CMake needs to find the `pip3 --user` installed binaries
export PATH=${HOME}/.local/bin:${PATH}
%endif

%{__cp} -p %{SOURCE1} data/country_osm_grid.sql.gz
%{__cp} -p %{SOURCE2} %{SOURCE3} data

%{__mkdir_p} build
pushd build
scl enable rh-php73 '%{cmake3} \
        -DBUILD_API:BOOL=ON \
        -DBUILD_IMPORTER:BOOL=ON \
        -DBUILD_OSM2PGSQL:BOOL=OFF \
        -DCMAKE_INSTALL_LIBDIR=%{_datadir} \
        ..'
%{cmake3_build}
popd


%install
pushd build
%{cmake3_install}
popd

# Python dependencies that aren't available as system packages; first
# install packages with C extensions from *source* and then install
# source-only dependencies.
%{_bindir}/pip3 install --ignore-installed \
  --target %{buildroot}%{nominatim_base}/lib-python \
  --no-binary :all: \
  datrie==%{datrie_version} \
  PyYAML==%{pyyaml_version}
%{_bindir}/pip3 install --ignore-installed \
  --target %{buildroot}%{nominatim_base}/lib-python \
  python-dotenv==%{python_dotenv_version} \
  PyICU==%{pyicu_version}
export PYTHONPATH=%{buildroot}%{nominatim_base}/lib-python:%{python3_sitearch}:%{python3_sitelib}

# Database needs to exist to run `nominatim refresh`.
export PGDATA="${HOME}/pgdata"
pg_ctl stop --mode fast --silent || true
rm -fr "${PGDATA}"
pg_ctl init --options "--encoding UTF-8 --locale en_US.UTF-8" --silent
pg_ctl start --silent
createdb nominatim

# Website
%{__mkdir_p} %{buildroot}%{nominatim_www}

## Install 'website' .php files with `nominatim refresh`, database must be running.
%{__cp} %{buildroot}%{nominatim_conf}/env.defaults %{buildroot}%{nominatim_www}/.env
%{buildroot}%{_bindir}/nominatim refresh \
 --website \
 --project-dir %{buildroot}%{nominatim_www}

# Clean out buildroot from any paths in generated PHP.
%{__sed} -i -e "s|%{buildroot}||g" %{buildroot}%{nominatim_www}/website/*.php

# Tokenizer setup is done on import, make sure a default file exists.
%{__mkdir_p} %{buildroot}%{nominatim_www}/tokenizer
cat >> %{buildroot}%{nominatim_www}/tokenizer/tokenizer.php <<EOF
<?php
@define('CONST_Max_Word_Frequency', 50000);
@define('CONST_Term_Normalization_Rules', ":: NFD (); [[:Nonspacing Mark:] [:Cf:]] >;  :: lower (); [[:Punctuation:][:Space:]]+ > ' '; :: NFC ();");
require_once('%{nominatim_base}/lib-php/tokenizer/legacy_tokenizer.php');
EOF

# Clean up temporary environment, and add /etc link.
%{__rm} %{buildroot}%{nominatim_www}/.env
%{__ln_s} %{nominatim_conf}/env.defaults %{buildroot}%{nominatim_www}/.env

# Destroy database.
pg_ctl stop --mode fast --silent
rm -fr "${PGDATA}"

# Data
%{__mkdir_p} %{buildroot}%{nominatim_data}/tiger
%{__cp} -rp data/* %{buildroot}%{nominatim_data}/
%{__rm} %{buildroot}%{nominatim_base}/country_name.sql \
  %{buildroot}%{nominatim_base}/country_osm_grid.sql.gz \
  %{buildroot}%{nominatim_base}/words.sql
%{__ln_s} %{nominatim_data}/country_name.sql \
  %{nominatim_data}/country_osm_grid.sql.gz \
  %{nominatim_data}/gb_postcode_data.sql.gz \
  %{nominatim_data}/us_postcode_data.sql.gz \
  %{nominatim_data}/words.sql \
  %{buildroot}%{nominatim_base}/
%{__ln_s} %{nominatim_data}/country_name.sql \
  %{nominatim_data}/country_osm_grid.sql.gz \
  %{nominatim_data}/gb_postcode_data.sql.gz \
  %{nominatim_data}/us_postcode_data.sql.gz \
  %{nominatim_data}/words.sql \
  %{buildroot}%{nominatim_www}/

# Library
%{__mkdir_p} %{buildroot}%{_libdir} %{buildroot}%{nominatim_www}/module
%{__mv} %{buildroot}%{nominatim_base}/module/%{name}.so  %{buildroot}%{_libdir}
%{__ln_s} %{_libdir}/%{name}.so %{buildroot}%{nominatim_base}/module
%{__ln_s} %{_libdir}/%{name}.so %{buildroot}%{nominatim_www}/module


%check
%if %{with tests}
# Reinitialize PostgreSQL database.
export PGDATA="${HOME}/pgdata"
pg_ctl stop --mode fast --silent || true
rm -fr "${PGDATA}"
pg_ctl init --options "--encoding UTF-8 --locale en_US.UTF-8" --silent

# Tune the database.
cat >> "${PGDATA}/postgresql.conf" <<EOF
# Max speed, min data safety.
fsync = off
full_page_writes = off
synchronous_commit = off
# Memory tuning, high value for maintenance work mem to support index
# creation done by data import.
shared_buffers = 4GB
maintenance_work_mem = 12GB
work_mem = 50MB
# Minimal WAL, no archiving.
wal_level = minimal
archive_mode = off
max_wal_senders = 0
EOF

# Start PostgreSQL
pg_ctl start --silent
createuser -S www-data

# In rpmbuild environment have to explicitly set the PYTHONPATH to include the
# user's site packages.
export PYTHONPATH=${HOME}/.local/lib/python%{python3_version}/site-packages:%{python3_sitearch}:%{python3_sitelib}

# Modify tests to use rh-php73
%{__sed} -i -e "s|/usr/bin/env', 'php|/opt/rh/rh-php73/root/bin/php|g" \
  nominatim/tools/exec_utils.py \
  test/bdd/steps/steps_api_queries.py \
  test/python/test_tools_refresh_setup_website.py

# Bump maximum statements for pylint.
echo "max-statements=100" >> .pylintrc

# Disable newer pylint checkers
%{__sed} -i "s/disable=/disable=arguments-differ,arguments-renamed,consider-using-f-string,consider-using-generator,consider-using-with,unspecified-encoding,use-dict-literal,/g" .pylintrc

# The ICU tokenizer tests won't work with CentOS 7's older ICU version.
%{__rm} -f test/python/test_tokenizer_icu.py

# Invoke testing/linting runner
pushd build
scl enable rh-php73 '%{ctest3}'
popd

# Clean up.
pg_ctl stop --mode fast --silent
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


%pre
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
