#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
require_env AWS_REGION EKS_CLUSTER NAMESPACE DEPLOYMENT CONTAINER
require_tools aws kubectl mktemp
read_approved_image
TASK_TMP=$(mktemp -d)
trap 'rm -rf -- "$TASK_TMP"' EXIT
export KUBECONFIG="$TASK_TMP/kubeconfig"
export AWS_PAGER=""
# Existing AWS provider chain must resolve to the protected deployment role.
aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER" \
  --kubeconfig "$KUBECONFIG" >/dev/null
deploy_image
