#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
require_env AZURE_CLIENT_ID AZURE_SUBSCRIPTION_ID ACR_NAME ACR_LOGIN_SERVER ACR_REPOSITORY LOCAL_IMAGE IMAGE_TAG
require_tools az docker mktemp
[[ "$ACR_NAME" =~ ^[a-zA-Z0-9]{5,50}$ ]] || exit 2
[[ "$ACR_LOGIN_SERVER" =~ ^[a-z0-9.-]+\.azurecr\.io$ ]] || exit 2
valid_tag "$IMAGE_TAG"
valid_repository "$ACR_REPOSITORY"
TASK_TMP=$(mktemp -d)
trap 'rm -rf -- "$TASK_TMP"' EXIT
export DOCKER_CONFIG="$TASK_TMP/docker"
export AZURE_CONFIG_DIR="$TASK_TMP/azure"
mkdir -p "$DOCKER_CONFIG" "$AZURE_CONFIG_DIR"
# User-assigned managed identity attached to this trusted Azure VM agent.
az login --identity --client-id "$AZURE_CLIENT_ID" --output none --only-show-errors
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
ACTUAL_SERVER=$(az acr show --name "$ACR_NAME" --query loginServer --output tsv)
[[ "$ACTUAL_SERVER" == "$ACR_LOGIN_SERVER" ]] || exit 3
az acr login --name "$ACR_NAME" --only-show-errors
REMOTE_IMAGE="$ACR_LOGIN_SERVER/$ACR_REPOSITORY:$IMAGE_TAG"
docker tag "$LOCAL_IMAGE" "$REMOTE_IMAGE"
docker push "$REMOTE_IMAGE"
DIGEST=$(az acr repository show --name "$ACR_NAME" \
  --image "$ACR_REPOSITORY:$IMAGE_TAG" --query digest --output tsv)
[[ "$DIGEST" =~ ^sha256:[a-f0-9]{64}$ ]] || exit 3
# Enforce unique, non-overwritable release tags through registry/release policy.
printf '%s@%s\n' "$ACR_LOGIN_SERVER/$ACR_REPOSITORY" "$DIGEST" > release-image.txt
printf 'Published immutable reference to release-image.txt\n'
