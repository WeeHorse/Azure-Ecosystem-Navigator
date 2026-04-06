# Key Vault

**Type:** Secrets / Security

## Short explanation
Secure store for secrets, keys, and certificates.

## Why it matters
Key Vault reduces the need to hardcode secrets and centralizes protection and auditing for sensitive material.

## Common relations
- Used by applications and managed identities.
- Can be secured with Azure RBAC and networking controls.
- Sends monitoring data into Azure Monitor logs.

## Typical security or governance concerns
- Secrets copied into code or configs bypass Key Vault entirely.
- Too many principals with access increases leakage risk.
- Public exposure or lax network rules weakens protection.

## Official references
- [Azure Key Vault overview](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)
- [What is Azure Key Vault?](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts)
- [Key Vault RBAC guide](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide)

[Back to overview](../index.md)