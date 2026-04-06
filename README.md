# Azure Structure Map Graphs

## Overview

This project provides three interactive Azure concept maps with a consistent UI/UX:

- Main ecosystem map
- Security-focused map
- Identity & governance-focused map

All map views now share the same behavior:

- Horizontally scrollable map frame
- Map auto-fit to frame width on load
- Zoom controls (`-`, `100%`, `+`) in the map header
- Clickable nodes opening concept content in an in-page modal overlay
- Shared top navigation with stable item ordering across map views

## Entrypoints

- `azure_concept_map/html/map-viewer.html` (main ecosystem map)
- `azure_security_map_v3/map-viewer.html` (security map)
- `azure_identity_governance_map_v1/map-viewer.html` (identity & governance map)

Notes:

- `azure_concept_map/html/index.html` is now a redirect to `map-viewer.html`.
- The old concept-list flow is intentionally retired from navigation.

## Run Locally

Because map pages fetch local assets (`diagram.md`, concept files, SVG), run via HTTP instead of `file://`.

From workspace root:

```bash
python3 -m http.server 8000
```

Open:

- `http://localhost:8000/azure_concept_map/html/map-viewer.html`
- `http://localhost:8000/azure_security_map_v3/map-viewer.html`
- `http://localhost:8000/azure_identity_governance_map_v1/map-viewer.html`

## Key Files

Main ecosystem map:

- `azure_concept_map/html/map-viewer.html`
- `azure_concept_map/assets/map-viewer.js`
- `azure_concept_map/assets/map-viewer.css`
- `azure_concept_map/azure-concepts-clickable.svg`
- `azure_concept_map/html/*.html` (concept content)

Security map:

- `azure_security_map_v3/map-viewer.html`
- `azure_security_map_v3/map-viewer.js`
- `azure_security_map_v3/diagram.md`
- `azure_security_map_v3/concepts/*.md`

Identity & governance map:

- `azure_identity_governance_map_v1/map-viewer.html`
- `azure_identity_governance_map_v1/map-viewer.js`
- `azure_identity_governance_map_v1/diagram.md`
- `azure_identity_governance_map_v1/concepts/*.md`
