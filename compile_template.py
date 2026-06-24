#!/usr/bin/env python3
"""
compile_template.py — Tourist Attractions Pipeline: Reusable Compile Script
===========================================================================
Copy this file to a new name (e.g. compile_canada.py), fill in the CITIES list,
and run it to produce individual JSON attraction files from wide_browse CSV output.

USAGE
-----
1. Run wide_browse for each city; note the CSV suffix (last 8 chars of filename).
2. Copy and rename this file:  cp compile_template.py compile_<batchname>.py
3. Fill in CITIES below — one dict per city.
4. Run:  python3 compile_<batchname>.py
5. Verify output, then zip and push to GitHub per PIPELINE_PLAYBOOK.md §5.

NEVER commit this script or entity .txt files to the repo.
Only compiled JSON files and zip archives go to GitHub.
"""

import csv, json, re, os
from datetime import datetime

# ---------------------------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------------------------

def clean_url(raw):
    """Extract the first clean HTTP(S) URL from a possibly markdown-annotated string."""
    if not raw: return ""
    # markdown link: [label](url)
    m = re.search(r'\(https?://[^\s\)]+\)', raw)
    if m: return m.group(0)[1:-1]
    # bare URL
    m = re.search(r'https?://[^\s\)\],"\']+', raw)
    if m: return m.group(0).rstrip('.,;)')
    return raw.strip()

def clean_text(raw):
    """Strip markdown link syntax injected by wide_browse, collapse whitespace."""
    if not raw: return ""
    cleaned = re.sub(r'\[([^\]]+)\]\(https?://[^\)]+\)', r'\1', raw)
    return re.sub(r'\s+', ' ', cleaned).strip()

def safe_parse_list(raw):
    """Parse highlights / tips field into a clean Python list.

    Accepts: JSON array strings, newline-separated, pipe-separated, semicolon-separated,
    or a plain string (returned as a single-item list).
    """
    if not raw: return []
    if isinstance(raw, list): return [clean_text(h) for h in raw if h]
    stripped = raw.strip()
    if stripped.startswith('['):
        try:
            items = json.loads(stripped)
            return [clean_text(str(h)) for h in items if h]
        except Exception:
            pass
    for delim in ['\n', '|', ';']:
        if delim in stripped:
            parts = [p.strip() for p in stripped.split(delim) if p.strip()]
            if len(parts) > 1:
                return [clean_text(p) for p in parts]
    return [clean_text(stripped)] if stripped else []

# ---------------------------------------------------------------------------
# CATEGORY NORMALISATION
# ---------------------------------------------------------------------------

CATEGORY_MAP = {
    'aquarium':       'Aquarium',
    'art gallery':    'Art Gallery',
    'art museum':     'Art Museum',
    'bar':            'Bar',
    'botanical':      'Botanical Garden',
    'brewery':        'Brewery',
    'children':       "Children's Museum",
    'church':         'Historic Church',
    'civil rights':   'Civil Rights Landmark',
    'college':        'University',
    'distillery':     'Distillery',
    'entertainment':  'Entertainment',
    'garden':         'Garden',
    'historic':       'Historic Site',
    'history museum': 'History Museum',
    'landmark':       'Landmark',
    'museum':         'Museum',
    'nature':         'Nature Area',
    'national park':  'National Park',
    'national memorial': 'National Memorial',
    'park':           'Park',
    'performing arts':'Performing Arts',
    'restaurant':     'Restaurant',
    'science':        'Science Museum',
    'shopping':       'Shopping',
    'sports':         'Sports Venue',
    'state park':     'State Park',
    'theater':        'Theater',
    'university':     'University',
    'winery':         'Winery',
    'zoo':            'Zoo',
}

def normalize_category(raw):
    """Map free-form category text to a canonical label."""
    if not raw: return "Attraction"
    t = clean_text(raw).lower()
    for key, val in CATEGORY_MAP.items():
        if key in t:
            return val
    first = re.split(r'[,/&]', clean_text(raw))[0].strip()
    return first.title() if first else "Attraction"

# ---------------------------------------------------------------------------
# BAD-ENTRY FILTER
# ---------------------------------------------------------------------------

BAD_PHRASES = [
    'no information', 'not found', 'does not exist', 'unable to find',
    'cannot find', 'no results', 'page not found', 'error', 'n/a',
    'no data', 'coming soon', 'under construction',
]

def is_bad(text):
    """Return True if the text is a browse-failure placeholder."""
    if not text: return True
    t = text.lower()
    return any(p in t for p in BAD_PHRASES)

# ---------------------------------------------------------------------------
# CSV → DICT HELPERS
# ---------------------------------------------------------------------------

# Accepts both snake_case and Title Case column headers from wide_browse CSVs.
COL_MAP = {
    'name':        ['Name',        'name'],
    'category':    ['Category',    'category'],
    'description': ['Description', 'description'],
    'address':     ['Address',     'address'],
    'city':        ['City',        'city'],
    'region':      ['Region',      'region'],
    'hours':       ['Hours',       'hours'],
    'days_open':   ['Days Open',   'days_open'],
    'admission':   ['Admission',   'admission'],
    'website':     ['Website',     'website'],
    'phone':       ['Phone',       'phone'],
    'image_url':   ['Image URL',   'image_url'],
    'highlights':  ['Highlights',  'highlights'],
    'tips':        ['Tips',        'tips'],
    'nearby':      ['Nearby',      'nearby'],
}

