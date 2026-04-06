# Managed Identity

## What it is
Allows Azure resources to authenticate without storing credentials.

## Security relevance
- Eliminates secrets in code
- Core DevSecOps pattern
- Strong identity-based security control

## Typical relationships
- Used by App Service, VM, Functions
- Accesses Key Vault and other resources
- Works with RBAC

## Official documentation
- https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview

## Tip
Bridge between identity, application security, and secrets.