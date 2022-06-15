# The following macros are also required:
%global libosmium_min_version 2.16.0
%global nodejs_min_version 10.0.0
%global protozero_min_version 1.3.0

# Enable tests by default.
%bcond_without tests

Name:           osrm-backend
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        High performance routing engine for OpenStreetMap data

License:        BSD
URL:            https://map.project-osrm.org
Source0:        https://github.com/Project-OSRM/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# A newer C++ toolchain is required to compile.
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  boost169-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  libxml2-devel
BuildRequires:  libzip-devel
BuildRequires:  lua-devel
BuildRequires:  protozero-devel >= %{protozero_min_version}
%if %{with tests}
BuildRequires:  nodejs >= %{nodejs_min_version}
%endif
BuildRequires:  tbb-devel

%description
High performance routing engine written in C++14 designed to run on OpenStreetMap data.


%package devel
Summary:   Development files for OSRM
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  boost169-devel
Requires:  bzip2-devel
Requires:  expat-devel
Requires:  libxml2-devel
Requires:  libzip-devel
Requires:  lua-devel

%description devel
This package contains OSRM header files for development purposes.


%prep
%autosetup -p1
%{__mkdir_p} build
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
export ENABLE_NODE_BINDINGS=On
%endif
pushd build
scl enable devtoolset-9 '%{cmake3} \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost169 \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost169 \
        -DCMAKE_BUILD_TYPE=Release \
        -DENABLE_ASSERTIONS=Off \
        -DENABLE_LTO=On \
        -DENABLE_NODE_BINDINGS=${ENABLE_NODE_BINDINGS:-Off} \
        -DOSMIUM_INCLUDE_DIR=%{_includedir} \
        -DPROTOZERO_INCLUDE_DIR=%{_includedir} \
        ..; %{cmake3_build}'
popd


%install
pushd build
%{cmake3_install}
# libosrm_guidance.so is not installed by default, do it manually.
%{__install} -p libosrm_guidance.so %{buildroot}%{_libdir}
popd


%check
%if %{with tests}
npm run nodejs-tests
%{__mkdir_p} example/build
pushd example/build
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:%{buildroot}%{_libdir}
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
%{__sed} -i \
 -e 's#include_directories(SYSTEM \${LibOSRM_INCLUDE_DIRS})#include_directories(SYSTEM \${LibOSRM_INCLUDE_DIRS} %{buildroot}%{_includedir} %{buildroot}%{_includedir}/osrm)#' \
 ../CMakeLists.txt
scl enable devtoolset-9 '%{cmake3} \
        -DCMAKE_BUILD_TYPE=Release \
        -DLibOSRM_INCLUDE_DIR=%{buildroot}%{_includedir} \
        -DLibOSRM_LIBRARY_DIRS=%{buildroot}%{_libdir} \
        ..; %{cmake3_build}'
popd
example/build/osrm-example test/data/mld/monaco.osrm
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
