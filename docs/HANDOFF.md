# HANDOFF: read this first

_Last updated: 2026-11-06_

## What this project is
A visualiser for ISRO/Bhuvan data, built as separate modules added one by one. It reuses the OpenLayers map + layer switcher + control patterns from `upstream/lookaround-map` but has **no Python backend**. Target: static hosting (GitHub Pages).

## Current state
- [x] Upstream project reviewed (`docs/UPSTREAM_NOTES.md`)
- [x] Bhuvan WMS GetCapabilities analysed (`docs/DATA_SOURCES.md`)
- [x] **Phase 1 DONE:** `data/catalog.json` schema v2: 36 states/UTs, 637 district layers, 40 state-level layers (`state_layers[]`), 40+ spelling fixes, validated (`data/catalog_report.txt`)
- [x] Phase 0 test page written: `isro.html` (plain HTML + OpenLayers 9.2.4 from jsDelivr, reads `data/catalog.json`). Not yet run on a live site; sandbox has no network.
- [ ] **Phase 0 RESULT NEEDED (NEXT)**: owner deploys to GitHub Pages, opens `isro.html`, clicks 'Run CORS checks' and clicks the map, then pastes the log ('Copy report') into the chat.
- [ ] Standalone page + Rollup entry
- [ ] LULC layer, pickers, legend, inspector, polish

## Immediate next step (superseded detail: page is built; see Phase 0 RESULT above)
Build a tiny `isro.html` test page (no build step) that:
1. Shows an OpenLayers map with one WMS layer, `sisdpv2:KL_Thiruvananthapuram_lulc_v2`, from `https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms`.
2. On click, calls GetFeatureInfo (`text/plain` and `application/json` if supported) and prints the result or the error.
Owner deploys it to GitHub Pages and reports back. If GetFeatureInfo is blocked by CORS, the fallback is a small Supabase edge function proxy.

## Key decisions (short)
- NDVI was the original goal, but the WMS has **no NDVI layers**. First module is **Land Use / Land Cover** instead. NDVI stays on the roadmap via another source. See DECISIONS.
- Standalone static page, not inside the Look Around app.
- Catalogue is generated and committed; never query GetCapabilities live (8 MB).

## How the owner works (follow this)
- Owner writes no build commands and prefers none suggested. **Agent writes the code; owner pushes to GitHub and checks the live GitHub Pages site.**
- Owner's other projects are static sites on GitHub Pages; Supabase is acceptable for small backend needs.
- Owner switches between accounts/agents, so keep this folder up to date: **update HANDOFF.md and append to SESSION_LOG.md at the end of every session.**
- Owner lives in Thiruvananthapuram, Kerala; Kerala is a good default test region.

## Gotchas
- Layer names are inconsistent (e.g. `KL_Alapurza`, `KL_Errnakulam`). Never construct names from patterns; use `catalog.json`. Display names are repaired only in `DISPLAY_FIXES` in `tools/build_catalog.py`.
- Odd codes are now merged (see DATA_SOURCES quirks). `CH` in district layers is Chhattisgarh!
- No layer has a time dimension, so no time slider and vintage is unknown.
- README of upstream asks users not to automate requests to the public Look Around instance (irrelevant for Bhuvan but keep a polite request rate).
