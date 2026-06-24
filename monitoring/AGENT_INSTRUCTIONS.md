# Tourist Attractions Change-Monitoring Agent

**Repo:** `kevinelong/tourist-attractions-data`  
**Baseline file:** `monitoring/baseline_snapshot.json`  
**Purpose:** Detect stale data in the JSON attraction files before it reaches users. Each run should produce a structured diff report grouped by city covering only attractions where something has verifiably changed.

---

## Scope

Monitor these 6 cities (the most recently added batch as of June 2026):

| Key | Label | JSON file |
|-----|-------|-----------|
| `bismarck_nd` | Bismarck, ND | `bismarck_nd_attractions.json` |
| `pierre_sd`   | Pierre, SD   | `pierre_sd_attractions.json`   |
| `helena_mt`   | Helena, MT   | `helena_mt_attractions.json`   |
| `cheyenne_wy` | Cheyenne, WY | `cheyenne_wy_attractions.json` |
| `boise_id`    | Boise, ID    | `boise_id_attractions.json`    |
| `ogden_ut`    | Ogden, UT    | `ogden_ut_attractions.json`    |

---

## What to Check Per Attraction

For each attraction in `baseline_snapshot.json`, visit **two sources** in this priority order:

1. **Official website** — use the `website` field from the JSON. Navigate to the contact/visit/hours page.
2. **Google Maps** — search `"<attraction name> <city>"` on Google Maps and read the Knowledge Panel.

### Fields to compare against baseline

| Field | What to look for |
|-------|-----------------|
| `hours` | Any day's open/close time changed |
| `days_open` | Days of week added or removed |
| `admission` | Any tier price changed, free→paid or paid→free |
| `website` | URL returns 404, redirects to a different domain, or homepage text changed significantly |
| `phone` | Number changed or disconnected |

### Closure detection

Flag an attraction as **CLOSED** if any of the following are true:
- Official website returns 404 or "permanently closed" language
- Google Maps shows "Permanently closed" or "Temporarily closed"
- The attraction's page has been replaced with a different business

---

## Change Classification

Use exactly these four change types in the report:

| Type | When to use |
|------|-------------|
| `HOURS_CHANGED` | Any change to `hours` or `days_open` |
| `ADMISSION_CHANGED` | Any change to `admission` |
| `WEBSITE_CHANGED` | Dead URL, redirect to new domain, or major content change |
| `CLOSED` | Permanently or indefinitely closed |

An attraction can have multiple change types (e.g., `HOURS_CHANGED + ADMISSION_CHANGED`).

---

## Diff Report Format

Produce a Markdown report with this exact structure. Save it to:  
`monitoring/diff_report_YYYY-MM.md`  
(e.g., `monitoring/diff_report_2026-07.md`)

```markdown
# Tourist Attractions Diff Report — [MONTH YYYY]

**Generated:** [ISO date]  
**Cities scanned:** 6  
**Attractions checked:** [N]  
**Changes found:** [N]

---

## [City Label]

### [Attraction Name]
- **Change type(s):** HOURS_CHANGED | ADMISSION_CHANGED | WEBSITE_CHANGED | CLOSED
- **Source:** [Official site URL or "Google Maps"]
- **Was:** [old value from baseline]
- **Now:** [new value found]
- **JSON field to patch:** `hours` / `admission` / `website` / etc.
- **Notes:** [any additional context, e.g. "seasonal closure", "new ownership"]

---
```

If a city has no changes, write:

```markdown
## [City Label]

No changes detected.
```

---

## Baseline Update Procedure

After a human reviews and patches the JSON files, the baseline must be updated. Run this Python snippet to regenerate `baseline_snapshot.json`:

```python
import json, hashlib, os
from datetime import datetime, timezone

REPO = "/home/user/workspace/tourist-attractions-data"
CITIES = [
    ("bismarck_nd", "Bismarck, ND"),
    ("pierre_sd",   "Pierre, SD"),
    ("helena_mt",   "Helena, MT"),
    ("cheyenne_wy", "Cheyenne, WY"),
    ("boise_id",    "Boise, ID"),
    ("ogden_ut",    "Ogden, UT"),
]
TRACKED_FIELDS = ["hours", "days_open", "admission", "website", "phone"]

baseline = {
    "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "description": "Baseline snapshot of change-tracked fields for 6 cities.",
    "cities": {}
}

for key, label in CITIES:
    path = os.path.join(REPO, f"{key}_attractions.json")
    with open(path) as f:
        data = json.load(f)
    city_entry = {
        "label": label,
        "total_attractions": data["total_attractions"],
        "snapshot_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "attractions": []
    }
    for a in data["attractions"]:
        fp = {k: a.get(k, "") for k in TRACKED_FIELDS}
        fp_hash = hashlib.md5(json.dumps(fp, sort_keys=True).encode()).hexdigest()[:12]
        city_entry["attractions"].append({
            "name": a["name"], "category": a.get("category",""),
            "address": a.get("address",""), "hash": fp_hash, **fp
        })
    baseline["cities"][key] = city_entry

with open(os.path.join(REPO, "monitoring/baseline_snapshot.json"), "w") as f:
    json.dump(baseline, f, indent=2, ensure_ascii=False)
print("Baseline updated.")
```

Commit the updated `baseline_snapshot.json` to the repo after patching.

---

## Efficiency Tips

- Check 10–15 attractions per city using `wide_browse` (one entity file per city).
- Prioritize attractions with `admission` > $0 and museums/parks (most likely to change seasonally).
- Skip attractions where `website` is empty — use Google Maps only.
- If credits run low, prioritize: CLOSED detections > HOURS_CHANGED > ADMISSION_CHANGED > WEBSITE_CHANGED.

---

## Output Files to Commit

After each run, commit these to the repo:

```
monitoring/
  baseline_snapshot.json     ← updated after patches are applied
  diff_report_YYYY-MM.md     ← new file each month
  run_log.jsonl              ← append one line per run: {date, cities, checked, changed}
```

### run_log.jsonl format (one JSON object per line)

```json
{"date": "2026-07-01", "cities": 6, "attractions_checked": 521, "changes_found": 12, "report": "diff_report_2026-07.md"}
```

---

## Repo Access

```
GitHub repo:   https://github.com/kevinelong/tourist-attractions-data
Clone path:    /home/user/workspace/tourist-attractions-data/
Git push:      git pull origin main --rebase && git add monitoring/ && git commit -m "..." && git push origin main
```

Token is stored in the session context. If unavailable, check `GITHUB_TOKEN` env or prior conversation history.
