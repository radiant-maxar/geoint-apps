%global underpass_home %{_datadir}/%{name}
%global underpass_group underpass
%global underpass_user underpass
%global underpass_uid 888

Name:           underpass
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        API and utility programs to manipulate OpenStreetMap data

License:        GPLv3
URL:            https://github.com/hotosm/underpass
Source0:        https://github.com/hotosm/underpass/archive/%{git_ref}/underpass-%{git_ref}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  dejagnu
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gdal-devel
BuildRequires:  gettext-devel
BuildRequires:  gumbo-parser-devel
BuildRequires:  jemalloc-devel
BuildRequires:  libosmium-devel
BuildRequires:  libpqxx-devel
BuildRequires:  libxml++-devel
BuildRequires:  make
BuildRequires:  openmpi-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  range-v3-devel
BuildRequires:  swig
BuildRequires:  zlib-devel


%description
Underpass is a C++ API and utility programs for manipulating OpenStreetMap data
at the database and raw data file level. It can download replication files from
the OSM planet server and use these files to update a local copy of the OSM
database, or analyze the changes to generate statistics. It is designed to be
high performance on modest hardware.


%prep
%autosetup -N -n underpass-%{git_ref}
sed -i 's/ -lboost_python38//g' Makefile.am
./autogen.sh


%build
%configure --prefix=/usr
%make_build


%install
%make_install


%check
# %{__make} %{?_smp_mflags} check
# There are more tests
# https://github.com/hotosm/underpass/blob/03ef283e1b09fca1effd0c4a2f9d749eec33c8fd/.github/workflows/run_tests.yml#L27-L41
# testsuite/libunderpass.all/tm-test
# # testsuite/libunderpass.all/usersync-test
# testsuite/libunderpass.all/pq-test
# testsuite/libunderpass.all/osm2pgsql-test
# testsuite/libunderpass.all/change-test


%pre
# Create user and group for running the Underpass application.
getent group %{underpass_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{underpass_uid} \
        --system \
        %{underpass_group}

getent passwd %{underpass_user} >/dev/null || \
    useradd \
        --uid %{underpass_uid} \
        --gid %{underpass_group} \
        --comment "Underpass User" \
        --shell /sbin/nologin \
        --home-dir %{underpass_home} \
        --system \
        %{underpass_user}


%files
%doc README.md INSTALL
%license COPYING
/usr/bin/replicator
%{_datadir}/doc/%{name}
%{_libdir}/%{name}
%{_libdir}/libhotosm.a
%{_libdir}/libhotosm.la
%{_libdir}/libhotosm.so
%{_libdir}/libunderpass.a
%{_libdir}/libunderpass.la
%{_libdir}/libunderpass.so
%{underpass_home}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
