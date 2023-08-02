%{!?catch2_version: %global catch2_version 2.13.9}

# renderd service user details.
%global renderd_home %{_sharedstatedir}/mod_tile
%global renderd_user renderd
%global renderd_group renderd
%global renderd_uid 740


Name:          mod_tile
Version:       %{rpmbuild_version}
Release:       %{rpmbuild_release}%{?dist}
Summary:       A program to efficiently render and serve map tiles for www.openstreetmap.org map using Apache and Mapnik

License:       GPLv2
URL:           https://github.com/openstreetmap/mod_tile
Source0:       https://github.com/openstreetmap/mod_tile/archive/%{rpmbuild_version}/%{name}-%{rpmbuild_version}.tar.gz
Source1:       https://github.com/catchorg/Catch2/releases/download/v%{catch2_version}/catch.hpp
Patch0:        mod_tile-20230720.patch

Requires:      httpd >= 2.4.6
Requires:      iniparser

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: glib2-devel
BuildRequires: httpd-devel
BuildRequires: iniparser-devel
BuildRequires: libcurl-devel
BuildRequires: libmemcached-devel
BuildRequires: mapnik-devel


%description
%{summary}.


%prep
%autosetup -p1
%{__mv} %{SOURCE1} includes/catch.hpp


%build
%{cmake} \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DENABLE_TESTS:BOOL=On
%{cmake_build}


%install
%{cmake_install}
%{__install} -d -m 0755 \
  %{buildroot}%{_usr}/lib/sysusers.d \
  %{buildroot}%{_usr}/lib/tmpfiles.d \
  %{buildroot}%{renderd_home}
%{__install} -d -m 0750 \
  %{buildroot}%{_rundir}/renderd

# sysusers.d configuration file for renderd.
%{__cat} > %{buildroot}%{_usr}/lib/sysusers.d/renderd.conf << EOF
g %{renderd_group} %{renderd_uid}
u %{renderd_user} %{renderd_uid}:%{renderd_uid} 'Tile Rendering User' %{renderd_home} -
EOF

# tmpfiles.d configuration file for renderd.
%{__cat} > %{buildroot}%{_usr}/lib/tmpfiles.d/renderd.conf << EOF
d %{_rundir}/renderd 0750 %{renderd_user} apache -
d %{renderd_home} 0755 %{renderd_user} apache -
EOF

# Example configuration file for mod_tile.
%{__cat} > mod_tile-example.conf << EOF
<VirtualHost *:80>
  ServerName localhost
  DocumentRoot /var/www/html

  LogLevel warn

  LoadTileConfigFile %{_sysconfdir}/renderd.conf

  ModTileRenderdSocketName %{_rundir}/renderd/renderd.sock

  ModTileEnableStats On
  ModTileBulkMode Off
  ModTileRequestTimeout 3
  ModTileMissingRequestTimeout 10
  ModTileMaxLoadOld 16
  ModTileMaxLoadMissing 50
  ModTileVeryOldThreshold 31536000000000

  ModTileCacheDurationMax 604800
  ModTileCacheDurationDirty 900
  ModTileCacheDurationMinimum 10800
  ModTileCacheDurationMediumZoom 13 86400
  ModTileCacheDurationLowZoom 9 518400
  ModTileCacheLastModifiedFactor 0.20
  ModTileEnableTileThrottling Off
  ModTileEnableTileThrottlingXForward 0
  ModTileThrottlingTiles 10000 1
  ModTileThrottlingRenders 128 0.2
</VirtualHost>
EOF


%check
%{ctest}


%pre
getent group %{renderd_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{renderd_uid} \
        --system \
        %{renderd_group}

getent passwd %{renderd_user} >/dev/null || \
    useradd \
        --uid %{renderd_uid} \
        --gid %{renderd_group} \
        --comment "Tile Rendering User" \
        --shell /sbin/nologin \
        --home-dir %{renderd_home} \
        --system \
        %{renderd_user}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc mod_tile-example.conf AUTHORS README.rst screenshot.jpg docs
%license COPYING
%{_sysconfdir}/httpd/conf.modules.d/11-tile.conf
%config(noreplace) %{_sysconfdir}/renderd.conf
%{_bindir}/render*
%{_libdir}/httpd/modules/mod_tile.so
%{_mandir}/man1/render*
%{_usr}/lib/sysusers.d/renderd.conf
%{_usr}/lib/tmpfiles.d/renderd.conf
%defattr(-, %{renderd_user}, apache, -)
%{renderd_home}
%defattr(-, %{renderd_user}, %{renderd_group}, -)
%{_rundir}/renderd


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
