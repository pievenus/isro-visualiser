# HANDOFF: read this first

_Last updated: 2026-11-06 (session 3)_

## What this project is
A visualiser for ISRO/Bhuvan data, built as separate modules added one by one. It reuses the OpenLayers map + layer switcher + control patterns from `upstream/lookaround-map` but has **no Python backend**. Target: static hosting (GitHub Pages).

## Current state
- [x] Upstream reviewed; WMS capabilities analysed; Phase 1 catalogue done (`data/catalog.json` v2)
- [x] Phase 0 DONE (live on https://pievenus.github.io/isro-visualiser/isro.html): tiles display OK, legend via <img> OK, **fetch()/GetFeatureInfo blocked (CORS)** -> Supabase proxy needed (D6)
- [x] `index.html` written (Phase 2+3): pickers, opacity, legend, click inspector via proxy, URL hash. **Not yet tested live.**
- [x] `supabase/functions/bhuvan-info/index.ts` written (GetFeatureInfo-only proxy, CORS locked to pievenus.github.io). **Not deployed.**
- [ ] **NEXT (owner):** create Supabase edge function `bhuvan-info` (dashboard > Edge Functions > paste the file; turn OFF "Verify JWT"), then put its URL in `PROXY` at the top of the script in `index.html`, push, test click info at /index.html.
- [ ] Phase 4 polish; next modules (slope, urban, groundwater, NDVI)

## Key decisions (short)
- NDVI was the original goal, but the WMS has **no NDVI layers**. First module is **Land Use / Land Cover** instead. NDVI stays on the roadmap via another source. See DECISIONS.
- Standalone static page, not inside the Look Around app.
- Catalogue is generated and committed; never query GetCapabilities live (8 MB).

## How the owner works (follow this)
- Owner writes no build commands and prefers none suggested. **Agent writes the code; owner pushes to GitHub and checks the live GitHub Pages site.**
- Owner's other projects are static sites on GitHub Pages; Supabase is acceptable for small backend needs.
- Owner switches between accounts/agents, so keep this folder up to date: **update HANDOFF.md and append to SESSION_LOG.md at the end of every session.**
- Owner lives in Thiruvananthapuram, Kerala; Kerala is a good default test region.
- **Deliver the whole repo as a zip every time anything changes** (owner request), then they copy it over and push.

## Gotchas
- Layer names are inconsistent (e.g. `KL_Alapurza`, `KL_Errnakulam`). Never construct names from patterns; use `catalog.json`. Display names are repaired only in `DISPLAY_FIXES` in `tools/build_catalog.py`.
- Odd codes are now merged (see DATA_SOURCES quirks). `CH` in district layers is Chhattisgarh!
- No layer has a time dimension, so no time slider and vintage is unknown.
- README of upstream asks users not to automate requests to the public Look Around instance (irrelevant for Bhuvan but keep a polite request rate).
