# Tourist Attractions Data — Agent Pipeline Playbook

This document is written for an autonomous agent executing the tourist attractions research pipeline. Read it completely before starting any work. Every section describes a real failure mode that has been encountered; follow the rules exactly.

**Repo:** `https://github.com/kevinelong/tourist-attractions-data`  
**Clone path:** `/home/user/workspace/tourist-attractions-data/`  
**Wide browse results:** `/home/user/workspace/wide/browse_results_*.csv`  
**Schema file:** `/home/user/workspace/ec_schema.json` (create if missing — see Section 3)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Completed Coverage](#2-completed-coverage)
3. [Schema & Data Contract](#3-schema--data-contract)
4. [Step 1 — Build Entity Lists](#4-step-1--build-entity-lists)
5. [Step 2 — Wide Browse (Sequential)](#5-step-2--wide-browse-sequential)
6. [Step 3 — Compile JSON Files](#6-step-3--compile-json-files)
7. [Step 4 — Zip & Push to GitHub](#7-step-4--zip--push-to-github)
8. [Step 5 — Change Monitoring](#8-step-5--change-monitoring)
9. [Credit Management](#9-credit-management)
10. [Git Workflow](#10-git-workflow)
11. [Batching Strategy](#11-batching-strategy)
12. [Planned Next Work](#12-planned-next-work)

---

## 1. Project Overview

This project builds a comprehensive JSON dataset of tourist attractions for US cities and (eventually) international destinations. Each city gets its own JSON file containing 70–130 structured attraction records covering museums, parks, restaurants, breweries, landmarks, universities, and more.

The pipeline has three main stages:
1. **Entity list** — a plain text file, one attraction name per line, for a given city
2. **Wide browse** — automated browser visits to each attraction's official site to extract structured data
3. **Compile** — a Python script that cleans the raw CSV output and writes the final JSON

The pipeline has already produced **~130 JSON files** covering the full United States. The next phase is **international destinations**.

---

## 2. Completed Coverage

### US Coverage (complete — do not re-run)

| Batch | Cities | Status |
|-------|--------|--------|
| West Coast majors | SF Bay Area, Reno, Seattle, Portland, Mammoth Lakes, New Orleans, Santa Barbara | ✅ |
| West Coast capitals + college towns | Sacramento, Salem, Olympia, Berkeley, Davis, Santa Cruz, SLO, Chico, Corvallis, Eugene, Bellingham, Pullman | ✅ |
| East Coast capitals + college towns | Boston, Cambridge MA, Providence, Hartford, Albany, New Haven, Trenton, Harrisburg, Annapolis, Dover DE, Richmond, Raleigh, Columbia SC, Augusta ME, Concord NH, Montpelier, Princeton, Ithaca, Hanover NH, Amherst MA, College Park, Charlottesville, Chapel Hill, Burlington VT, Newark DE, Durham NC | ✅ |
| East Coast metros | NYC, Philadelphia, Washington DC, Baltimore, Miami, Atlanta, Charlotte NC, Nashville, Pittsburgh, Buffalo NY, Portland ME, Savannah GA, Charleston SC, Newport RI | ✅ |
| Nevada | Las Vegas, Carson City, Henderson NV, Lake Tahoe NV | ✅ |
| Midwest capitals + college towns | Madison WI, Ann Arbor MI, Columbus OH, Indianapolis IN, Springfield IL, Iowa City IA, Minneapolis MN, Lansing MI, Lincoln NE, Lawrence KS, Bloomington IN, Columbia MO | ✅ |
| Midwest major metros | Chicago IL, Detroit MI, Cleveland OH, Milwaukee WI, Cincinnati OH, St. Louis MO, Kansas City MO, Omaha NE | ✅ |
| Texas + Oklahoma + Arkansas | Dallas TX, Houston TX, Austin TX, San Antonio TX, Oklahoma City OK, Tulsa OK, Little Rock AR, Baton Rouge LA | ✅ |
| Mountain / Southwest | Denver CO, Boulder CO, Fort Collins CO, Colorado Springs CO, Phoenix AZ, Tucson AZ, Scottsdale AZ, Albuquerque NM, Santa Fe NM, Salt Lake City UT, Provo UT | ✅ |
| South / Southeast | Memphis TN, Louisville KY, Lexington KY, Jackson MS, Des Moines IA, Knoxville TN, Chattanooga TN, Birmingham AL | ✅ |
| Great Plains + additions | Bismarck ND, Pierre SD, Topeka KS, Jefferson City MO, Helena MT, Cheyenne WY, Fargo ND, Sioux Falls SD, Rapid City SD, Boise ID, Ogden UT, Laramie WY | ✅ |

**Before adding any city, check this table. Never re-run a completed city.**

---

## 3. Schema & Data Contract

Every JSON file must conform to this schema. Never add or remove top-level fields.

### File-level wrapper
```json
{
  "title": "City, ST — Tourist Attractions",
  "generated": "2026-01-01T00:00:00Z",
  "total_attractions": 95,
  "regions_covered": ["downtown", "north side", ...],
  "attractions": [ ... ]
}
```

### Per-attraction object
```json
{
  "name":        "string — full official name",
  "category":    "string — normalized (see category list below)",
  "description": "string — 2-4 sentences, no markdown citations",
  "address":     "string — full street address",
  "city":        "string — city name only",
  "region":      "string — neighborhood or district",
  "hours":       "string — full weekly schedule",
  "days_open":   "string — days of week open",
  "admission":   "string — all price tiers, or 'Free'",
  "website":     "string — bare URL, no markdown",
  "phone":       "string",
  "image_url":   "string — direct .jpg/.jpeg/.png/.webp URL",
  "highlights":  ["string", "string", ...],
  "tips":        "string — visitor tips",
  "nearby":      "string — nearby attraction names"
}
```

### Normalized category values
Use only these values for `category`. Map any raw browser output to the closest match:

```
Aquarium, Art Gallery, Art Museum, Bar, Botanical Garden, Brewery,
Children's Museum, Civil Rights Landmark, Distillery, Entertainment,
Garden, Historic Church, Historic Site, History Museum, Landmark,
Museum, National Memorial, National Park, Nature Area, Park,
Performing Arts, Restaurant, Science Museum, Shopping, Sports Venue,
State Park, Theater, University, Winery, Zoo, Attraction
```

### Schema file (create at runtime if missing)
Write this JSON to `/home/user/workspace/ec_schema.json` before running wide browse:

```json
{
  "type": "object",
  "properties": {
    "name":        {"type": "string", "title": "Name"},
    "category":    {"type": "string", "title": "Category"},
    "description": {"type": "string", "title": "Description"},
    "address":     {"type": "string", "title": "Address"},
    "city":        {"type": "string", "title": "City"},
    "region":      {"type": "string", "title": "Region"},
    "hours":       {"type": "string", "title": "Hours"},
    "days_open":   {"type": "string", "title": "Days Open"},
    "admission":   {"type": "string", "title": "Admission"},
    "website":     {"type": "string", "title": "Website"},
    "phone":       {"type": "string", "title": "Phone"},
    "image_url":   {"type": "string", "title": "Image URL"},
    "highlights":  {"type": "array", "items": {"type": "string"}, "title": "Highlights"},
    "tips":        {"type": "string", "title": "Tips"},
    "nearby":      {"type": "string", "title": "Nearby"}
  }
}
```

---

## 4. Step 1 — Build Entity Lists

An entity list is a plain text file with one attraction name per line. It is the input to `wide_browse`.

### File naming convention
```
/home/user/workspace/{city_key}_entities.txt
```
Examples: `boise_id_entities.txt`, `toronto_on_entities.txt`

### Target size
- **80–100 lines** per city. Never exceed 128 (hard limit for `wide_browse`).
- If you write more than 128 lines, trim before browsing: `head -128 file.txt > file_trim.txt`

### What to include
Write attraction names as a person would type them into Google Maps — specific enough to find the right place, not so long that searches fail:

```
Idaho State Capitol Building
Boise Art Museum
Old Idaho Penitentiary State Historic Site
Zoo Boise
Julia Davis Park
Boise River Greenbelt
Basque Museum and Cultural Center
Discovery Center of Idaho
World Center for Birds of Prey
Bogus Basin Mountain Recreation Area
```

### Good entity diversity for a city
Cover all of these categories proportionally:
- **Landmarks & government buildings** (5–8): capitol, city hall, historic districts
- **Museums** (10–15): history, art, science, specialty
- **Parks & nature** (10–15): state parks, trails, gardens, wildlife areas
- **Breweries & distilleries** (5–8): local craft producers
- **Restaurants & food** (5–8): notable/iconic local spots
- **Entertainment & arts** (5–8): theaters, music venues, arenas
- **Universities** (2–4): main campus and notable buildings
- **Shopping & markets** (3–5): farmers markets, notable districts
- **Nearby day trips** (5–10): attractions within ~60 miles

### What NOT to include
- National chains (McDonald's, Starbucks, Holiday Inn)
- Generic terms ("downtown area", "city parks")
- Places already covered in a nearby city's file
- Anything you are not confident exists

---

## 5. Step 2 — Wide Browse (Sequential)

`wide_browse` visits each entity in the list and extracts structured data. **This is the most important constraint in the entire pipeline:**

### ⚠️ CRITICAL: wide_browse is NOT concurrency-safe

**Run exactly one city at a time. Never run two `wide_browse` calls simultaneously.** The CSV output files will collide and data will be lost. Wait for each call to return before starting the next.

### Standard wide browse call

```python
wide_browse(
    entities_file="/home/user/workspace/{city_key}_entities.txt",
    prompt_template="Search for {entity} in the [CITY NAME] area and visit its official website or best available page. Extract: full official name, category (e.g. Museum, Park, Restaurant, Bar, Brewery, University, Entertainment, Landmark, etc.), 2-4 sentence description, full street address, city, neighborhood/region, hours of operation (full weekly schedule), days open, admission/ticket prices (all tiers; Free if free), official website URL (plain, no markdown), phone number, a direct image URL ending in .jpg/.jpeg/.png/.webp from official site or Wikipedia, 4-6 highlights as a list, visitor tips, nearby attractions.",
    output_schema_file="/home/user/workspace/ec_schema.json"
)
```

Replace `[CITY NAME]` with the actual city and state (e.g., "Toronto, Ontario, Canada").

### Recording the CSV path
The return value contains `file_path` — the path to the CSV output, always under `wide/browse_results_*.csv`. **Write this down immediately.** You need it for the compile step.

```
Example return: {"file_path": "wide/browse_results_mpnf8jj8.csv", "total_entities": 90, "successful": 90, ...}
```

### Handling partial results (credit exhaustion)
If `wide_browse` returns fewer successful rows than entities (due to credit exhaustion), do NOT discard partial results. Follow this retry pattern:

1. Read the CSV to find which entities were successfully processed
2. Build a retry file with only the missing entities
3. Run `wide_browse` again on the retry file
4. When compiling, pass **both** CSVs to the compile script using the `"csvs": [list]` key

```python
# Example: find missing entities after a partial run
import csv

completed = set()
with open("/home/user/workspace/wide/browse_results_PARTIAL.csv") as f:
    for row in csv.DictReader(f):
        completed.add(row.get("entity", "").strip())

with open("/home/user/workspace/boise_id_entities.txt") as f:
    all_entities = [line.strip() for line in f if line.strip()]

missing = [e for e in all_entities if e not in completed]

with open("/home/user/workspace/boise_id_retry.txt", "w") as f:
    f.write("\n".join(missing))
```

### Credit exhaustion recovery
If a wide browse call returns 0 results with "Insufficient credits" in the error list:
- **Wait 5 minutes** before retrying (credits restore on a rolling basis)
- Retry the exact same entity file
- Do not modify the entity file or schema between retries

---

## 6. Step 3 — Compile JSON Files

After wide browse completes, run the compile script to clean raw CSV data into final JSON.

### Reference implementation
The full, working compile script is at: `/home/user/workspace/compile_batch6.py`  
Copy it and adapt the `CITIES` list for your new cities. Do not rewrite the helper functions — they are battle-tested.

### Key helper functions (must preserve exactly)

**`clean_url(raw)`** — Strips markdown link syntax `[label](url)` and returns a bare URL. Wide browse often injects citation markdown into URL fields; this removes it.

**`clean_text(raw)`** — Strips all `[label](url)` citation markdown from text fields. Every text field must be run through this before writing to JSON.

**`safe_parse_list(raw)`** — Parses the `highlights` field, which may arrive as a JSON array string, newline-separated text, pipe-separated text, or a bare string. Returns a clean Python list.

**`normalize_category(raw)`** — Maps raw category strings (which may include citations and subcategories) to the normalized category list. Uses substring matching.

**`is_bad(text)`** — Returns True if a text field contains error phrases like "not found", "unable to find", "n/a". Used to filter out failed browse results.

### CITIES config block
Each city entry in the `CITIES` list looks like this:

```python
{
    "key": "toronto_on",
    "title": "Toronto, ON — Tourist Attractions",
    "region_keywords": ["toronto", "downtown toronto", "north york", "scarborough",
                        "etobicoke", "york", "east end", "west end"],
    "csvs": ["wide/browse_results_XXXXXXXX.csv"],
    # If retry was needed, add both:
    # "csvs": ["wide/browse_results_FIRST.csv", "wide/browse_results_RETRY.csv"],
}
```

`region_keywords` drives the sort order — attractions whose `region` or `city` field contains an early keyword are sorted first. Put the most central/important areas first.

### Deduplication
The compile script deduplicates by `name.lower().strip()`. If the same attraction appears in two CSVs (first pass + retry), only the first occurrence is kept. This is intentional — the first pass usually has better data.

### Output location
Always write compiled JSON to:
```
/home/user/workspace/tourist-attractions-data/{city_key}_attractions.json
```

### Target count
- Aim for **75–110 attractions** per city after deduplication and filtering
- If a city produces fewer than 60, consider expanding the entity list and re-running
- Capitals and small cities (population < 100k) may legitimately produce 60–80

---

## 7. Step 4 — Zip & Push to GitHub

### Naming convention for zip files
Group related cities into one zip per batch:
```
{descriptive_group}_attractions.zip
```
Examples:
- `canada_attractions.zip`
- `mexico_attractions.zip`
- `western_europe_attractions.zip`

### Push sequence (always in this order)
```bash
cd /home/user/workspace/tourist-attractions-data

# 1. Pull latest before touching anything
git pull origin main --rebase

# 2. Copy new files (already written to repo dir by compile script)
# (no copy needed if compile script wrote directly to repo dir)

# 3. Stage new JSON and zip files
git add *_attractions.json *.zip

# 4. Commit with a descriptive message including city count and total attractions
git commit -m "Add [batch name]: [N] cities, [N] attractions ([City1], [City2], ...)"

# 5. Push
git push origin main
```

### GitHub authentication
Token must be embedded in the remote URL:
```bash
git remote set-url origin https://kevinelong:{TOKEN}@github.com/kevinelong/tourist-attractions-data.git
```
The token expires periodically. If push fails with "Authentication failed", a new token is needed from the repo owner. Token needs `repo` scope.

### After every push, verify
```bash
git log --oneline -3
```
Confirm your commit appears at the top.

---

## 8. Step 5 — Change Monitoring

A separate monitoring workflow exists for keeping existing data fresh. See:
```
monitoring/AGENT_INSTRUCTIONS.md
monitoring/baseline_snapshot.json
```

The baseline captures `hours`, `days_open`, `admission`, `website`, and `phone` for the 6 most recently added cities. When running a monitoring pass:

1. For each attraction, visit its `website` and/or search Google Maps
2. Compare each field to the baseline value
3. If different, record a `HOURS_CHANGED`, `ADMISSION_CHANGED`, `WEBSITE_CHANGED`, or `CLOSED` event
4. Write the diff report to `monitoring/diff_report_YYYY-MM.md`
5. Append one line to `monitoring/run_log.jsonl`
6. Push all three files: updated `baseline_snapshot.json` + new diff report + updated `run_log.jsonl`

---

## 9. Credit Management

Wide browse is the most credit-intensive operation. Follow these rules to avoid waste:

### Hard limits
- **128 entities maximum** per `wide_browse` call. Trim files over 128 with `head -128`.
- Never run `wide_browse` in parallel. Serialize all calls.

### Batch sizing
- 80–100 entities per city is the sweet spot — enough for a rich dataset, not so many that credit hits are frequent
- For large metros (NYC, London, Paris, Tokyo), consider 2 passes of 100 each using different entity categories

### When credits run out mid-browse
Do NOT restart from scratch. The partial CSV is valuable. Follow the retry pattern in Section 5.

### Cost awareness by step
| Step | Relative cost |
|------|---------------|
| Build entity list | Near zero |
| Wide browse (per city) | High |
| Compile script | Near zero |
| Git push | Near zero |
| Monitoring scan (per city) | Medium |

---

## 10. Git Workflow

### Repository layout
```
tourist-attractions-data/
├── {city_key}_attractions.json    ← one per city, ~75-110 attractions
├── {batch_name}_attractions.zip   ← one per batch grouping
├── README.md                      ← auto-updated table of contents
├── PIPELINE_PLAYBOOK.md           ← this file
├── compile_template.py            ← reusable compile script
├── monitoring/
│   ├── AGENT_INSTRUCTIONS.md      ← change-monitoring task spec
│   ├── baseline_snapshot.json     ← field fingerprints for monitored cities
│   ├── diff_report_YYYY-MM.md     ← monthly change reports
│   └── run_log.jsonl              ← monitoring run history
└── food_and_events/               ← separate pipeline (restaurants/events)
```

### Commit message format
```
[Action] [batch/scope]: [N] cities, [N] attractions ([City1], [City2], ...)

Examples:
Add Batch 7 — Canada: 5 cities, 487 attractions (Toronto, Vancouver, Montreal, Calgary, Ottawa)
Add monitoring diff report 2026-07: 14 changes across 6 cities
Update baseline_snapshot.json after July 2026 patches
```

### Never commit
- Raw entity `.txt` files (they stay in `/home/user/workspace/`, not the repo)
- Compile Python scripts (they stay in `/home/user/workspace/`)
- Wide browse CSV files (`wide/browse_results_*.csv`)
- Any file over 10MB

---

## 11. Batching Strategy

### Choosing which cities to add next

**Priority order for next batches:**
1. **International — Canada** (highest value, large US travel audience): Vancouver, Victoria, Toronto, Ottawa, Montreal, Quebec City, Calgary, Edmonton, Winnipeg, Halifax
2. **International — Mexico** (popular US destination): Mexico City, Cancun, Puerto Vallarta, San Miguel de Allende, Oaxaca City, Guadalajara, Cabo San Lucas, Playa del Carmen
3. **International — Caribbean** (popular US destination): Nassau, Havana, San Juan PR, Montego Bay, Bridgetown, Punta Cana
4. **International — Western Europe**: London, Paris, Amsterdam, Rome, Barcelona, Berlin, Vienna, Prague, Lisbon, Dublin
5. **International — Other** (Mexico/Canada/Europe exhaust first): Tokyo, Bangkok, Sydney, etc.

### Batch size guidance
- **6–12 cities per batch** is optimal. Fewer = more pushes without benefit. More = higher risk of credit exhaustion mid-batch.
- Group cities **geographically or thematically** so the zip file name is meaningful.
- Keep batches under 1,000 total entity rows (sum of all entity files in the batch).

### International entity list tips
For international cities, include:
- English-language names where they exist ("Eiffel Tower", not "Tour Eiffel")
- Neighborhood names in local language are fine (they improve Google search results)
- Include the country or city in the entity name when there's ambiguity: "Louvre Museum Paris", not just "Louvre Museum"
- Include currency and language context in the browse prompt (add "Prices may be in [currency]" to the prompt template)

### International prompt template adjustment
Add a localization note to the standard prompt:
```
"...admission/ticket prices (all tiers; Free if free; include currency symbol), official website URL..."
```

---

## 12. Planned Next Work

In priority order:

### Phase 1 — Canada (next)
**Target cities:** Vancouver BC, Victoria BC, Toronto ON, Ottawa ON, Montreal QC, Quebec City QC, Calgary AB, Edmonton AB, Winnipeg MB, Halifax NS  
**Zip name:** `canada_attractions.zip`  
**Notes:** Include both English and French names in entity lists for Quebec cities. French attraction names often search better on Google Maps.

### Phase 2 — Mexico
**Target cities:** Mexico City, Guadalajara, Monterrey, Cancun/Riviera Maya, Puerto Vallarta, Oaxaca City, San Miguel de Allende, Cabo San Lucas  
**Zip name:** `mexico_attractions.zip`  
**Notes:** Use English names in entity lists (most major attractions have widely-used English names). Include "Mexico" or city name to disambiguate from US cities.

### Phase 3 — Caribbean
**Target cities:** San Juan PR (US territory), Nassau Bahamas, Havana Cuba, Montego Bay Jamaica, Punta Cana Dominican Republic, Bridgetown Barbados, Charlotte Amalie USVI  
**Zip name:** `caribbean_attractions.zip`

### Phase 4 — Western Europe
**Target cities:** London, Paris, Amsterdam, Rome, Barcelona, Berlin, Vienna, Prague, Lisbon, Dublin  
**Zip name:** `western_europe_attractions.zip`  
**Notes:** These cities have thousands of attractions — be selective. Focus on UNESCO sites, world-famous museums, iconic landmarks, popular neighborhoods. Avoid generic tourist traps.

### Phase 5 — Change Monitoring
Run the monitoring workflow (see `monitoring/AGENT_INSTRUCTIONS.md`) after each international batch is added to keep the full dataset fresh.

---

## Quick Reference

| Task | Command/Location |
|------|-----------------|
| Schema file | `/home/user/workspace/ec_schema.json` |
| Entity files | `/home/user/workspace/{city_key}_entities.txt` |
| CSV output dir | `/home/user/workspace/wide/` |
| Compiled JSON dir | `/home/user/workspace/tourist-attractions-data/` |
| Compile template | `/home/user/workspace/tourist-attractions-data/compile_template.py` |
| Monitoring instructions | `monitoring/AGENT_INSTRUCTIONS.md` |
| Baseline snapshot | `monitoring/baseline_snapshot.json` |
| Max entities per wide_browse | **128** |
| Concurrency rule | **One wide_browse at a time — never parallel** |
| Credit recovery | Wait 5 min, retry same file |
| Git auth | Token in remote URL, `repo` scope required |
