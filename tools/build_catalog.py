#!/usr/bin/env python3
"""Build data/catalog.json from the saved Bhuvan WMS GetCapabilities file.

Usage (from repo root):  python3 tools/build_catalog.py
Standard library only. Real layer names are NEVER altered; only display names are tidied.

Schema (v2):
  states[]: {code, name, state_layers[], districts[]}
    state_layers[]: {layer, label, bbox, queryable, scale_hint_max}   (>=1 when state-level data exists)
    districts[]:    {layer, display, bbox, queryable}
"""
import json, re, sys, collections
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "bhuvan_getcapabilities_1_1_1.xml"
OUT = ROOT / "data" / "catalog.json"
REPORT = ROOT / "data" / "catalog_report.txt"
WMS = "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms"

# Canonical codes used by this catalogue (the service itself is inconsistent).
STATES = {
 "AN":"Andaman & Nicobar Islands","AP":"Andhra Pradesh","AR":"Arunachal Pradesh","AS":"Assam",
 "BR":"Bihar","CG":"Chhattisgarh","CH":"Chandigarh","DD":"Daman & Diu","DL":"Delhi",
 "DN":"Dadra & Nagar Haveli","GA":"Goa","GJ":"Gujarat","HP":"Himachal Pradesh",
 "HR":"Haryana","JH":"Jharkhand","JK":"Jammu & Kashmir","KA":"Karnataka","KL":"Kerala",
 "LD":"Lakshadweep","MH":"Maharashtra","ML":"Meghalaya","MN":"Manipur","MP":"Madhya Pradesh",
 "MZ":"Mizoram","NL":"Nagaland","OR":"Odisha","PB":"Punjab","PY":"Puducherry",
 "RJ":"Rajasthan","SK":"Sikkim","TN":"Tamil Nadu","TR":"Tripura","TS":"Telangana",
 "UK":"Uttarakhand","UP":"Uttar Pradesh","WB":"West Bengal",
}

# District layers (workspace sisdpv2): the service's "CH" prefix is Chhattisgarh (verified by bbox),
# not Chandigarh.
DISTRICT_CODE_MAP = {"CH": "CG"}

# State-level layers (workspace basemap): service name -> (canonical state, label).
# Verified by bounding box. Plain "CH_LULC" really is Chandigarh.
BASEMAP_MAP = {
 "CG1": ("CG", None), "DIU": ("DD", "Diu"), "Daman": ("DD", "Daman"),
 "PY1": ("PY", "Puducherry"), "PY2": ("PY", "Karaikal"), "PY3": ("PY", "Mahe"), "PY4": ("PY", "Yanam"),
 "RJ1": ("RJ", "Part 1"), "RJ2": ("RJ", "Part 2"),
}

# Display-name spelling fixes. Key = name as auto-prettified from the service; value = shown to users.
NAME_FIXES = {
 "Alapurza":"Alappuzha","Errnakulam":"Ernakulam","Kasargod":"Kasaragod","Kozhikkode":"Kozhikode",
 "Banglore":"Bengaluru Urban","Banglore Rural":"Bengaluru Rural","Gulberga":"Gulbarga",
 "Aizwal":"Aizawl","Champai":"Champhai","Lawngtalai":"Lawngtlai","Sahia":"Saiha","Serchip":"Serchhip",
 "Baska":"Baksa","Fatehbad":"Fatehabad","Bageshwer":"Bageshwar","Bardhman":"Barddhaman",
 "East Maedinipur":"East Medinipur","West Medinipur":"West Medinipur","Muzzafarnagar":"Muzaffarnagar",
 "Sbs Nagar":"SBS Nagar","Anugul":"Angul","Baudh":"Boudh","Debagarh":"Deogarh","Jajapur":"Jajpur",
 "Gariabandh":"Gariaband","Bemetra":"Bemetara","Balodbajar":"Balodabazar","Shopain":"Shopian",
 "Ahmadabad":"Ahmedabad","Bara Banki":"Barabanki","Rae Bareli":"Raebareli","Chittaurgarh":"Chittorgarh",
 "Agar Melwa":"Agar Malwa","Coochbihar":"Cooch Behar","Taran Taran":"Tarn Taran",
 "Dadra Nagar Haveli":"Dadra & Nagar Haveli","Pondicherry":"Puducherry",
}

