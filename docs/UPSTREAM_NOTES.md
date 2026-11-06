# UPSTREAM NOTES: sk-zk/lookaround-map (MIT, (c) 2022 skzk)

Web viewer for Apple Look Around panoramas using reverse-engineered Apple Maps endpoints.

- **Backend:** Flask (`app.py`, `routes/api.py`, `limiter.py`), proxy-fix, CORS, compression, IP blacklist (`config/blacklist.txt`), rate limits. Endpoints: `/tiles/coverage/x/y`, `/closest` (100 m, 5 req/s), `/address`, `/pano/<id>/<build>/<zoom>/<face>`. HEIC to JPEG via heic2rgb/pyheif/pillow-heif.
- **Missing submodule:** `sk-zk/lookaround` (imported as `lookaround.auth`, `.geocode`) is not in the zip, so the server can't run. Irrelevant to this project.
- **Frontend:** Rollup bundle; OpenLayers map in `js/map/` (Apple/Google/OSM base layers; layer files in `js/map/layers/`, e.g. `openStreetMap.js`, `coverageLayer.js`); viewer = Photo Sphere Viewer + three.js in `js/viewer/`; UI controls in `js/ui/` (`TimeMachineControl.js`, `HistoricalControl.js`, `ColorLegendControl.js`); layer switcher in `js/external/ol-layerswitcher/`; URL state via protobuf.
- **Reusable here:** map setup, layer switcher, layer-file pattern, control patterns, Rollup config (`rollup.config.js`, multiple inputs).
- **Not reusable:** everything Apple/Look Around/Flask/viewer/protobuf.
