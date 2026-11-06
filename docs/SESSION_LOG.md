# SESSION LOG (append only; newest at bottom)

## Session 1: 2026-11-06 (earlier, previous account/session)
- Reviewed `lookaround-map-main.zip`; summarised in UPSTREAM_NOTES.
- Owner goal: ISRO data visualiser on top of this map, module by module, **NDVI first**.
- Researched Bhuvan/NOEDA (web): NDVI via NOEDA needs login; no confirmed NDVI WMS URL.
- Owner uploaded `getcapabilities_1_1_1.xml`; analysed it; found it is vector LULC/etc. with no NDVI and no time dimension, so proposed LULC as Module 1 and standalone page.
- Owner approved ("looks good") and asked for a repo with all logs so context survives switching accounts/agents.
- Session hit free-usage limit before the repo was delivered.

## Session 2: 2026-11-06 (this one)
- Re-verified XML facts directly (7,245 layers; 7,219 queryable; 0 dimensions; 0 "ndvi" matches; sisdpv2 = 637 layers over 34 states; basemap LULC = 44).
- Created this repo skeleton, `tools/build_catalog.py`, and generated `data/catalog.json` (637 district layers; 44 state-level entries, 8 of them odd codes to merge).
- Wrote README + docs. No UI code yet.
- **Next:** Phase 0 feasibility test page (see HANDOFF).

## Session 2 (cont.): Phase 0 page
- Wrote `isro.html`: OSM base + Bhuvan TileWMS, state/district pickers from catalog.json, opacity slider, tile ok/fail counters, click runs GetFeatureInfo in 4 formats (text/plain, application/json, text/html, GML) via fetch(), 'Run CORS checks' button probes GetMap/GetLegendGraphic via fetch() and <img>, 'Copy report' button.
- Could not test live (no network in sandbox); JS syntax checked only.
- **Next:** owner runs it on GitHub Pages and pastes the report. Decide: direct calls (if CORS ok) vs Supabase proxy.

## Session 2 (cont.): Phase 1 catalogue
- Found that district prefix `CH` is Chhattisgarh (bbox ~81E, 20.7N), fixed. Merged CG1, RJ1/2, PY1-4, DIU/Daman via BASEMAP_MAP (verified by bbox).
- Corrected earlier count: 40 state-level layers (the 44 included 4 zoomed-in Gujarat layers).
- Added ~40 display-name fixes, validation (no duplicates, no missing bbox) and `data/catalog_report.txt`.
- Updated `isro.html` for schema v2 (adds 'Whole state' option in the picker).
- **Next:** owner's local/live test of `isro.html` (Phase 0 result), then Phase 2 (real layer module).
