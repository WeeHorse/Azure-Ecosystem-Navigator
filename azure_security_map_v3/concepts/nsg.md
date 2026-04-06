# Network Security Group (NSG)

## What it is
Filters inbound and outbound network traffic using allow/deny rules.

## Security relevance
- Implements least privilege at network level
- Key control for segmentation
- Simple but critical building block

## Typical relationships
- Attached to subnets or NICs
- Works alongside VNet and Firewall
- Protects workloads like VMs

## Official documentation
- https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview

## Tip
Compare NSG (distributed control) vs Firewall (centralized control).