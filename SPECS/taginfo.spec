# Taginfo service user details.
%global taginfo_home %{_datadir}/taginfo
%global taginfo_logs %{_var}/log/taginfo
%global taginfo_var %{_sharedstatedir}/taginfo
%global taginfo_user taginfo
%global taginfo_group taginfo
%global taginfo_uid 744

# Prerequisite versions
%{!?abseil_cpp_version: %global abseil_cpp_version 20211102.0}
%{!?libosmium_min_version: %global libosmium_min_version 2.14.0}
%{!?ruby_max_version: %global ruby_max_version 2.8.0}
%{!?ruby_min_version: %global ruby_min_version 2.7.0}
%{!?sqlite_min_version: %global sqlite_min_version 3.36.0}

# Don't provide for any libraries from the Rails application bundle
# or for the abseil-cpp libraries needed for the tools.
%global __provides_exclude_from ^%{taginfo_home}/vendor/bundle/ruby/.*\\.so.*$

Name:           taginfo
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        OpenStreetMap Taginfo
License:        GPLv3
URL:            https://github.com/taginfo/taginfo

Source0:        https://github.com/taginfo/taginfo/archive/%{git_ref}/taginfo-%{git_ref}.tar.gz
Source1:        https://github.com/taginfo/taginfo-tools/archive/%{tools_git_ref}/taginfo-tools-%{tools_git_ref}.tar.gz
Source2:        https://github.com/abseil/abseil-cpp/archive/%{abseil_git_ref}/abseil-cpp-%{abseil_git_ref}.tar.gz
Source3:        https://taginfo.openstreetmap.org/download/taginfo-languages.db.bz2
Source4:        https://taginfo.openstreetmap.org/download/taginfo-projects.db.bz2
Source5:        https://taginfo.openstreetmap.org/download/taginfo-wiki.db.bz2
Source10:       maxar_logo.png
Source11:       nga_logo.png

Patch0:         taginfo-default-config.patch
Patch1:         taginfo-logging.patch
Patch2:         taginfo-use-bundler.patch
Patch3:         taginfo-sqlite-enable-loadextension.patch
Patch4:         taginfo-tools-tests-run-serial.patch

BuildRequires:  bzip2-devel
BuildRequires:  cmake3
BuildRequires:  curl
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  expat-devel
BuildRequires:  gd-devel
BuildRequires:  make
BuildRequires:  libicu-devel
BuildRequires:  libosmium-devel
BuildRequires:  protozero-devel
BuildRequires:  ruby
BuildRequires:  ruby-devel
BuildRequires:  rubygem-bundler
BuildRequires:  rubygem-rake
BuildRequires:  rubygem-test-unit
BuildRequires:  rubygems-devel
BuildRequires:  sqlite-devel
BuildRequires:  sqlite-pcre
BuildRequires:  zlib-devel

Requires:       bzip2
Requires:       curl
Requires:       ruby >= %{ruby_min_version}
Requires:       ruby < %{ruby_max_version}
Requires:       rubygem-bundler >= 2.1.0
Requires:       sqlite >= %{sqlite_min_version}
Requires:       sqlite-pcre
Requires:       which
# Require the separate tools package.
Requires:       %{name}-tools%{?_isa} = %{version}-%{release}

%description
Brings together information about OpenStreetMap tags and makes it
searchable and browsable.

%package data
Summary:	Taginfo data files
BuildArch:      noarch

%description data
This package contains Taginfo data files.

%package tools
Summary:	Taginfo tools
Provides:       bundled(abseil-cpp)

%description tools
These are some tools needed for creating statistics from a planet or
other OSM file.


%prep
%setup -q -n taginfo-%{git_ref}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1


%build
# taginfo
%{_bindir}/bundle config set --local path vendor/bundle
%{_bindir}/bundle install

# taginfo-tools
# Enable the updated compiler toolchain prior to building.
. /opt/rh/devtoolset-9/enable
%{__mkdir_p} taginfo-tools
%{__tar} -C taginfo-tools --strip-components 1 -xzf %{SOURCE1}
%{__tar} -C taginfo-tools/abseil-cpp --strip-components 1 -xzf %{SOURCE2}

pushd taginfo-tools
cat %{PATCH4} | patch -p1 -s
%{__mkdir_p} build
pushd build
%{cmake3} ..
%{cmake3_build}
popd
popd


