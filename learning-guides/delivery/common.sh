#!/usr/bin/env bash
# Sourced helpers. Intended for trusted, isolated Linux release agents.
set -euo pipefail
umask 077

require_env() {
  local name
  for name in "$@"; do
    [[ -n "${!name:-}" ]] || { printf 'Missing variable: %s\n' "$name" >&2; exit 2; }
  done
}

require_tools() {
  local tool
  for tool in "$@"; do command -v "$tool" >/dev/null || exit 2; done
}

valid_tag() {
  [[ "$1" =~ ^[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}$ ]] || {
    printf 'Invalid image tag\n' >&2; exit 2;
  }
}

valid_repository() {
  [[ "$1" =~ ^[a-z0-9]+([._/-][a-z0-9]+)*$ ]] || {
    printf 'Repository must use the supported lowercase path form\n' >&2; exit 2;
  }
}

read_approved_image() {
  require_env APPROVED_REPOSITORY
  local release_file="${RELEASE_FILE:-release-image.txt}"
  IMAGE=$(cat -- "$release_file")
  [[ "$IMAGE" =~ ^[a-z0-9][a-z0-9./:_-]*@sha256:[a-f0-9]{64}$ ]] || {
    printf 'Expected one immutable image digest reference\n' >&2; exit 2;
  }
  [[ "${IMAGE%@*}" == "$APPROVED_REPOSITORY" ]] || {
    printf 'Image repository is outside the configured allowlist\n' >&2; exit 2;
  }
  # APPROVED_REPOSITORY comes from protected deployment config, not PR input.
}

deploy_image() {
  require_env NAMESPACE DEPLOYMENT CONTAINER
  kubectl auth can-i patch deployments.apps --namespace "$NAMESPACE" >/dev/null
  kubectl set image "deployment/$DEPLOYMENT" "$CONTAINER=$IMAGE" --namespace "$NAMESPACE"
  kubectl rollout status "deployment/$DEPLOYMENT" --namespace "$NAMESPACE" --timeout=180s
}
