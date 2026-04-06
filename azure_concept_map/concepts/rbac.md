# Azure RBAC

**Type:** Access Control

## Short explanation
Authorization model that controls who can do what at which Azure scope.

## Why it matters
RBAC is one of the most important Azure concepts for security because it translates identity into permission at management group, subscription, resource group, or resource level.

## Common relations
- Uses identities from Microsoft Entra ID.
- Applies at scopes like management group, subscription, resource group, and resource.
- Can grant roles to users, groups, service principals, and managed identities.

## Typical security or governance concerns
- Overbroad Contributor or Owner assignments are common weaknesses.
- Permanent high privilege increases blast radius.
- Assignments at too high a scope affect more resources than intended.

## Official references
- [Azure RBAC overview](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Azure built-in roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)

[Back to overview](../index.md)