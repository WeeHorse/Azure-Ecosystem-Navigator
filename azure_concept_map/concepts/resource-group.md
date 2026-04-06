# Resource Group

**Type:** Governance / Operations

## Short explanation
Container for related Azure resources, often grouped by lifecycle.

## Why it matters
Resource groups help teams deploy, update, secure, and delete sets of resources together.

## Common relations
- Lives inside a subscription.
- Contains resources such as VMs, storage accounts, VNets, and Key Vaults.
- Can receive RBAC and policy assignments.

## Typical security or governance concerns
- Mixing unrelated resources can make change management harder.
- Deleting a resource group can delete all contained resources.

## Official references
- [What is a resource group?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal)
- [Azure Resource Manager overview](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview)

[Back to overview](../index.md)