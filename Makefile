## Conditional variables.
DOCKER ?= docker
DOCKER_COMPOSE ?= docker-compose
CI ?= false
COMPOSE_FILE ?= docker-compose.yml
COMPOSE_PROJECT_NAME ?= geoint-apps-$(RPMBUILD_CHANNEL)
IMAGE_PREFIX ?= $(COMPOSE_PROJECT_NAME)_

## Macro functions.

build_unless_image_exists = $(shell $(DOCKER) image inspect $(IMAGE_PREFIX)$(1) >/dev/null 2>&1 || DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) build $(1))
pull_if_ci = $(shell bash -c '[ "$(CI)" == "false" ] || $(DOCKER_COMPOSE) pull --quiet $(1)')

# The `rpmbuild_util.py` utility script is used to pull out configured versions,
# Docker build images, and other build variables.
rpmbuild_util = $(shell ./scripts/rpmbuild_util.py $(1) --config-file $(COMPOSE_FILE) $(2))
config_release = $(call rpmbuild_util,$(1),--release)
config_version = $(call rpmbuild_util,$(1),--version)

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call rpmbuild_util,dist,--variable)
rpm_file = $(call rpmbuild_util,$(1),--filename)

# Gets the RPM package name from the filename.
rpm_package = $(shell ./scripts/rpm_package.py $(1))
rpmbuild_image = $(call rpmbuild_util,$(call rpm_package,$(1)),--image)
rpmbuild_image_parent = $(call rpmbuild_util,$(call rpmbuild_image,$(1)).build.args.rpmbuild_image,--variable --config-key services)
rpmbuild_release = $(call config_release,$(call rpm_package,$(1)))
rpmbuild_version = $(call config_version,$(call rpm_package,$(1)))

## Variables
DOCKER_VERSION := $(shell $(DOCKER) --version 2>/dev/null)
DOCKER_COMPOSE_VERSION := $(shell $(DOCKER_COMPOSE) --version 2>/dev/null)
POSTGRES_VERSION := $(shell echo $(call rpmbuild_util,postgres_version,--variable) | tr -d '.')
RPMBUILD_CHANNEL := $(call rpmbuild_util,channel_name,--variable)
RPMBUILD_UID := $(shell id -u)
RPMBUILD_GID := $(shell id -g)

# RPM files at desired versions.
MOD_TILE_RPM := $(call rpm_file,mod_tile)
NOMINATIM_RPM := $(call rpm_file,nominatim)
NOMINATIM_UI_RPM := $(call rpm_file,nominatim-ui)
OSRM_BACKEND_RPM := $(call rpm_file,osrm-backend)
OSRM_FRONTEND_RPM := $(call rpm_file,osrm-frontend)
OVERPASS_API_RPM := $(call rpm_file,overpass-api)
TAGINFO_RPM := $(call rpm_file,taginfo)


# Build images and RPMs.
RPMBUILD_BASE_IMAGES := \
	rpmbuild \
	rpmbuild-generic \
	rpmbuild-generic-nodejs
RPMBUILD_RPMS := \
	mod_tile \
	nominatim \
	nominatim-ui \
	osrm-backend \
	osrm-frontend \
	overpass-api \
	taginfo

## General targets

.PHONY: \
	all \
	distclean \
	$(RPMBUILD_BASE_IMAGES) \
	$(RPMBUILD_RPMS)

all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif
ifndef DOCKER_COMPOSE_VERSION
    $(error "command docker-compose is not available, please install Docker")
endif

distclean: .env
	$(DOCKER_COMPOSE) down --volumes --rmi all
	rm -fr .env RPMS/noarch RPMS/x86_64 SOURCES/*.asc SOURCES/*.sha256 SOURCES/*.tgz SOURCES/*.tar.gz SOURCES/*.tar.xz SOURCES/*.zip

# Environment file for docker-compose; required packages for build containers
# are provided here.
.env: SPECS/*.spec
	echo COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) > .env
	echo IMAGE_PREFIX=$(IMAGE_PREFIX) >> .env
	echo RPMBUILD_GID=$(RPMBUILD_GID) >> .env
	echo RPMBUILD_UID=$(RPMBUILD_UID) >> .env
	echo RPMBUILD_MOD_TILE_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/mod_tile.spec) >> .env
	echo RPMBUILD_NOMINATIM_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/nominatim.spec --define postgres_version=$(POSTGRES_VERSION)) >> .env
	echo RPMBUILD_NOMINATIM_UI_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/nominatim-ui.spec) >> .env
	echo RPMBUILD_OSRM_BACKEND_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osrm-backend.spec) >> .env
	echo RPMBUILD_OSRM_FRONTEND_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/osrm-frontend.spec) >> .env
	echo RPMBUILD_OVERPASS_API_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/overpass-api.spec) >> .env
	echo RPMBUILD_TAGINFO_PACKAGES=$(shell ./scripts/buildrequires.py SPECS/taginfo.spec) >> .env

## Image targets
rpmbuild: .env
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)

rpmbuild-generic: rpmbuild
	$(call pull_if_ci,$?)
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)

rpmbuild-generic-nodejs: rpmbuild-generic
	$(call pull_if_ci,$?)
	$(call pull_if_ci,$@)
	$(call build_unless_image_exists,$@)


## RPM targets
mod_tile: $(MOD_TILE_RPM)
nominatim: $(NOMINATIM_RPM)
nominatim-ui: $(NOMINATIM_UI_RPM)
osrm-backend: $(OSRM_BACKEND_RPM)
osrm-frontend: $(OSRM_FRONTEND_RPM)
overpass-api: $(OVERPASS_API_RPM)
taginfo: $(TAGINFO_RPM)


## Build patterns
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm: .env
	$(call pull_if_ci,$(call rpmbuild_image_parent,$*))
	$(call build_unless_image_exists,$(call rpmbuild_image_parent,$*))
	$(call pull_if_ci,$(call rpmbuild_image,$*))
	$(call build_unless_image_exists,$(call rpmbuild_image,$*))
	$(DOCKER_COMPOSE) run --rm -T $(call rpmbuild_image,$*) \
		$(shell ./scripts/rpmbuild_util.py $(call rpm_package,$*) --config-file $(COMPOSE_FILE))
