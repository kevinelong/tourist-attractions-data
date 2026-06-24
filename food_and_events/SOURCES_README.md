# Agent-Friendly Source Registry

**File:** `sources.json`
**Schema version:** 1.0
**Purpose:** Pre-vetted list of restaurant-opening trackers and dated/ticketed event calendars across 21 US metros + 12 national aggregators, with per-source agent-compatibility data so future research runs can skip the discovery + probing step.

## Structure

```
{
  "schema_version", "title", "description", "generated_at",
  "summary_stats": { total_sources, reachable_via_http, rss_feeds_detected, ... },
  "agent_compatibility_legend": { excellent, good, fair, blocked, ... },
  "recommended_methods_legend":  { rss_feed, http_fetch_or_browser, ... },
  "tiers": {
    "national_aggregator": {
      "restaurant_openings": [ <source>, ... ],
      "events_calendar":     [ <source>, ... ]
    },
    "west_coast_mega": {
      "Los Angeles":   { "restaurant_openings": [...], "events_calendar": [...] },
      "San Francisco": { ... },
      ...
    },
    "east_coast_mega": { ... },
    "in_between_mega": { ... }
  }
}
```

## Per-source record

Every source has:

| Field | Purpose |
|---|---|
| `name`, `url`, `publisher` | Identification |
| `content_type` | `restaurant_openings` or `events_calendar` |
| `status.http_status`, `status.reachable`, `status.probed_at` | Most recent probe result |
| `agent_compatibility.rating` | `excellent`/`good`/`fair`/`blocked`/`url_invalid`/`rate_limited` |
| `agent_compatibility.recommended_method` | How a future agent should access this source |
| `agent_compatibility.notes` | Human-readable caveats |
| `ancillary.rss_url` | If present, prefer this over HTML scraping |
| `ancillary.has_jsonld`, `has_schema_event`, `has_schema_restaurant` | Structured-data signals |
| `ancillary.js_framework` | Next.js / React / Nuxt.js / WordPress / Drupal — implies whether plain HTTP works |
| `ancillary.robots_pplx_allowed`, `robots_generic_allowed`, `robots_gptbot_allowed` | robots.txt disposition |
| `ancillary.page_size_kb`, `server`, `content_type_header` | Performance and infra hints |

## How to use this in an agent run

1. **Pick a city.** Look up `tiers.<tier>.<City>`.
2. **Filter by rating.** Start with `rating == "excellent"` (RSS) — those are zero-cost.
3. **Group by `recommended_method`.** For each method:
   - `rss_feed` → fetch `ancillary.rss_url`, parse XML.
   - `http_fetch_or_browser` → `fetch_url` first; only escalate to `browser_task` if content is empty.
   - `browser_task (JS-rendered)` → go straight to browser automation.
   - `browser_task (Cloudflare/anti-bot 403)` → real browser session required.
   - `browser_task (robots.txt disallows PerplexityBot)` → use browser_task respectfully, conservative volume.
4. **Skip or re-discover.** `url_invalid` sources need a path correction — quick web search will usually find the live page.

## Current summary stats

- **146 total sources** across 21 cities and 12 national aggregators
- **117 reachable** on first HTTP probe
- **63 RSS feeds** auto-detected (the highest-value subset)
- Rating distribution: `excellent` 63 · `good` 47 · `blocked` 15 · `url_invalid` 13 · `fair` 7 · `rate_limited` 1

## City coverage

- **West Coast Mega:** Los Angeles, San Francisco, San Diego, Seattle, Portland
- **East Coast Mega:** New York, Boston, Washington DC, Philadelphia, Miami, Atlanta
- **In-between Mega:** Chicago, Houston, Dallas, Austin, Denver, Phoenix, Las Vegas, Minneapolis, Nashville, New Orleans

## Refresh cadence recommendation

- Re-probe quarterly (URLs rot, robots.txt changes, publishers move CMS).
- After re-probe, diff `agent_compatibility.rating` per source to flag regressions.
