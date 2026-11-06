# DECISIONS

| # | Decision | Why |
|---|----------|-----|
| D1 | Standalone static page, not inside the Look Around map | Look Around needs a Flask server; Bhuvan data doesn't. Static = GitHub Pages, matching owner's other projects. |
| D2 | First module is LULC, not NDVI | The uploaded Bhuvan WMS capabilities contains zero "ndvi" layers (verified: 0 matches). NDVI needs another source. |
| D3 | Generate and commit `catalog.json` | 7,245 layers / 8 MB capabilities; names are inconsistent; no live query needed. |
| D4 | Never rewrite real layer names, only display names | Names are what the server expects. |
| D5 | Agent writes code, owner pushes + tests on live site | Owner's workflow; no build commands suggested. |
| D6 | Supabase edge function is the fallback if CORS blocks GetFeatureInfo | Keeps hosting static. |
| D7 | Keep `upstream/lookaround-map` as an unmodified reference copy | MIT licence; submodule `lookaround` (Apple API) is missing from the zip and irrelevant here. |
| D8 | Don't re-host NOEDA raw files | NOEDA licence is single-user; attribution required. |
| D9 | Catalogue schema v2: `state_layers[]` (list) instead of a single `state_layer` | Some states (RJ, PY, DD) have several state-level layers. |
| D10 | Service code `CH` in district layers is mapped to `CG` (Chhattisgarh) | Verified by bounding box; an earlier assumption of Chandigarh was wrong. |