def get_field(row, field):
    for col in COL_MAP.get(field, []):
        if col in row:
            return row[col]
    return ''

def read_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows

def build_attraction(row):
    """Convert a CSV row into a clean attraction dict; return None to skip bad rows."""
    name = clean_text(get_field(row, 'name'))
    if not name or is_bad(name):
        return None
    desc = clean_text(get_field(row, 'description'))
    if is_bad(desc):
        return None
    return {
        'name':        name,
        'category':    normalize_category(get_field(row, 'category')),
        'description': desc,
        'address':     clean_text(get_field(row, 'address')),
        'city':        clean_text(get_field(row, 'city')),
        'region':      clean_text(get_field(row, 'region')),
        'hours':       clean_text(get_field(row, 'hours')),
        'days_open':   clean_text(get_field(row, 'days_open')),
        'admission':   clean_text(get_field(row, 'admission')),
        'website':     clean_url(get_field(row, 'website')),
        'phone':       clean_text(get_field(row, 'phone')),
        'image_url':   clean_url(get_field(row, 'image_url')),
        'highlights':  safe_parse_list(get_field(row, 'highlights')),
        'tips':        clean_text(get_field(row, 'tips')),
        'nearby':      clean_text(get_field(row, 'nearby')),
    }

# ---------------------------------------------------------------------------
# CITIES CONFIG  ← EDIT THIS SECTION FOR EACH BATCH
# ---------------------------------------------------------------------------
# Each entry needs:
#   key             — output filename stem  (e.g. "vancouver_bc")
#   title           — human title for the JSON envelope
#   region_keywords — ordered list used for sort priority (most central first)
#   csvs            — list of CSV path(s) relative to /home/user/workspace/
#                     Multiple CSVs are merged (used when a city needed a retry pass)
#
# EXAMPLE (replace with real cities and CSV suffixes):
CITIES = [
    # {
    #     "key": "vancouver_bc",
    #     "title": "Vancouver, BC — Tourist Attractions",
    #     "region_keywords": [
    #         "vancouver", "downtown vancouver", "gastown", "granville island",
    #         "kitsilano", "stanley park", "north vancouver", "burnaby", "richmond",
    #         "surrey", "coquitlam", "new westminster"
    #     ],
    #     "csvs": ["wide/browse_results_XXXXXXXX.csv"],
    # },
    # {
    #     "key": "victoria_bc",
    #     "title": "Victoria, BC — Tourist Attractions",
    #     "region_keywords": [
    #         "victoria", "inner harbour", "james bay", "oak bay", "saanich",
    #         "esquimalt", "langford", "sidney", "sooke", "cowichan"
    #     ],
    #     "csvs": ["wide/browse_results_YYYYYYYY.csv"],
    # },
]

# ---------------------------------------------------------------------------
# OUTPUT DIRECTORY  ← change if needed
# ---------------------------------------------------------------------------
OUT_DIR = "/home/user/workspace/tourist-attractions-data"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# MAIN COMPILE LOOP  — no changes needed below this line
# ---------------------------------------------------------------------------

total_all = 0

for city in CITIES:
    # 1. Load all CSV rows for this city (merges retry CSVs automatically)
    rows = []
    for csv_rel in city["csvs"]:
        csv_path = os.path.join("/home/user/workspace", csv_rel)
        rows.extend(read_csv(csv_path))

    # 2. Build + deduplicate attractions
    seen = set()
    attractions = []
    for row in rows:
        attr = build_attraction(row)
        if attr is None:
            continue
        key = attr['name'].lower().strip()
        if key in seen:
            continue
        seen.add(key)
        attractions.append(attr)

    # 3. Sort: primary region keywords first, then alphabetical within group
    region_order = city["region_keywords"]

    def sort_key(a):
        r = a.get('region', '').lower()
        c = a.get('city', '').lower()
        n = a.get('name', '').lower()
        for i, kw in enumerate(region_order):
            if kw in r or kw in c:
                return (i, n)
        return (len(region_order), n)

    attractions.sort(key=sort_key)

    # 4. Build output envelope
    output = {
        "title":             city["title"],
        "generated":         datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_attractions": len(attractions),
        "regions_covered":   city["region_keywords"][:8],
        "attractions":       attractions,
    }

    # 5. Write JSON file
    out_file = os.path.join(OUT_DIR, f"{city['key']}_attractions.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  {city['key']:30s}  →  {len(attractions):3d} attractions  →  {out_file}")
    total_all += len(attractions)

print(f"\nTotal attractions compiled: {total_all}")
print("Next steps:")
print("  1. Review spot-check a few JSON files")
print("  2. Zip the new files:  zip -j <batch>_attractions.zip tourist-attractions-data/*_attractions.json")
print("  3. Push to GitHub per PIPELINE_PLAYBOOK.md §5 (Git Push Procedure)")
