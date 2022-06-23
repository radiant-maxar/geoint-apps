# The following macros are also required:
%global nodejs_min_version 10.0.0

%global __brp_mangle_shebangs /usr/bin/true

Name:           osrm-frontend
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Frontend for OSRM

License:        BSD
URL:            https://map.project-osrm.org
# The `git_ref` variable must be defined because the project doesn't use tags.
Source0:        https://github.com/Project-OSRM/osrm-frontend/archive/%{git_ref}/osrm-frontend-%{git_ref}.tar.gz

BuildArch:      noarch
BuildRequires:  nodejs-devel >= %{nodejs_min_version}

Requires: nodejs >= %{nodejs_min_version}
%if 0%{?rhel} >= 8
Requires: npm
%endif


%description
Frontend for OSRM, a routing engine for OpenStreetMap data.


%prep
%autosetup -n osrm-frontend-%{git_ref} -p 1


%build
npm install
npm run build


%install
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__cp} -rp \
   bundle.js \
   css \
   debug \
   favicon.ico \
   fonts \
   i18n \
   images \
   index.html \
   node_modules \
   package.json \
   package-lock.json \
   scripts \
   src \
   %{buildroot}%{_datadir}/%{name}
touch %{buildroot}%{_datadir}/%{name}/bundle.{js.map,raw.js}


%files
%doc README.md
%license LICENSE
%{_datadir}/%{name}/css/fonts.css
%{_datadir}/%{name}/css/site.css
%{_datadir}/%{name}/debug/arrows*
%{_datadir}/%{name}/debug/dist
%{_datadir}/%{name}/favicon.ico
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/i18n
%{_datadir}/%{name}/images
%{_datadir}/%{name}/index.html
%{_datadir}/%{name}/node_modules
%{_datadir}/%{name}/package.json
%{_datadir}/%{name}/package-lock.json
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/src/geocoder.js
%{_datadir}/%{name}/src/index.js
%{_datadir}/%{name}/src/itinerary_builder.js
%{_datadir}/%{name}/src/links.js
%{_datadir}/%{name}/src/localization.js
%{_datadir}/%{name}/src/lrm_options.js
%{_datadir}/%{name}/src/polyfill.js
%{_datadir}/%{name}/src/state.js
%{_datadir}/%{name}/src/tools.js
%{_datadir}/%{name}/src/libs
# These files need to owned by an unprivileged user, so it may recompile
# with new settings.
%defattr(-,nobody,nobody)
%{_datadir}/%{name}/bundle.js
%{_datadir}/%{name}/bundle.js.map
%{_datadir}/%{name}/bundle.raw.js
%{_datadir}/%{name}/css/leaflet.css
%{_datadir}/%{name}/debug/index.html
%{_datadir}/%{name}/src/leaflet_options.js


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
