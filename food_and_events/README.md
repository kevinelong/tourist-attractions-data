# Mega-City Restaurant Openings & Events

Per-city JSON files with recent restaurant openings and dated/ticketed events for 21 U.S. mega-city metros.

## Pipeline

1. **Source registry** — see `sources.json` in the repo root: 146 sources probed for RSS, robots.txt disposition, JS framework, and agent-compatibility rating
2. **Per-city extraction plan** — top 3-4 sources per city per content type, cost-sorted (RSS-first, then HTTP, browser_task only when blocked)
3. **Deterministic classifier** — Python regex + URL-path heuristics separate true openings from reviews/round-ups/news; events require a date-hint + event-keyword + ticket-signal
4. **Output normalization** — HTML stripping, markdown-link cleanup, ISO dates, deterministic category tagging
5. **Per-city JSON** — top-level keys: `title`, `generated`, `city`, `tier`, `population_m`, `extraction_method`, `totals`, `sources_used`, `sources_failed`, `raw_html_pages_available`, `restaurant_openings[]`, `events_calendar[]`

## City Run Order (used to generate these files)

West Coast → East Coast → Central, each tier by metro population descending.

| # | City | Tier | Metro Pop (M) |
|---|------|------|--------------|
| 1 | Los Angeles | west_coast_mega | 12.81 |
| 2 | San Francisco | west_coast_mega | 4.57 |
| 3 | Seattle | west_coast_mega | 4.10 |
| 4 | San Diego | west_coast_mega | 3.30 |
| 5 | Portland | west_coast_mega | 2.51 |
| 6 | New York | east_coast_mega | 19.50 |
| 7 | Atlanta | east_coast_mega | 6.31 |
| 8 | Washington | east_coast_mega | 6.30 |
| 9 | Philadelphia | east_coast_mega | 6.25 |
| 10 | Miami | east_coast_mega | 6.18 |
| 11 | Boston | east_coast_mega | 4.94 |
| 12 | Chicago | in_between_mega | 9.26 |
| 13 | Dallas | in_between_mega | 8.10 |
| 14 | Houston | in_between_mega | 7.51 |
| 15 | Phoenix | in_between_mega | 5.07 |
| 16 | Minneapolis | in_between_mega | 3.71 |
| 17 | Denver | in_between_mega | 3.05 |
| 18 | Austin | in_between_mega | 2.55 |
| 19 | Las Vegas | in_between_mega | 2.40 |
| 20 | Nashville | in_between_mega | 2.16 |
| 21 | New Orleans | in_between_mega | 1.27 |

## Item Schema

### restaurant_openings[]

```json
{
  "name": "Restaurant or article title (HTML-stripped)",
  "url": "Canonical article URL",
  "summary": "Plain-text summary, ~600 chars max",
  "categories": ["Italian", "Pizza"],
  "published_iso": "2026-06-23",
  "classification_hint": "opening | opening_from_html_listing",
  "source": {"name": "Eater LA", "url": "https://la.eater.com"}
}
```

### events_calendar[]

```json
{
  "name": "Event name",
  "url": "Event URL",
  "summary": "Plain-text summary, ~600 chars max",
  "category": "Music | Comedy | Art & Exhibits | Theater & Performance | Sports | Food & Drink | Community & Outdoor | Workshops & Talks | Other",
  "published_iso": "2026-06-20",
  "classification_hint": "event | event_no_date | event_from_html_listing",
  "source": {"name": "...", "url": "..."}
}
```

## Anti-Pollution Rules Applied (from Berkeley A/B test)

- Token-sequence dedup: no field repeats the same phrase twice
- Markdown links stripped: `[Name](url)` → `Name`
- HTML entities decoded (&#8217; → ’, etc.)
- Article-style false positives filtered (obituaries, fires, James Beard award round-ups, "best of" guides excluded from openings)

## Generation Stats

Total: 353 items across 21 cities (73 openings + 280 events).
