# The following macros are also required:
# * gevent_version
# * gunicorn_version
# * numpy_version
# * pyproj_version
# * pyredis_version
# * pyyaml_version
# * shapely_version

%global mapproxy_cache %{_var}/cache/mapproxy
%global mapproxy_config %{_sysconfdir}/mapproxy
%global mapproxy_home %{_sharedstatedir}/mapproxy
%global mapproxy_logs %{_var}/log/mapproxy
%global mapproxy_root %{_datadir}/mapproxy
%global mapproxy_run /run/mapproxy
%global mapproxy_user mapproxy
%global mapproxy_group %{mapproxy_user}
%global mapproxy_uid 753
%global mapproxy_gid %{mapproxy_uid}


%global __provides_exclude_from ^%{mapproxy_root}/venv/.*$
%global __requires_exclude_from ^%{mapproxy_root}/venv/bin/.*$


Name:           mapproxy
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        MapProxy is a tile cache and WMS proxy
License:        ASL 2.0
URL:            https://mapproxy.org/
Source0:        https://github.com/mapproxy/mapproxy/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Patch0:         mapproxy-tests-el9.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gdal-devel
BuildRequires:  geos-devel
BuildRequires:  lapack-devel
BuildRequires:  libffi-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  proj-devel
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  python3-pillow
BuildRequires:  python3-wheel
BuildRequires:  systemd-rpm-macros

Requires:       python3-gdal
Requires:       python3-lxml
Requires:       python3-pillow

Provides:       bundled(python3-gevent) = %{gevent_version}
Provides:       bundled(python3-gunicorn) = %{gunicorn_version}
Provides:       bundled(python3-numpy) = %{numpy_version}
Provides:       bundled(python3-pyproj) = %{pyproj_version}
Provides:       bundled(python3-PyYAML) = %{pyyaml_version}
Provides:       bundled(python3-redis) = %{pyredis_version}
Provides:       bundled(python3-shapely) = %{shapely_version}


%description
MapProxy is an open source proxy for geospatial data. It caches, accelerates and transforms data from existing map services and serves any desktop or web GIS client.


%prep
%autosetup -p1


%build
# Create virtualenv and upgrade its pip/setuptools/wheel to latest versions.
python3 -m venv --system-site-packages venv
./venv/bin/pip3 install pip setuptools wheel --upgrade

# Install additional dependencies with `--no-binary` so they're linked with appropriate
# library versions and compiled with hardening flags on our EL platform.
./venv/bin/pip3 install \
  gevent==%{gevent_version} \
  gunicorn==%{gunicorn_version} \
  numpy==%{numpy_version} \
  https://github.com/radiant-maxar/pyproj/archive/%{pyproj_version}.zip \
  PyYAML==%{pyyaml_version} \
  redis==%{pyredis_version} \
  shapely==%{shapely_version} \
  -v --no-binary :all:

# Report RPM version.
%{__sed} -i -e 's/unknown_version/%{version}-%{rpmbuild_release}/g' mapproxy/version.py


%install
%{__install} -d -m 0755 \
 %{buildroot}%{_sysconfdir}/sysconfig \
 %{buildroot}%{_unitdir} \
 %{buildroot}%{_usr}/lib/tmpfiles.d \
 %{buildroot}%{mapproxy_root}
%{__install} -d -m 0750 \
 %{buildroot}%{mapproxy_cache} \
 %{buildroot}%{mapproxy_config} \
 %{buildroot}%{mapproxy_home} \
 %{buildroot}%{mapproxy_logs} \
 %{buildroot}%{mapproxy_run}

# mapproxy tmpfiles.d entry
echo "d %{mapproxy_run} 0750 %{mapproxy_user} %{mapproxy_group} -" > \
       %{buildroot}%{_usr}/lib/tmpfiles.d/%{name}.conf

# Create an empty default config file.
touch %{buildroot}%{mapproxy_config}/%{name}.yaml

# Create environment file.
%{__cat} <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/%{name}
MAPPROXY_CONFIG_FILE=%{mapproxy_config}/%{name}.yaml
MAPPROXY_HOST=0.0.0.0
MAPPROXY_PORT=8080
MAPPROXY_WORKERS=3
MAPPROXY_TIMEOUT=179
EOF
chmod 0640 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Copy module and virtual environment.
for dir in mapproxy venv; do
    %{__cp} -rp ${dir} %{buildroot}%{mapproxy_root}/${dir}
done

# Ensure VIRTUAL_ENV points to the installed location in activation scripts.
%{__sed} -i -e 's|^VIRTUAL_ENV=.*|VIRTUAL_ENV="%{mapproxy_root}/venv"|g' \
  %{buildroot}%{mapproxy_root}/venv/bin/activate
