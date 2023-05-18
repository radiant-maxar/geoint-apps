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

Requires:       python3-gdal

Provides:       bundled(python3-cffi)
Provides:       bundled(python3-gevent)
Provides:       bundled(python3-gunicorn)
Provides:       bundled(python3-lxml)
Provides:       bundled(python3-numpy)
Provides:       bundled(python3-psycopg2)
Provides:       bundled(python3-pyproj)
Provides:       bundled(python3-PyYAML)
Provides:       bundled(python3-shapely)

%description
GeoNode is a web-based application and platform for developing geospatial information systems (GIS) and for deploying spatial data infrastructures (SDI).


%prep
%autosetup


%build
%{_bindir}/python3 -m venv venv
./venv/bin/python3 -m pip install pip --upgrade
./venv/bin/python3 -m pip install setuptools wheel --upgrade
./venv/bin/python3 -m pip install \
--no-binary cffi,gevent,gunicorn,lxml,numpy,psycopg2,pyproj,Pillow,PyYAML,Shapely,uWSGI \
-v -r requirements.txt


%files
%doc AUTHORS README.md SECURITY.md
%license license.txt


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
