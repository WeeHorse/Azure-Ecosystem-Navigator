# Subscription

**Type:** Governance

## Short explanation
Administrative and billing boundary that contains Azure resources.

## Why it matters
Subscriptions are a key scope in Azure. Cost control, access assignment, policy, and many operational boundaries are commonly organized here.

## Common relations
- Belongs under a management group hierarchy.
- Contains resource groups and resources.
- Can receive RBAC and Policy assignments.
- Is often assessed by Defender for Cloud.

## Typical security or governance concerns
- Placing unrelated workloads in one subscription can blur ownership and cost tracking.
- Too much privilege at subscription scope is a common security mistake.

## Official references
- [Azure Resource Manager overview](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview)
- [Management groups overview](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview)

[Back to overview](../index.md)