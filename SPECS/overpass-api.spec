%global overpass_api_home %{_datadir}/%{name}
%global overpass_api_data %{_localstatedir}/lib/%{name}
%global overpass_api_group overpass-api
%global overpass_api_user overpass-api
%global overpass_api_uid 883

# Enable tests by default.
%bcond_without tests

Name:           overpass-api
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        A database engine to query the OpenStreetMap data

License:        Affero GPL v3
URL:            https://overpass-api.de/
Source0:        https://github.com/drolbr/Overpass-API/archive/%{git_ref}/Overpass-API-%{git_ref}.tar.gz

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  expat-devel
BuildRequires:  lz4-devel
BuildRequires:  make
BuildRequires:  zlib-devel

Patch0:         overpass-api-environment-settings.patch
Patch1:         overpass-api-test-basedir-fix.patch

# Replication scripts use wget to retrieve URLs.
Requires:       wget

%description
The Overpass API (formerly known as OSM Server Side Scripting, or
OSM3S before 2011) is a read-only API that serves up custom selected
parts of the OSM map data. It acts as a database over the web: the
client sends a query to the API and gets back the data set that
corresponds to the query.


%prep
%autosetup -p1 -n Overpass-API-%{git_ref}


%build
pushd src
autoscan
libtoolize
aclocal
autoheader
automake --add-missing
autoconf
%{__rm} -rf autom4te.cache
popd
pushd build
%{__sed} -i \
  -e 's|^AC_CONFIG_FILES\(\[Makefile test-bin/Makefile\]\)$|#AC_CONFIG_FILES([Makefile test-bin/Makefile])|' \
  -e 's|^#AC_CONFIG_FILES\(\[Makefile\]\)$|AC_CONFIG_FILES([Makefile])|' \
  ../src/configure.ac
%{__sed} -i \
  -e 's|^SUBDIRS = test-bin$|#SUBDIRS = test-bin|' \
  -e 's|^#SUBDIRS =$|SUBDIRS =|' \
  ../src/Makefile.am
%global _configure ../src/configure
%configure --enable-lz4 --prefix=%{overpass_api_home}
%make_build
popd


%install
pushd build
%make_install
popd
pushd src
%{__cp} -rp html rules %{buildroot}%{overpass_api_home}
%{__install} -d -m 0755 %{buildroot}%{overpass_api_data}/{db,diffs,replicate}
%{__ln_s} %{overpass_api_data}/{db,diffs,replicate} %{buildroot}%{overpass_api_home}
popd


%check
%if %{with tests}
pushd build
%{__sed} -i \
  -e 's|^#AC_CONFIG_FILES\(\[Makefile test-bin/Makefile\]\)$|AC_CONFIG_FILES([Makefile test-bin/Makefile])|' \
  -e 's|^AC_CONFIG_FILES\(\[Makefile\]\)$|#AC_CONFIG_FILES([Makefile])|' \
  ../src/configure.ac
%{__sed} -i \
  -e 's|^#SUBDIRS = test-bin$|SUBDIRS = test-bin|' \
  -e 's|^SUBDIRS =$|#SUBDIRS =|' \
  ../src/Makefile.am
%global _configure ../src/configure
%configure --enable-lz4 --prefix=%{overpass_api_home}_test
%make_build
%make_install
popd
pushd osm-3s_testing
%{buildroot}%{overpass_api_home}_test/test-bin/run_testsuite.sh 40 notimes >test.stdout.log 2>test.stderr.log
FAILED=$(grep FAILED test.stdout.log)
if [ -n "${FAILED}" ]; then
  cat test.stdout.log
  cat test.stderr.log
  exit 1
fi
echo "All tests successful."
popd
%endif


%files
%{overpass_api_home}
%defattr(-, %{overpass_api_user}, %{overpass_api_group}, -)
%{overpass_api_data}


%pre
getent group %{overpass_api_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{overpass_api_uid} \
        --system \
        %{overpass_api_group}

getent passwd %{overpass_api_user} >/dev/null || \
    useradd \
        --uid %{overpass_api_uid} \
        --gid %{overpass_api_group} \
        --comment "Overpass API User" \
        --shell /sbin/nologin \
        --home-dir %{overpass_api_home} \
        --system \
        %{overpass_api_user}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
