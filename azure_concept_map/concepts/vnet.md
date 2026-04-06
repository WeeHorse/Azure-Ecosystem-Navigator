# Virtual Network (VNet)

**Type:** Networking

## Short explanation
Fundamental private networking construct for Azure workloads.

## Why it matters
VNets create the network boundary in Azure that lets workloads communicate privately and connect to on-premises networks.

## Common relations
- Contains subnets.
- Connects to on-premises networks through VPN Gateway or ExpressRoute.
- Hosts workloads such as VMs, private endpoints, and some platform-integrated services.

## Typical security or governance concerns
- Poor subnet design complicates segmentation.
- Excessive public exposure undermines isolation.
- Weak routing and filtering patterns can widen attack paths.

## Official references
- [Azure Virtual Network overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/)

[Back to overview](../index.md)