%install
# Keep downloads in taginfo's home.
%{__rm} -f web/public/download
%{__ln_s} ../../download web/public/download
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}
%{__install} -d -m 0755 %{buildroot}%{_unitdir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -d -m 0755 %{buildroot}%{_libdir}
%{__install} -d -m 0755 %{buildroot}%{taginfo_home}
%{__install} -d -m 0750 %{buildroot}%{taginfo_logs}
%{__install} -d -m 0755 %{buildroot}%{taginfo_var}
%{__install} -d -m 0755 %{buildroot}%{taginfo_var}/{chronology,db,data,download,languages,master,projects,wiki}
%{__install} -m 0640 taginfo-config-example.json %{buildroot}%{_sysconfdir}/taginfo-config.json
%{__install} -m 0644 %{SOURCE3} %{SOURCE4} %{SOURCE5} %{buildroot}%{taginfo_var}/download
%{__ln_s} %{_sysconfdir}/taginfo-config.json %{buildroot}%{_datadir}/taginfo-config.json
%{__ln_s} %{taginfo_logs} %{buildroot}%{taginfo_var}/log
%{__ln_s} %{taginfo_var}/data %{buildroot}%{taginfo_home}/data
%{__ln_s} %{taginfo_var}/download %{buildroot}%{taginfo_home}/download

# Copy taginfo binaries and their absl shared libraries.
%{__install} -m 0755 taginfo-tools/build/src/taginfo-* %{buildroot}%{_bindir}
%{__install} -m 0755 taginfo-tools/build/src/osmstats %{buildroot}%{_bindir}
%{_bindir}/find taginfo-tools/build/abseil-cpp \
 -type f -name \*.so -exec %{__install} -m 0755 {} %{buildroot}%{_libdir} \;

# Copy most web application files.
%{__cp} \
 --preserve \
 --recursive \
 .bundle \
 bin \
 examples \
 extern \
 sources \
 vendor \
 web \
 Gemfile* \
 %{buildroot}%{taginfo_home}

# Add any additional sources.
%{__install} -m 0644 %{SOURCE10} %{buildroot}%{taginfo_home}/web/public/img/logo/maxar.png
%{__install} -m 0644 %{SOURCE11} %{buildroot}%{taginfo_home}/web/public/img/logo/nga.png

# Taginfo unit file for updating all data.
%{__cat} >> %{buildroot}%{_unitdir}/taginfo-update.service <<EOF
[Unit]
Description=Updates all Taginfo data
Documentation=%{url}
Requires=network-online.target
After=network.target

[Service]
Type=oneshot
User=%{taginfo_user}
Group=%{taginfo_group}
ExecStart=%{taginfo_home}/sources/update_all.sh %{taginfo_var}
ExecStartPost=%{_bindir}/mv -v %{taginfo_var}/selection.db %{taginfo_var}/taginfo-history.db %{taginfo_var}/taginfo-master.db %{taginfo_var}/db/taginfo-db.db %{taginfo_var}/languages/taginfo-languages.db %{taginfo_var}/projects/taginfo-projects.db %{taginfo_var}/wiki/taginfo-wiki.db %{taginfo_var}/data
WorkingDirectory=%{taginfo_home}

NoNewPrivileges=true
PrivateDevices=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=full
EOF


%check
pushd taginfo-tools/build
%{ctest3}
popd
pushd web
%{_bindir}/rake test
popd


%pre
# Create user and group for running the Taginfo application.
getent group %{taginfo_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{taginfo_uid} \
        --system \
        %{taginfo_group}

getent passwd %{taginfo_user} >/dev/null || \
    useradd \
        --uid %{taginfo_uid} \
        --gid %{taginfo_group} \
        --comment "Taginfo User" \
        --home-dir %{taginfo_home} \
        --shell /sbin/nologin \
        --system \
        %{taginfo_user}


%files
%doc README.md history.md
%license LICENSE
%{taginfo_home}/bin
%{taginfo_home}/data
%{taginfo_home}/download
%{taginfo_home}/examples
%{taginfo_home}/extern
%{taginfo_home}/sources
%{taginfo_home}/vendor
%{taginfo_home}/Gemfile*
%dir %{taginfo_home}/web
%{taginfo_home}/web/i18n
%{taginfo_home}/web/lib
%{taginfo_home}/web/public
%{taginfo_home}/web/test
%{taginfo_home}/web/*.rb
%{taginfo_home}/web/*.ini
%{taginfo_home}/web/views
%{taginfo_home}/web/viewsjs
%{_unitdir}/taginfo-update.service
%{_datadir}/taginfo-config.json
# Config files, readable by taginfo only.
%defattr(-, root, %{taginfo_group}, -)
%config(noreplace) %{_sysconfdir}/taginfo-config.json
# Bundle directory, config.ru, and data/log, directories should
# all be owned  by taginfo.
%defattr(-, %{taginfo_user}, %{taginfo_group}, -)
%{taginfo_home}/.bundle
%{taginfo_home}/web/config.ru
%dir %{taginfo_var}
%dir %{taginfo_logs}
%{taginfo_var}/log
%dir %{taginfo_var}/chronology
%dir %{taginfo_var}/db
%dir %{taginfo_var}/data
%dir %{taginfo_var}/download
%dir %{taginfo_var}/languages
%dir %{taginfo_var}/master
%dir %{taginfo_var}/projects
%dir %{taginfo_var}/wiki

%files data
%defattr(-, %{taginfo_user}, %{taginfo_group}, -)
%{taginfo_var}/download/*.bz2

%files tools
%doc taginfo-tools/README.md
%license taginfo-tools/LICENSE
%{_libdir}/*.so
%{_bindir}/osmstats
%{_bindir}/taginfo-*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
