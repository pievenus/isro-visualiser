# ISRO Data Visualiser

A static web map for exploring ISRO / NRSC (Bhuvan) open geospatial data, one module at a time.
Built on the OpenLayers map code of [sk-zk/lookaround-map](https://github.com/sk-zk/lookaround-map) (MIT), but **standalone**: no Flask/Look Around backend, so it can be hosted on GitHub Pages.

**Status:** Planning + data catalogue done. No UI code written yet. See `docs/HANDOFF.md`.

## If you are an AI agent or a new session: read these first, in order
1. `docs/HANDOFF.md`: current state, next step, how the owner works
2. `docs/PLAN.md`: module roadmap and phases
3. `docs/DECISIONS.md`: what was decided and why (don't relitigate)
4. `docs/DATA_SOURCES.md`: verified facts about the Bhuvan WMS
5. `docs/SESSION_LOG.md`: chronological log

## Layout
```
data/bhuvan_getcapabilities_1_1_1.xml   raw WMS capabilities (8 MB, source of truth)
data/catalog.json                       generated: state > district LULC layers
tools/build_catalog.py                  regenerates catalog.json (stdlib Python)
upstream/lookaround-map/                unmodified reference copy of the upstream project
docs/                                   handoff, plan, decisions, sources, log
```

## Attribution
Data: "Bhuvan, National Remote Sensing Centre, ISRO, Government of India". Upstream code: MIT, (c) 2022 skzk.
