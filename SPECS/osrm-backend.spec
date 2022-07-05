# Force CMake to use `build` for its directory, tests assume it.
%global _vpath_builddir build

# Enable tests by default.
%bcond_without tests

Name:           osrm-backend
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        High performance routing engine for OpenStreetMap data

License:        BSD
URL:            https://map.project-osrm.org
Source0:        https://github.com/Project-OSRM/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  ccache
BuildRequires:  compat-lua-devel
BuildRequires:  cmake
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libosmium-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzip-devel
BuildRequires:  protozero-devel
%if %{with tests}
BuildRequires:  nodejs
%endif
BuildRequires:  tbb-devel

%description
High performance routing engine written in C++14 designed to run on OpenStreetMap data.


%package devel
Summary:   Development files for OSRM
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  boost-devel
Requires:  bzip2-devel
Requires:  expat-devel
Requires:  libxml2-devel
Requires:  libzip-devel
Requires:  lua-devel

%description devel
This package contains OSRM header files for development purposes.


%prep
%autosetup -p1
# Patch CMakeLists.txt:
#  * Use proper library path (/usr/lib64)
#  * Relax Lua requirement to 5.1
%{__sed} -i \
 -e 's/DESTINATION lib)$/DESTINATION lib\${LIB_SUFFIX})/' \
 -e 's/set(PKGCONFIG_LIBRARY_DIR "\${CMAKE_INSTALL_PREFIX}\/lib")/set(PKGCONFIG_LIBRARY_DIR "\${CMAKE_INSTALL_PREFIX}\/lib\${LIB_SUFFIX}")/' \
 -e 's/Lua 5\.2/Lua 5\.1/' \
 CMakeLists.txt


%build
%if %{with tests}
npm install
%{__rm} -f unit_tests/contractor/files.cpp
%{__rm} -f unit_tests/util/connectivity_checksum.cpp
%endif
%{cmake} \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DENABLE_ASSERTIONS:BOOL=Off \
 -DENABLE_CCACHE:BOOL=On \
 -DENABLE_LTO:BOOL=On \
 -DENABLE_NODE_BINDINGS:BOOL=On \
 -DLUA_INCLUDE_DIR:PATH=%{_includedir}/lua-5.1 \
 -DLUA_LIBRARY:FILEPATH=%{_libdir}/liblua-5.1.so
%{cmake_build}


%install
%{cmake_install}


%check
%if %{with tests}
npm run nodejs-tests

pushd example
%{__sed} -i \
 -e 's#include_directories(SYSTEM \${LibOSRM_INCLUDE_DIRS})#include_directories(SYSTEM \${LibOSRM_INCLUDE_DIRS} %{buildroot}%{_includedir} %{buildroot}%{_includedir}/osrm)#' \
 CMakeLists.txt
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
cmake \
 -B %{_vpath_builddir} \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DLibOSRM_INCLUDE_DIR:PATH=%{buildroot}%{_includedir} \
 -DLibOSRM_LIBRARY_DIRS:PATH=%{buildroot}%{_libdir}
%{__make} -C %{_vpath_builddir} %{?_smp_mflags}
popd
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:%{buildroot}%{_libdir}
example/%{_vpath_builddir}/osrm-example test/data/mld/monaco.osrm
%{cmake_build} --target tests
pushd %{_vpath_builddir}
for TEST_BIN in unit_tests/*-tests; do
  if [ "${TEST_BIN}" == "unit_tests/library-extract-tests" ] \
  || [ "${TEST_BIN}" == "unit_tests/updater-tests" ]; then
    echo "Skipping '${TEST_BIN}'."
    continue
  fi
  echo "Running '${TEST_BIN}':"
  ${TEST_BIN}
done
popd
%endif


%files
%{_bindir}/osrm-*
%{_libdir}/*.so
%{_datadir}/osrm/profiles
%doc README.md CHANGELOG.md
%license LICENSE.TXT


%files devel
%{_includedir}/flatbuffers
%{_includedir}/mapbox
%{_includedir}/osrm
%{_libdir}/pkgconfig/libosrm.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