def pretty(token):
    return re.sub(r"_+", " ", token).strip().title()

def bbox(l):
    b = l.find("LatLonBoundingBox")
    if b is None: return None
    return [round(float(b.get(k)), 5) for k in ("minx", "miny", "maxx", "maxy")]

def main():
    root = ET.parse(SRC).getroot()
    states = collections.OrderedDict()
    def st_for(code):
        return states.setdefault(code, {"code": code, "name": STATES[code], "state_layers": [], "districts": []})

    for l in root.iter("Layer"):
        n = l.find("Name")
        if n is None: continue
        name = n.text
        if name.startswith("sisdpv2:") and name.endswith("_lulc_v2") and not name.startswith("sisdpv2:sisdp_"):
            raw_code, rest = name.split(":", 1)[1].split("_", 1)
            code = DISTRICT_CODE_MAP.get(raw_code, raw_code)
            stem = pretty(rest[:-len("_lulc_v2")])
            st_for(code)["districts"].append({"layer": name, "display": NAME_FIXES.get(stem, stem),
                "bbox": bbox(l), "queryable": l.get("queryable") == "1"})
        elif name.startswith("basemap:") and name.endswith("_LULC"):
            raw = name.split(":", 1)[1][:-len("_LULC")]
            code, label = BASEMAP_MAP.get(raw, (raw, None))
            sh = l.find("ScaleHint")
            st_for(code)["state_layers"].append({"layer": name, "label": label, "bbox": bbox(l),
                "queryable": l.get("queryable") == "1",
                "scale_hint_max": float(sh.get("max")) if sh is not None else None})

    for st in states.values():
        st["districts"].sort(key=lambda d: d["display"])
        st["state_layers"].sort(key=lambda s: s["layer"])

    # ---- validation ----
    problems = []
    for code in states:
        if code not in STATES: problems.append(f"unknown state code {code}")
    for st in states.values():
        names = [d["display"] for d in st["districts"]]
        dup = [k for k, v in collections.Counter(names).items() if v > 1]
        if dup: problems.append(f"{st['code']}: duplicate display names {dup}")
        for d in st["districts"]:
            if not d["bbox"]: problems.append(f"{d['layer']}: no bbox")
        if not st["districts"] and not st["state_layers"]:
            problems.append(f"{st['code']}: empty")

    nd = sum(len(s["districts"]) for s in states.values())
    nonq = [d["layer"] for s in states.values() for d in s["districts"] if not d["queryable"]]
    catalog = {
        "schema_version": 2,
        "generated_from": SRC.name, "wms_url": WMS, "wms_version": "1.1.1",
        "district_style": "sisdpv2:sisdp_lulc_v2",
        "legend_url_template": WMS + "?request=GetLegendGraphic&version=1.1.1&format=image%2Fpng&width=20&height=20&layer={layer}",
        "attribution": "Bhuvan, National Remote Sensing Centre, ISRO, Government of India",
        "vintage_note": "The WMS publishes no time dimension; capture year is unknown. District names suggest older boundaries (e.g. Telangana shows 10 districts).",
        "states": sorted(states.values(), key=lambda s: s["name"]),
    }
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=1))

    lines = [f"states/UTs: {len(states)}", f"district layers: {nd}",
             f"state-level layers: {sum(len(s['state_layers']) for s in states.values())}",
             f"states with districts but no state-level layer: {[s['code'] for s in states.values() if s['districts'] and not s['state_layers']]}",
             f"states with state-level only: {[s['code'] for s in states.values() if not s['districts']]}",
             f"non-queryable district layers: {nonq}", f"problems: {problems or 'none'}"]
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
