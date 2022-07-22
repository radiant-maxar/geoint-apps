# The following macros are also required:
%global nodejs_min_version 14.0.0

# Variables for Nominatim UI paths
%global nominatim_ui_base %{_datadir}/%{name}
%global nominatim_ui_conf %{_sysconfdir}/%{name}
%global nominatim_ui_www %{_var}/www/%{name}

%bcond_without tests

Name:           nominatim-ui
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Debug web interface for Nominatim
License:        GPLv2
URL:            https://github.com/osm-search/nominatim-ui
Source0:        https://github.com/osm-search/nominatim-ui/archive/v%{version}/nominatim-ui-%{version}.tar.gz
Patch0:         nominatim-ui-test-browser-no-sandbox.patch
Patch1:         nominatim-ui-test-vaduz-name-keyword.patch

BuildArch:      noarch

BuildRequires:  nodejs >= %{nodejs_min_version}
BuildRequires:  yarn

%if %{with tests}
BuildRequires:  chromium
%endif

%description
%{summary}.


%prep
%autosetup -p1


%build
yarn install
yarn build


%install
%{__install} -d %{buildroot}%{_var}/www \
  %{buildroot}%{nominatim_ui_base} \
  %{buildroot}%{nominatim_ui_conf}
%{__cp} -rp dist/* %{buildroot}%{nominatim_ui_base}
%{__ln_s} %{nominatim_ui_base} %{buildroot}%{nominatim_ui_www}
%{__mv} %{buildroot}%{nominatim_ui_base}/config.defaults.js %{buildroot}%{nominatim_ui_conf}/
%{__ln_s} %{nominatim_ui_conf}/config.defaults.js %{buildroot}%{nominatim_ui_base}/


%check
yarn lint
%if %{with tests}
yarn test
%endif


%files
%doc CHANGES.md CONTRIBUTE.md README.md screenshot.png
%license LICENSE
%config(noreplace) %{nominatim_ui_conf}/config.defaults.js
%{nominatim_ui_www}
%{nominatim_ui_base}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
