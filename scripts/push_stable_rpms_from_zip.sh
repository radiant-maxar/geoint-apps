#!/usr/bin/env bash
set -eu

RPMS_ZIP_FILE=${1:-"RPMS.zip"}
RPMS_ZIP_FILE_NAME=$(basename "${RPMS_ZIP_FILE}")

if [ ! -f "${RPMS_ZIP_FILE}" ]; then
  printf "ERROR: The zip file '%s' does not exist.\n" "${RPMS_ZIP_FILE}" 1>&2
  exit
fi

AWS_PROFILE=${AWS_PROFILE:-"geoint-apps"}
AWS_S3_BUCKET=${AWS_S3_BUCKET:-"geoint-apps"}
EL_VERSION=${EL_VERSION:-el7}

GIT_ROOT_DIR=$(git rev-parse --show-toplevel)
REPO_PREFIX="${EL_VERSION}/stable"

AWS_S3_REPO_URL="s3://${AWS_S3_BUCKET}/${REPO_PREFIX}"
COMPOSE_FILE="${GIT_ROOT_DIR}/docker-compose.${EL_VERSION}.yml"
EXTRACTED_RPMS_PATH="/tmp/${RPMS_ZIP_FILE_NAME}/RPMS"
LOCAL_REPO_PATH="/tmp/${RPMS_ZIP_FILE_NAME}/${REPO_PREFIX}"

AWS_SYNC_CMD="aws --profile=${AWS_PROFILE} s3 sync"
DOCKER_RUN_CMD="docker-compose run \
                --rm \
                --volume ${HOME}/.gnupg-geoint:/rpmbuild/.gnupg:rw \
                --volume ${EXTRACTED_RPMS_PATH}:/rpmbuild/EXTRACTED_RPMS:rw \
                --volume ${LOCAL_REPO_PATH}:/rpmbuild/${REPO_PREFIX}:rw \
                --volume ${GIT_ROOT_DIR}/scripts:/rpmbuild/scripts:ro \
                rpmbuild-generic"


# Ensure we are in the expected directory
cd ${GIT_ROOT_DIR}

# Ensure the .env file does not exist
rm .env

# Build the rpmbuild-generic image
make --file Makefile.${EL_VERSION} rpmbuild-generic

# Make sure extracted rpms & local repo directories are empty
rm -rf "${EXTRACTED_RPMS_PATH}" "${LOCAL_REPO_PATH}"

# Create extracted rpms & local repo directories
mkdir --parents "${EXTRACTED_RPMS_PATH}" "${LOCAL_REPO_PATH}"

# Extract RPMS_ZIP_FILE to EXTRACTED_RPMS_PATH
unzip "${RPMS_ZIP_FILE}" -d "${EXTRACTED_RPMS_PATH}"


# Export COMPOSE_FILE variable
export COMPOSE_FILE

# Sign the local RPMs
${DOCKER_RUN_CMD} \
  bash -c "ls -al EXTRACTED_RPMS; rpm --addsign EXTRACTED_RPMS/*/*.rpm"
# Copy the local RPMs into the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "cp -av EXTRACTED_RPMS/*/*.rpm ${REPO_PREFIX}"
# Update the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-update.sh ${REPO_PREFIX}"
# Sign the local repo copy
${DOCKER_RUN_CMD} \
  bash -c "./scripts/repo-sign.sh ${REPO_PREFIX}"

# Sync the local repo copy to the S3 repo (dry run)
${AWS_SYNC_CMD} --delete --dryrun \
  "${LOCAL_REPO_PATH}"/ "${AWS_S3_REPO_URL}"/

echo "-------------------------"
echo "Execute the following command if the dryrun output above appears correct:"
echo "${AWS_SYNC_CMD} --delete ${LOCAL_REPO_PATH}/ ${AWS_S3_REPO_URL}/"
