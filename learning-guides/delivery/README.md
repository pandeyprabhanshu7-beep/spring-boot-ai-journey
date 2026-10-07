# Delivery examples: prerequisite and identity contract

These templates execute real publish/deploy operations when you run them. They were syntax-checked, not run against cloud resources. Use trusted isolated Linux agents with pre-provisioned resources and reviewed identity policies. Source examples use commercial AWS and Azure public-cloud endpoints.

## Common requirements

- Bash, cloud CLI, Docker for publishing, kubectl for deployment; kubelogin for AKS.
- A local candidate image already built and tested. The publisher does not rebuild it.
- Release tags protected against overwrite and concurrent conflicting publication. The scripts resolve a tag after pushing; mutable tags would introduce a race. Stronger implementations capture and verify the pushed manifest digest directly.
- Protected release jobs, provenance/signature verification, environment approval and deployment serialization supplied by your CI/GitOps system.
- Existing namespace, Deployment/container, image-pull identity, compatible configuration and health probes.
- Registry read permission to resolve the digest, in addition to push. Azure `az acr show` also requires management-plane read of the registry.
- Scripts assume deployment permissions include patch plus read/watch needed to observe rollout. `auth can-i patch` is only a preflight for one action.

## AWS publisher

Set `AWS_REGION`, `AWS_ACCOUNT_ID`, `ECR_REPOSITORY`, `LOCAL_IMAGE`, `IMAGE_TAG`.
The AWS SDK/CLI credential chain must resolve to the intended role. TeamCity can inject its temporary shared-credentials file; Jenkins on an approved AWS agent can use an instance role or an explicitly assumed release role. ECR needs authorization-token permission plus repository upload and `DescribeImages` permissions. See the guide for the separate trust and permission policies.

Run from the bundle root: `bash delivery/publish_aws.sh`.

## Azure publisher

Set `AZURE_CLIENT_ID`, `AZURE_SUBSCRIPTION_ID`, `ACR_NAME`, `ACR_LOGIN_SERVER`, `ACR_REPOSITORY`, `LOCAL_IMAGE`, `IMAGE_TAG`.
The supplied script uses a **user-assigned managed identity attached to the Azure VM agent**. Its subscription must be visible to that identity, registry metadata readable, and repository push/read permitted under the registry's RBAC/ABAC mode.

Run: `bash delivery/publish_azure.sh`.
For Azure Pipelines/GitHub federation, adapt the authentication layer: the task/action already logs in. Do not replace its session with VM identity accidentally.

## Deployment

Both deployers read `RELEASE_FILE` (default `release-image.txt`). Set `APPROVED_REPOSITORY` to the exact protected allowed registry/repository, without tag/digest. Set `NAMESPACE`, `DEPLOYMENT`, `CONTAINER`.

EKS additionally needs `AWS_REGION`, `EKS_CLUSTER` and a deployment-role credential chain, cluster discovery permission and an access entry/RBAC mapping.

AKS additionally needs `AZURE_CLIENT_ID`, `AZURE_SUBSCRIPTION_ID`, `AKS_RESOURCE_GROUP`, `AKS_CLUSTER`. The example uses VM managed identity, managed Entra integration, cluster-user credential retrieval permission and namespace-level authorization.

Run the selected `bash delivery/deploy_eks.sh` or `bash delivery/deploy_aks.sh` only after approval of the release record. These scripts update the existing Deployment image and observe rollout; they do not execute schema migrations, verify signatures, provision roles or create infrastructure.

## Local checks

```bash
python3 -m unittest discover -s delivery -p 'test_*.py'
```

Run `bash -n` on each shell file. The scripts create per-job configuration directories with restricted permissions and remove them on exit. They do not erase Docker daemon caches; use disposable agents to avoid cross-job state and privilege leakage. Do not enable shell xtrace around credentials.
