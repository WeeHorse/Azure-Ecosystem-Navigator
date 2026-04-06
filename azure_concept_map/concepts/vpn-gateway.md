# VPN Gateway

**Type:** Networking / Hybrid

## Short explanation
Encrypted connectivity between Azure VNets and on-premises or between VNets.

## Why it matters
VPN Gateway is a core hybrid connectivity concept when organizations need secure tunnels over the public internet.

## Common relations
- Connects on-premises networks to a VNet.
- Supports site-to-site, point-to-site, and VNet-to-VNet patterns.
- Uses a dedicated gateway subnet inside the VNet design.

## Typical security or governance concerns
- Weak tunnel design or key management can expose connectivity.
- Bandwidth and resilience planning matter for business-critical traffic.

## Official references
- [About Azure VPN Gateway](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways)
- [VPN Gateway settings](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-gateway-settings)

[Back to overview](../index.md)