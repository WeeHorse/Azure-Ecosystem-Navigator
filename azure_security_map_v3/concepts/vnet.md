# Virtual Network (VNet)

## What it is
Foundational private network boundary for Azure workloads, subnets, and private connectivity.

## Security relevance
- Core concept for segmentation and traffic design
- Anchor for NSG, Firewall, VPN, ExpressRoute, and Private Endpoint
- Central to hybrid architecture discussions

## Typical relationships
- Contains subnets and private endpoints
- Connects to on-prem via VPN or ExpressRoute
- Hosts workloads like VMs and App Services

## Official documentation
- https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview
- https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/

## Tip
Use this as the backbone when exploring how all other security controls attach to infrastructure.
