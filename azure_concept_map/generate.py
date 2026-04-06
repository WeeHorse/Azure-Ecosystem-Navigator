from pathlib import Path
import html
import textwrap
import zipfile

base = Path('/mnt/data/azure_concept_map')
concepts_dir = base / 'concepts'
html_dir = base / 'html'
assets_dir = base / 'assets'

concepts = {
    'tenant': {
        'title': 'Tenant',
        'summary': 'Top-level identity boundary in Azure, tied to a Microsoft Entra directory.',
        'type': 'Governance / Identity',
        'why': 'A tenant is where identities, authentication, and many governance capabilities begin. It frames who can sign in and what organizational directory backs Azure access.',
        'relations': [
            'Contains or is associated with subscriptions through organizational governance.',
            'Uses Microsoft Entra ID as the identity system for users, groups, apps, and managed identities.',
            'Provides the administrative context in which RBAC and policy decisions are applied.'
        ],
        'risks': [
            'Weak identity hygiene at tenant level affects the whole organization.',
            'Poor separation between test and production tenants can create governance confusion.',
            'Insufficient MFA and conditional access can expose privileged administration.'
        ],
        'docs': [
            ('Microsoft Entra documentation', 'https://learn.microsoft.com/en-us/entra/identity/'),
            ('What is Microsoft Entra?', 'https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra')
        ]
    },
    'management-group': {
        'title': 'Management Group',
        'summary': 'Hierarchy level above subscriptions for consistent policy and access management.',
        'type': 'Governance',
        'why': 'Management groups let you apply governance across multiple subscriptions instead of repeating the same settings manually.',
        'relations': [
            'Contains subscriptions and possibly child management groups.',
            'Provides a scope for Azure Policy and RBAC assignments.',
            'Helps standardize large Azure estates.'
        ],
        'risks': [
            'Overly complex hierarchies make responsibility unclear.',
            'Broad assignments at high scope can unintentionally affect many subscriptions.'
        ],
        'docs': [
            ('Azure management groups overview', 'https://learn.microsoft.com/en-us/azure/governance/management-groups/overview'),
            ('Management groups documentation', 'https://learn.microsoft.com/en-us/azure/governance/management-groups/')
        ]
    },
    'subscription': {
        'title': 'Subscription',
        'summary': 'Administrative and billing boundary that contains Azure resources.',
        'type': 'Governance',
        'why': 'Subscriptions are a key scope in Azure. Cost control, access assignment, policy, and many operational boundaries are commonly organized here.',
        'relations': [
            'Belongs under a management group hierarchy.',
            'Contains resource groups and resources.',
            'Can receive RBAC and Policy assignments.',
            'Is often assessed by Defender for Cloud.'
        ],
        'risks': [
            'Placing unrelated workloads in one subscription can blur ownership and cost tracking.',
            'Too much privilege at subscription scope is a common security mistake.'
        ],
        'docs': [
            ('Azure Resource Manager overview', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview'),
            ('Management groups overview', 'https://learn.microsoft.com/en-us/azure/governance/management-groups/overview')
        ]
    },
    'resource-group': {
        'title': 'Resource Group',
        'summary': 'Container for related Azure resources, often grouped by lifecycle.',
        'type': 'Governance / Operations',
        'why': 'Resource groups help teams deploy, update, secure, and delete sets of resources together.',
        'relations': [
            'Lives inside a subscription.',
            'Contains resources such as VMs, storage accounts, VNets, and Key Vaults.',
            'Can receive RBAC and policy assignments.'
        ],
        'risks': [
            'Mixing unrelated resources can make change management harder.',
            'Deleting a resource group can delete all contained resources.'
        ],
        'docs': [
            ('What is a resource group?', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal'),
            ('Azure Resource Manager overview', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview')
        ]
    },
    'entra-id': {
        'title': 'Microsoft Entra ID',
        'summary': 'Cloud identity and access management service for users, groups, apps, and devices.',
        'type': 'Identity',
        'why': 'Authentication starts here for many Azure scenarios. Entra ID underpins identity, sign-in, conditional access, app identities, and more.',
        'relations': [
            'Authenticates users, groups, apps, and managed identities.',
            'Works with RBAC to authorize access to Azure resources.',
            'Integrates with on-premises identity in hybrid setups.'
        ],
        'risks': [
            'Weak authentication controls can expose cloud administration.',
            'Poor role hygiene or stale groups can create privilege creep.',
            'Hybrid identity sync issues can spread mistakes across environments.'
        ],
        'docs': [
            ('Microsoft Entra ID documentation', 'https://learn.microsoft.com/en-us/entra/identity/'),
            ('Microsoft Entra product family', 'https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra')
        ]
    },
    'rbac': {
        'title': 'Azure RBAC',
        'summary': 'Authorization model that controls who can do what at which Azure scope.',
        'type': 'Access Control',
        'why': 'RBAC is one of the most important Azure concepts for security because it translates identity into permission at management group, subscription, resource group, or resource level.',
        'relations': [
            'Uses identities from Microsoft Entra ID.',
            'Applies at scopes like management group, subscription, resource group, and resource.',
            'Can grant roles to users, groups, service principals, and managed identities.'
        ],
        'risks': [
            'Overbroad Contributor or Owner assignments are common weaknesses.',
            'Permanent high privilege increases blast radius.',
            'Assignments at too high a scope affect more resources than intended.'
        ],
        'docs': [
            ('Azure RBAC overview', 'https://learn.microsoft.com/en-us/azure/role-based-access-control/overview'),
            ('Azure built-in roles', 'https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles')
        ]
    },
    'policy': {
        'title': 'Azure Policy',
        'summary': 'Governance service that evaluates and enforces rules across Azure resources.',
        'type': 'Governance / Compliance',
        'why': 'Policy is how organizations turn standards into enforceable rules. It helps with compliance, allowed SKUs, tagging, secure configuration, and remediation patterns.',
        'relations': [
            'Applies at management group, subscription, resource group, or resource scope.',
            'Evaluates resources against definitions and effects.',
            'Supports broad governance and security baselines.'
        ],
        'risks': [
            'Overly aggressive policy can block valid deployments.',
            'Lax policy leaves misconfigurations undetected.',
            'Unclear ownership of policy exceptions undermines governance.'
        ],
        'docs': [
            ('Azure Policy overview', 'https://learn.microsoft.com/en-us/azure/governance/policy/overview'),
            ('Policy definition structure basics', 'https://learn.microsoft.com/en-us/azure/governance/policy/concepts/definition-structure-basics')
        ]
    },
    'vnet': {
        'title': 'Virtual Network (VNet)',
        'summary': 'Fundamental private networking construct for Azure workloads.',
        'type': 'Networking',
        'why': 'VNets create the network boundary in Azure that lets workloads communicate privately and connect to on-premises networks.',
        'relations': [
            'Contains subnets.',
            'Connects to on-premises networks through VPN Gateway or ExpressRoute.',
            'Hosts workloads such as VMs, private endpoints, and some platform-integrated services.'
        ],
        'risks': [
            'Poor subnet design complicates segmentation.',
            'Excessive public exposure undermines isolation.',
            'Weak routing and filtering patterns can widen attack paths.'
        ],
        'docs': [
            ('Azure Virtual Network overview', 'https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview'),
            ('Introduction to Azure Virtual Networks', 'https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/')
        ]
    },
    'vpn-gateway': {
        'title': 'VPN Gateway',
        'summary': 'Encrypted connectivity between Azure VNets and on-premises or between VNets.',
        'type': 'Networking / Hybrid',
        'why': 'VPN Gateway is a core hybrid connectivity concept when organizations need secure tunnels over the public internet.',
        'relations': [
            'Connects on-premises networks to a VNet.',
            'Supports site-to-site, point-to-site, and VNet-to-VNet patterns.',
            'Uses a dedicated gateway subnet inside the VNet design.'
        ],
        'risks': [
            'Weak tunnel design or key management can expose connectivity.',
            'Bandwidth and resilience planning matter for business-critical traffic.'
        ],
        'docs': [
            ('About Azure VPN Gateway', 'https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways'),
            ('VPN Gateway settings', 'https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-gateway-settings')
        ]
    },
    'expressroute': {
        'title': 'ExpressRoute',
        'summary': 'Private connection from on-premises infrastructure into Microsoft cloud services.',
        'type': 'Networking / Hybrid',
        'why': 'ExpressRoute is often used when organizations need more predictable, private, enterprise-grade connectivity than internet-based VPN.',
        'relations': [
            'Connects on-premises networks to Azure over a private connection.',
            'Used in hybrid architectures alongside VNets and corporate networking.'
        ],
        'risks': [
            'Requires provider coordination and careful resilience planning.',
            'A private connection is not automatically a secure architecture without segmentation and governance.'
        ],
        'docs': [
            ('Azure ExpressRoute overview', 'https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction'),
            ('ExpressRoute documentation', 'https://learn.microsoft.com/en-us/azure/expressroute/')
        ]
    },
    'key-vault': {
        'title': 'Key Vault',
        'summary': 'Secure store for secrets, keys, and certificates.',
        'type': 'Secrets / Security',
        'why': 'Key Vault reduces the need to hardcode secrets and centralizes protection and auditing for sensitive material.',
        'relations': [
            'Used by applications and managed identities.',
            'Can be secured with Azure RBAC and networking controls.',
            'Sends monitoring data into Azure Monitor logs.'
        ],
        'risks': [
            'Secrets copied into code or configs bypass Key Vault entirely.',
            'Too many principals with access increases leakage risk.',
            'Public exposure or lax network rules weakens protection.'
        ],
        'docs': [
            ('Azure Key Vault overview', 'https://learn.microsoft.com/en-us/azure/key-vault/general/overview'),
            ('What is Azure Key Vault?', 'https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts'),
            ('Key Vault RBAC guide', 'https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide')
        ]
    },
    'monitor': {
        'title': 'Azure Monitor',
        'summary': 'Unified observability service for metrics, logs, traces, and events from cloud and hybrid resources.',
        'type': 'Monitoring / Operations',
        'why': 'Security and operations both depend on telemetry. Azure Monitor helps teams observe workload health, behavior, and signals that feed further analytics.',
        'relations': [
            'Collects telemetry from Azure and hybrid environments.',
            'Works with logs, alerts, dashboards, and related tools.',
            'Can feed data used by Microsoft Sentinel and Defender for Cloud scenarios.'
        ],
        'risks': [
            'Insufficient logging reduces detection and troubleshooting ability.',
            'Collecting telemetry without ownership creates alert fatigue.',
            'Sensitive logs still need access control and retention management.'
        ],
        'docs': [
            ('Azure Monitor overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview'),
            ('Azure Monitor Agent overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview')
        ]
    },
    'defender': {
        'title': 'Defender for Cloud',
        'summary': 'Cloud security posture and threat protection across Azure and hybrid workloads.',
        'type': 'Security',
        'why': 'Defender for Cloud is useful as a bridge between governance, posture management, recommendations, and threat protection across cloud and hybrid estates.',
        'relations': [
            'Assesses subscriptions and workloads for security posture.',
            'Works across hybrid and multicloud contexts.',
            'Integrates with broader security tooling and workflows.'
        ],
        'risks': [
            'Security recommendations without ownership do not improve posture.',
            'Teams can mistake visibility for remediation if workflows are not defined.'
        ],
        'docs': [
            ('Defender for Cloud overview', 'https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction'),
            ('Defender for Cloud documentation', 'https://learn.microsoft.com/en-us/azure/defender-for-cloud/')
        ]
    },
    'arc': {
        'title': 'Azure Arc',
        'summary': 'Extends Azure management, governance, and security to on-premises and multicloud resources.',
        'type': 'Hybrid / Governance',
        'why': 'Arc is central when teaching hybrid environments because it shows how Azure control-plane patterns can be extended beyond native Azure resources.',
        'relations': [
            'Extends governance and management to servers, Kubernetes, and other external resources.',
            'Works with Azure services such as Monitor and Defender for Cloud.',
            'Represents non-Azure machines in Azure for consistent operations.'
        ],
        'risks': [
            'Hybrid machines need secure onboarding and lifecycle management.',
            'Inconsistent standards between cloud and on-prem can still persist if governance is weak.'
        ],
        'docs': [
            ('Azure Arc overview', 'https://learn.microsoft.com/en-us/azure/azure-arc/overview'),
            ('Azure Arc-enabled servers overview', 'https://learn.microsoft.com/en-us/azure/azure-arc/servers/overview')
        ]
    },
    'on-prem': {
        'title': 'On-premises Environment',
        'summary': 'Local datacenter or corporate infrastructure outside Azure.',
        'type': 'Hybrid',
        'why': 'Hybrid security depends on understanding that organizations often operate across local infrastructure and cloud services at the same time.',
        'relations': [
            'Connects to Azure through VPN Gateway or ExpressRoute.',
            'May integrate identity and monitoring with Azure services.',
            'Can be represented and governed through Azure Arc.'
        ],
        'risks': [
            'Different control models between on-prem and cloud create blind spots.',
            'Legacy systems can weaken otherwise modern cloud security patterns.'
        ],
        'docs': [
            ('Azure Arc overview', 'https://learn.microsoft.com/en-us/azure/azure-arc/overview'),
            ('VPN Gateway documentation', 'https://learn.microsoft.com/en-us/azure/vpn-gateway/'),
            ('ExpressRoute documentation', 'https://learn.microsoft.com/en-us/azure/expressroute/')
        ]
    }
}

readme = """# Azure Concept Map Starter Pack

This package gives you a first clickable concept map for **Azure security and hybrid environments**.

## Files

- `azure-concepts-clickable.svg` — static diagram with clickable nodes.
- `azure-concepts.dot` — Graphviz source.
- `azure-concepts-mermaid.md` — Mermaid version with click directives.
- `index.md` — overview page.
- `concepts/` — Markdown concept cards.
- `html/` — HTML concept cards and a landing page.

## How to use

### Fastest
Open `azure-concepts-clickable.svg` in a browser and click nodes.

### If you want Markdown-first
Open `index.md` and `azure-concepts-mermaid.md` in a Markdown viewer that supports Mermaid click links.

### If you want browser pages
Open `html/index.html`.

## Suggested teaching use

1. Start with the overview diagram.
2. Click into one concept at a time.
3. Let students compare governance, identity, networking, monitoring, and hybrid concepts.
4. Extend the graph with more nodes such as NSG, Firewall, Managed Identity, SQL, Sentinel, and Private Endpoint.
"""

(base / 'index.md').write_text(readme, encoding='utf-8')

for slug, c in concepts.items():
    md = [f"# {c['title']}", '', f"**Type:** {c['type']}", '', f"## Short explanation\n{c['summary']}", '', f"## Why it matters\n{c['why']}", '', '## Common relations']
    md += [f"- {x}" for x in c['relations']]
    md += ['', '## Typical security or governance concerns']
    md += [f"- {x}" for x in c['risks']]
    md += ['', '## Official references']
    md += [f"- [{name}]({url})" for name, url in c['docs']]
    md += ['', '[Back to overview](../index.md)']
    (concepts_dir / f'{slug}.md').write_text('\n'.join(md), encoding='utf-8')

    links = ''.join(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{html.escape(name)}</a></li>' for name, url in c['docs'])
    rels = ''.join(f'<li>{html.escape(x)}</li>' for x in c['relations'])
    risks = ''.join(f'<li>{html.escape(x)}</li>' for x in c['risks'])
    page = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{html.escape(c['title'])}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 900px; line-height: 1.6; padding: 0 1rem; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 1rem 1.25rem; margin: 1rem 0; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .muted {{ color: #555; }}
  </style>
</head>
<body>
  <p><a href=\"index.html\">← Back to overview</a></p>
  <h1>{html.escape(c['title'])}</h1>
  <p class=\"muted\"><strong>Type:</strong> {html.escape(c['type'])}</p>
  <div class=\"card\">
    <h2>Short explanation</h2>
    <p>{html.escape(c['summary'])}</p>
  </div>
  <div class=\"card\">
    <h2>Why it matters</h2>
    <p>{html.escape(c['why'])}</p>
  </div>
  <div class=\"card\">
    <h2>Common relations</h2>
    <ul>{rels}</ul>
  </div>
  <div class=\"card\">
    <h2>Typical security or governance concerns</h2>
    <ul>{risks}</ul>
  </div>
  <div class=\"card\">
    <h2>Official references</h2>
    <ul>{links}</ul>
  </div>
</body>
</html>
"""
    (html_dir / f'{slug}.html').write_text(page, encoding='utf-8')

# Mermaid
mermaid = """# Azure concepts Mermaid map

```mermaid
flowchart TD
    Tenant["Tenant"]
    MG["Management Group"]
    Sub["Subscription"]
    RG["Resource Group"]
    Entra["Microsoft Entra ID"]
    RBAC["Azure RBAC"]
    Policy["Azure Policy"]
    VNet["VNet"]
    VPN["VPN Gateway"]
    ER["ExpressRoute"]
    KV["Key Vault"]
    Monitor["Azure Monitor"]
    Defender["Defender for Cloud"]
    Arc["Azure Arc"]
    OnPrem["On-premises Environment"]

    Tenant -->|identity context| MG
    MG -->|contains| Sub
    Sub -->|contains| RG
    Entra -->|authenticates| RBAC
    RBAC -->|authorizes at scope| MG
    RBAC -->|authorizes at scope| Sub
    RBAC -->|authorizes at scope| RG
    Policy -->|governs| MG
    Policy -->|governs| Sub
    RG -->|contains| VNet
    RG -->|contains| KV
    VNet -->|connects via| VPN
    VNet -->|connects via| ER
    OnPrem -->|connects to| VPN
    OnPrem -->|connects to| ER
    Monitor -->|observes| RG
    Monitor -->|observes| OnPrem
    Defender -->|assesses| Sub
    Defender -->|protects| OnPrem
    Arc -->|extends governance to| OnPrem
    Arc -->|integrates with| Monitor
    Arc -->|integrates with| Defender

    click Tenant href "./concepts/tenant.md" "Open Tenant card"
    click MG href "./concepts/management-group.md" "Open Management Group card"
    click Sub href "./concepts/subscription.md" "Open Subscription card"
    click RG href "./concepts/resource-group.md" "Open Resource Group card"
    click Entra href "./concepts/entra-id.md" "Open Entra ID card"
    click RBAC href "./concepts/rbac.md" "Open RBAC card"
    click Policy href "./concepts/policy.md" "Open Policy card"
    click VNet href "./concepts/vnet.md" "Open VNet card"
    click VPN href "./concepts/vpn-gateway.md" "Open VPN Gateway card"
    click ER href "./concepts/expressroute.md" "Open ExpressRoute card"
    click KV href "./concepts/key-vault.md" "Open Key Vault card"
    click Monitor href "./concepts/monitor.md" "Open Azure Monitor card"
    click Defender href "./concepts/defender.md" "Open Defender for Cloud card"
    click Arc href "./concepts/arc.md" "Open Azure Arc card"
    click OnPrem href "./concepts/on-prem.md" "Open On-premises card"
```
"""
(base / 'azure-concepts-mermaid.md').write_text(mermaid, encoding='utf-8')

# Graphviz source
node_lines = []
for slug, c in concepts.items():
    label = c['title']
    url = f'html/{slug}.html'
    node_lines.append(f'  "{slug}" [label="{label}", URL="{url}", target="_top", tooltip="{label}"];')

edges = [
    ('tenant', 'management-group', 'identity context'),
    ('management-group', 'subscription', 'contains'),
    ('subscription', 'resource-group', 'contains'),
    ('entra-id', 'rbac', 'authenticates'),
    ('rbac', 'management-group', 'authorizes at scope'),
    ('rbac', 'subscription', 'authorizes at scope'),
    ('rbac', 'resource-group', 'authorizes at scope'),
    ('policy', 'management-group', 'governs'),
    ('policy', 'subscription', 'governs'),
    ('resource-group', 'vnet', 'contains'),
    ('resource-group', 'key-vault', 'contains'),
    ('vnet', 'vpn-gateway', 'connects via'),
    ('vnet', 'expressroute', 'connects via'),
    ('on-prem', 'vpn-gateway', 'connects to'),
    ('on-prem', 'expressroute', 'connects to'),
    ('monitor', 'resource-group', 'observes'),
    ('monitor', 'on-prem', 'observes'),
    ('defender', 'subscription', 'assesses'),
    ('defender', 'on-prem', 'protects'),
    ('arc', 'on-prem', 'extends governance to'),
    ('arc', 'monitor', 'integrates with'),
    ('arc', 'defender', 'integrates with'),
]

edge_lines = [f'  "{a}" -> "{b}" [label="{label}"];' for a,b,label in edges]

dot = "digraph AzureConcepts {\n  rankdir=LR;\n  graph [pad=0.2, nodesep=0.5, ranksep=0.8];\n  node [shape=box, style=rounded, fontname=Helvetica, fontsize=11, margin=0.18];\n  edge [fontname=Helvetica, fontsize=10];\n" + "\n".join(node_lines) + "\n" + "\n".join(edge_lines) + "\n}\n"
(base / 'azure-concepts.dot').write_text(dot, encoding='utf-8')

# HTML index
cards = ''.join(f'<li><a href="{slug}.html">{c["title"]}</a> — {html.escape(c["summary"])}.</li>' for slug, c in concepts.items())
html_index = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Azure Concept Map</title>
    <link rel=\"stylesheet\" href=\"../assets/map-viewer.css\">
  <style>
        body {{ margin: 0; line-height: 1.6; }}
        .list-shell {{ max-width: 1160px; margin: 0 auto; padding: 0 1.25rem 2.2rem; }}
        .card {{ border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.25rem; margin: 1rem 0; background: #fff; box-shadow: var(--shadow); }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 12px; }}
        .card a:not(.btn) {{ color: #0b57d0; }}
  </style>
</head>
<body>
    <header class=\"hero\">
        <div class=\"hero-inner\">
            <p class=\"eyebrow\">Azure Ecosystem Navigator</p>
            <h1>Concept List</h1>
            <p class=\"subtitle\">Browse all concept cards directly, or jump to either map view from the same fixed menu.</p>
            <nav class=\"site-nav\" aria-label=\"Primary\">
                <ul class=\"site-menu\">
                    <li><a class=\"btn\" href=\"map-viewer.html\">Main Map</a></li>
                    <li><a class=\"btn is-active\" href=\"index.html\" aria-current=\"page\">Concept List</a></li>
                    <li><a class=\"btn\" href=\"../../azure_security_map_v3/map-viewer.html\">Security Map</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class=\"list-shell\">
        <div class=\"card\">
            <p>This is a starter map for Azure security and hybrid environments. Open the SVG below in a browser or click the concept pages in the list.</p>
            <p><a href=\"map-viewer.html\">Open interactive map viewer (scroll + modal)</a></p>
            <p><a href=\"../azure-concepts-clickable.svg\">Open clickable SVG</a></p>
        </div>
        <div class=\"card\">
            <h2>Concept cards</h2>
            <ul>{cards}</ul>
        </div>
    </main>
</body>
</html>
"""
(html_dir / 'index.html').write_text(html_index, encoding='utf-8')

print('Generated source files.')
