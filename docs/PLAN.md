# PLAN

## Roadmap (modules added one by one)
1. **Land Use / Land Cover (Bhuvan WMS)**, current
2. Slope (`sdv` workspace, per district)
3. Urban themes by town (`nuis`, 153 towns)
4. Groundwater / water resources (`gw`, `twris`)
5. **NDVI**: needs a different data source (see DATA_SOURCES "NDVI"). Options: NRSC NOEDA downloads (login, single-user licence, can't re-host), or another ISRO/Bhuvan endpoint to be found.
6. Later ideas: rainfall, fire locations, ocean data.

Each module = one catalogue (if needed) + one `js/map/layers/isro/<name>.js` + optional control.

## Module 1 phases
- **Phase 0 Feasibility**: tiles load cross-origin? GetFeatureInfo CORS? Which info formats work? Fallback: Supabase edge-function proxy.
- **Phase 1 Catalogue**: DONE (schema v2, merged codes, spelling fixes, validation report). Possible later: map renamed UP districts to current names; add search index.
- **Phase 2 Layer**: `js/map/layers/isro/lulc.js` using OpenLayers `ImageWMS`/`TileWMS`; state + district pickers; zoom-to-bbox; opacity slider; state-level layer when zoomed out (scale hint max 1.75E7), district layer when zoomed in.
- **Phase 3 Legend + inspector**: scrollable legend panel (legend PNG is ~376x1020); click popup with class; degrade gracefully for 26 non-queryable layers.
- **Phase 4 Polish**: loading/error states when Bhuvan is slow; selection + opacity in URL fragment; permanent attribution; "vintage not published" note.

## Architecture
- New page `isro.html` + new Rollup input; reuse `js/map/map.js`, layer switcher, control patterns (`ColorLegendControl.js` for legends). Skip `app.py`, `routes/`, `js/viewer/`, protobuf view-state.
- Until the Rollup entry exists, prototype as a plain HTML page with OpenLayers from a CDN.

## Open questions
- Should the district picker cover all India from the start or a few states first? (Owner has not answered; default: all, because the catalogue already includes everything.)
