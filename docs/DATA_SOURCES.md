# DATA SOURCES (verified against `data/bhuvan_getcapabilities_1_1_1.xml`)

## Bhuvan WMS
- Endpoint: `https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms` (GeoServer, WMS 1.1.1, updateSequence 20116)
- 7,245 named layers; 7,219 queryable; **0 time dimensions**; no NDVI layers.
- GetMap formats include image/png, jpeg, gif; GetFeatureInfo: text/plain, GML, text/xml, text/html (JSON not listed in the capabilities, so test `application/json`); GetLegendGraphic: png/jpeg/gif/json.
- CRS: EPSG:4326 and 3857 supported (plus thousands more).
- Layers are vector data rendered server-side (slow when zoomed out).

| Workspace | Layers | Content |
|---|---|---|
| nuis | 2988 | Urban themes, ~153 towns |
| sisdp | 989 | Older district land cover (`*_lc`) |
| sdv | 900 | incl. slope per district |
| basemap | 705 | incl. 40 state-level `XX_LULC` layers (scale max 1.75E7) and 4 zoomed-in Gujarat layers `sisdp_gj1..4_lulc` (scale max 5E4) |
| sisdpv2 | 637 | District LULC v2 (`XX_District_lulc_v2`), shared style `sisdpv2:sisdp_lulc_v2`; 34 states/UTs; Kerala = all 14 districts |
| mmi 217, gw 179, twris 119, cadastral 81, tour 52, cleanganga 45, hs 42, hydrology 29, moef 28 ... | | |

Legend URL pattern:
`https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?request=GetLegendGraphic&version=1.1.1&format=image%2Fpng&width=20&height=20&layer=<workspace>%3A<layer>`

## NDVI (not yet sourced)
- NRSC open data archive (NOEDA) has NDVI products incl. filtered NDVI time series. Needs free login, single-user licence (no re-hosting). Attribution: "Name of the Data, National Remote Sensing Centre, ISRO, Government of India, Hyderabad, India."
- A working Bhuvan NDVI WMS/WMTS URL and token requirements are **unconfirmed**. (Earlier session noted a Reddit report that Bhuvan tokens exist but endpoint docs are hard to find.)

## Unverified / risks
- CORS behaviour of Bhuvan (tiles vs GetFeatureInfo): **untested**; this is Phase 0.
- Uptime and endpoint stability of a government server: no guarantee.
- Capture year of each layer: not published by the service.

## Catalogue quirks found in Phase 1 (verified by bounding box)
- District-layer code `CH` = **Chhattisgarh** (not Chandigarh). The state-level `CH_LULC` really is Chandigarh.
- State-level splits: `CG1`=Chhattisgarh, `RJ1`/`RJ2`=Rajasthan parts, `PY1..4`=Puducherry/Karaikal/Mahe/Yanam, `Daman`/`DIU`=Daman & Diu.
- Telangana has district layers but no state-level layer; Andaman & Nicobar and Chandigarh have state-level only.
- District names look like older boundaries (Telangana has 10 districts; Allahabad, Gurgaon, Gulbarga, Cuddapah still in use), so the data likely predates 2014-2016 redistricting. Capture year still unknown.
- Some UP names are renamed districts (e.g. Prabudhinagar, Panchshil Nagar, Kansi Ram Nagar); not mapped to current names yet.
