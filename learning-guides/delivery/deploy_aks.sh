#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
require_env AZURE_CLIENT_ID AZURE_SUBSCRIPTION_ID AKS_RESOURCE_GROUP AKS_CLUSTER NAMESPACE DEPLOYMENT CONTAINER
require_tools az kubelogin kubectl mktemp
read_approved_image
TASK_TMP=$(mktemp -d)
trap 'rm -rf -- "$TASK_TMP"' EXIT
export AZURE_CONFIG_DIR="$TASK_TMP/azure"
export KUBECONFIG="$TASK_TMP/kubeconfig"
mkdir -p "$AZURE_CONFIG_DIR"
az login --identity --client-id "$AZURE_CLIENT_ID" --output none --only-show-errors
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
# Managed Entra integration is assumed. Never request --admin here.
az aks get-credentials --resource-group "$AKS_RESOURCE_GROUP" --name "$AKS_CLUSTER" \
  --file "$KUBECONFIG" --overwrite-existing --only-show-errors
kubelogin convert-kubeconfig -l azurecli
deploy_image
