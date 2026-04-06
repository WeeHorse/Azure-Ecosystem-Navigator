# Azure Structure Map Graphs

## Entrypoints

Primary entrypoint for the ecosystem map:
- `azure_concept_map/html/map-viewer.html`

What it does:
- Shows the full Azure concept map in a horizontally scrollable viewport.
- Lets you click map nodes to open concept details in an overlay modal.

Security-focused map entrypoint:
- `azure_security_map_v3/map-viewer.html`

Identity/governance-focused map entrypoint:
- `azure_identity_governance_map_v1/map-viewer.html`

## Run locally

Because the interactive page loads assets with `fetch`, run it through a local web server (not `file://`).

From the workspace root:

```bash
python3 -m http.server 8000
```

Then open:
- `http://localhost:8000/azure_concept_map/html/map-viewer.html` (ecosystem map)
- `http://localhost:8000/azure_security_map_v3/map-viewer.html` (security map)
- `http://localhost:8000/azure_identity_governance_map_v1/map-viewer.html` (identity/governance map)

## Where key files live

- `azure_concept_map/html/map-viewer.html` - interactive UI shell
- `azure_concept_map/assets/map-viewer.js` - SVG loading, node click handling, modal logic
- `azure_concept_map/assets/map-viewer.css` - layout and modal styling
- `azure_concept_map/azure-concepts-clickable.svg` - map graphic with node links
- `azure_concept_map/html/*.html` - concept pages used as modal content
- `azure_security_map_v3/map-viewer.html` - security map UI shell
- `azure_security_map_v3/map-viewer.js` - Mermaid rendering, node click handling, modal logic
- `azure_security_map_v3/diagram.md` - Mermaid security graph source
- `azure_security_map_v3/concepts/*.md` - markdown concept cards used as modal content
- `azure_identity_governance_map_v1/map-viewer.html` - identity/governance map UI shell
- `azure_identity_governance_map_v1/map-viewer.js` - Mermaid rendering, node click handling, modal logic
- `azure_identity_governance_map_v1/diagram.md` - Mermaid identity/governance graph source
- `azure_identity_governance_map_v1/concepts/*.md` - markdown concept cards used as modal content