%{__sed} -i -e 's|VIRTUAL_ENV ".*"|VIRTUAL_ENV="%{mapproxy_root}/venv"|g' \
  %{buildroot}%{mapproxy_root}/venv/bin/activate.{csh,fish}

# Correct shebang path for files in virtualenv directory.
%{__sed} -i \
  -e '1s|#!/usr/bin/env python|#!%{mapproxy_root}/venv/bin/python3|' \
  -e '1s|#!/.*/venv/bin/python3|#!%{mapproxy_root}/venv/bin/python3|' \
  %{buildroot}%{mapproxy_root}/venv/bin/f2py* \
  %{buildroot}%{mapproxy_root}/venv/bin/gunicorn* \
  %{buildroot}%{mapproxy_root}/venv/bin/pip* \
  %{buildroot}%{mapproxy_root}/venv/bin/pyproj* \
  %{buildroot}%{mapproxy_root}/venv/bin/wheel*

# Link mapproxy module into the virtual environment site modules.
%{__ln_s} %{mapproxy_root}/mapproxy \
 %{buildroot}%{mapproxy_root}/venv/lib/python%{__default_python3_version}/site-packages

# mapproxy-seed
%{__cat} <<EOF > %{buildroot}%{mapproxy_root}/venv/bin/mapproxy-seed
#!%{mapproxy_root}/venv/bin/python3
import re
import sys
from mapproxy.seed.script import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?\$', '', sys.argv[0])
    sys.exit(main())
EOF
chmod 0755 %{buildroot}%{mapproxy_root}/venv/bin/mapproxy-seed

# mapproxy-util
%{__cat} <<EOF > %{buildroot}%{mapproxy_root}/venv/bin/mapproxy-util
#!%{mapproxy_root}/venv/bin/python3
import re
import sys
from mapproxy.script.util import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?\$', '', sys.argv[0])
    sys.exit(main())
EOF
chmod 0755 %{buildroot}%{mapproxy_root}/venv/bin/mapproxy-util

# Create WSGI module that'll get the configuration file from the environment.
%{__cat} <<EOF > %{buildroot}%{mapproxy_root}/wsgi.py
import os
from mapproxy.wsgiapp import make_wsgi_app

application = make_wsgi_app(os.environ.get("MAPPROXY_CONFIG_FILE"))
EOF

%{__cat} <<EOF > %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=%{summary}
Documentation=%{url}
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=simple
User=%{mapproxy_user}
Group=%{mapproxy_group}
ExecStart=%{mapproxy_root}/venv/bin/gunicorn \\
  --bind \${MAPPROXY_HOST}:\${MAPPROXY_PORT} \\
  --worker-class gevent \\
  --workers \${MAPPROXY_WORKERS} \\
  --timeout \${MAPPROXY_TIMEOUT} \\
  --access-logfile - \\
  wsgi
EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}
WorkingDirectory=%{mapproxy_root}

NoNewPrivileges=true
PrivateDevices=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=full

[Install]
WantedBy=multi-user.target
EOF


%check
./venv/bin/pip3 install -r requirements-tests.txt
./venv/bin/pytest -v mapproxy


%pre
%{_bindir}/getent group %{mapproxy_group} >/dev/null || \
    %{_sbindir}/groupadd \
        --force \
        --gid %{mapproxy_gid} \
        --system \
        %{mapproxy_group}

%{_bindir}/getent passwd %{mapproxy_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{mapproxy_uid} \
        --gid %{mapproxy_group} \
        --comment "MapProxy user" \
        --shell %{_sbindir}/nologin \
        --home-dir %{mapproxy_home} \
        --no-create-home \
        --system \
        %{mapproxy_user}


%post
if test -f /.dockerenv; then exit 0; fi
%systemd_post %{name}.service


%preun
if test -f /.dockerenv; then exit 0; fi
%systemd_preun %{name}.service


%postun
if test -f /.dockerenv; then exit 0; fi
%systemd_postun %{name}.service


%files
%doc AUTHORS.txt CHANGES.txt README.rst
%license COPYING.txt LICENSE.txt
%{mapproxy_root}
%{_unitdir}/%{name}.service
%{_usr}/lib/tmpfiles.d/%{name}.conf
%defattr(-, root, %{mapproxy_group}, -)
%dir %{mapproxy_config}
%config(noreplace) %{mapproxy_config}/%{name}.yaml
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%defattr(-, %{mapproxy_user}, %{mapproxy_group}, -)
%dir %{mapproxy_cache}
%dir %{mapproxy_logs}
%dir %{mapproxy_home}
%dir %{mapproxy_run}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
