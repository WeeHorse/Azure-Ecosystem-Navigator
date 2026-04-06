# Private Endpoint

## What it is
Provides private IP access to Azure services within a VNet.

## Security relevance
- Removes public exposure of services
- Reduces attack surface significantly
- Key concept in secure cloud architecture

## Typical relationships
- Connects VNet to Storage, SQL, etc.
- Uses private IP and DNS
- Works with NSG and Firewall

## Official documentation
- https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview

## Tip
Concept in “no public internet exposure” patterns.