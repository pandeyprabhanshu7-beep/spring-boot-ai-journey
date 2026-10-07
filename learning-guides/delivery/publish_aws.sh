#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
require_env AWS_REGION AWS_ACCOUNT_ID ECR_REPOSITORY LOCAL_IMAGE IMAGE_TAG
require_tools aws docker mktemp
[[ "$AWS_ACCOUNT_ID" =~ ^[0-9]{12}$ ]] || exit 2
[[ "$AWS_REGION" =~ ^[a-z]{2}-[a-z]+-[0-9]+$ ]] || exit 2
valid_tag "$IMAGE_TAG"
valid_repository "$ECR_REPOSITORY"
TASK_TMP=$(mktemp -d)
trap 'rm -rf -- "$TASK_TMP"' EXIT
export DOCKER_CONFIG="$TASK_TMP/docker"
mkdir -p "$DOCKER_CONFIG"
export AWS_PAGER=""
# Commercial AWS partition example; adapt endpoints for other partitions.
REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
REMOTE_IMAGE="$REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
aws ecr get-login-password --region "$AWS_REGION" |
  docker login --username AWS --password-stdin "$REGISTRY"
docker tag "$LOCAL_IMAGE" "$REMOTE_IMAGE"
docker push "$REMOTE_IMAGE"
DIGEST=$(aws ecr describe-images --region "$AWS_REGION" \
  --registry-id "$AWS_ACCOUNT_ID" --repository-name "$ECR_REPOSITORY" \
  --image-ids "imageTag=$IMAGE_TAG" --query 'imageDetails[0].imageDigest' --output text)
[[ "$DIGEST" =~ ^sha256:[a-f0-9]{64}$ ]] || exit 3
# Registry tag immutability is a prerequisite for resolving this tag safely.
printf '%s@%s\n' "$REGISTRY/$ECR_REPOSITORY" "$DIGEST" > release-image.txt
printf 'Published immutable reference to release-image.txt\n'
