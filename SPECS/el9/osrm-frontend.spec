%global osrm_frontend_home %{_datadir}/osrm-frontend
%global osrm_frontend_uid 551
%global osrm_frontend_user osrm-frontend

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
BuildRequires:  nodejs-devel

Requires:       nodejs


%description
Frontend for OSRM, a routing engine for OpenStreetMap data.


%prep
%autosetup -p1 -n osrm-frontend-%{git_ref}


%build
npm install
npm run build


%install
%{__install} -d %{buildroot}%{osrm_frontend_home}
%{__install} -d -m 0750 %{buildroot}%{osrm_frontend_home}/.npm
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
   %{buildroot}%{osrm_frontend_home}
touch %{buildroot}%{osrm_frontend_home}/bundle.{js.map,raw.js}


%files
%doc README.md
%license LICENSE
%{osrm_frontend_home}/css/fonts.css
%{osrm_frontend_home}/css/site.css
%{osrm_frontend_home}/debug/arrows*
%{osrm_frontend_home}/debug/dist
%{osrm_frontend_home}/favicon.ico
%{osrm_frontend_home}/fonts
%{osrm_frontend_home}/i18n
%{osrm_frontend_home}/images
%{osrm_frontend_home}/index.html
%{osrm_frontend_home}/node_modules
%{osrm_frontend_home}/package.json
%{osrm_frontend_home}/package-lock.json
%{osrm_frontend_home}/scripts
%{osrm_frontend_home}/src/geocoder.js
%{osrm_frontend_home}/src/index.js
%{osrm_frontend_home}/src/itinerary_builder.js
%{osrm_frontend_home}/src/links.js
%{osrm_frontend_home}/src/localization.js
%{osrm_frontend_home}/src/lrm_options.js
%{osrm_frontend_home}/src/polyfill.js
%{osrm_frontend_home}/src/state.js
%{osrm_frontend_home}/src/tools.js
%{osrm_frontend_home}/src/libs
# These files need to owned by osrm-frontend, so it may recompile with new settings.
%defattr(-,%{osrm_frontend_user},%{osrm_frontend_user})
%dir %{osrm_frontend_home}/.npm
%{osrm_frontend_home}/bundle.js
%{osrm_frontend_home}/bundle.js.map
%{osrm_frontend_home}/bundle.raw.js
%{osrm_frontend_home}/css/leaflet.css
%{osrm_frontend_home}/debug/index.html
%{osrm_frontend_home}/src/leaflet_options.js


%pre
%{_bindir}/getent group %{osrm_frontend_user} >/dev/null || \
    %{_sbindir}/groupadd \
        --force \
        --gid %{osrm_frontend_uid} \
        --system \
        %{osrm_frontend_user}

%{_bindir}/getent passwd %{osrm_frontend_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{osrm_frontend_uid} \
        --gid %{osrm_frontend_user} \
        --comment "OSRM Frontend User" \
        --shell /sbin/nologin \
        --home-dir %{osrm_frontend_home} \
        --system \
        %{osrm_frontend_user}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
