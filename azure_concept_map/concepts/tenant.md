# Tenant

**Type:** Governance / Identity

## Short explanation
Top-level identity boundary in Azure, tied to a Microsoft Entra directory.

## Why it matters
A tenant is where identities, authentication, and many governance capabilities begin. It frames who can sign in and what organizational directory backs Azure access.

## Common relations
- Contains or is associated with subscriptions through organizational governance.
- Uses Microsoft Entra ID as the identity system for users, groups, apps, and managed identities.
- Provides the administrative context in which RBAC and policy decisions are applied.

## Typical security or governance concerns
- Weak identity hygiene at tenant level affects the whole organization.
- Poor separation between test and production tenants can create governance confusion.
- Insufficient MFA and conditional access can expose privileged administration.

## Official references
- [Microsoft Entra documentation](https://learn.microsoft.com/en-us/entra/identity/)
- [What is Microsoft Entra?](https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra)

[Back to overview](../index.md)