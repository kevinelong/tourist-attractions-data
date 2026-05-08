# Tourist Attractions Data

JSON datasets for tourist attractions across US cities. Each file contains structured attraction data including name, category, description, address, hours, admission, website, phone, image_url, highlights, tips, and nearby attractions.

## Major Cities
| File | City | Attractions |
|------|------|-------------|
| sf_bay_area_attractions.json | San Francisco Bay Area, CA | 112 |
| reno_area_attractions.json | Reno, NV | 111 |
| seattle_area_attractions.json | Seattle, WA | 108 |
| portland_area_attractions.json | Portland, OR | 114 |
| mammoth_lakes_attractions.json | Mammoth Lakes, CA | 89 |
| new_orleans_attractions.json | New Orleans, LA | 202 |
| santa_barbara_attractions.json | Santa Barbara, CA | 140 |

## West Coast Capitals & College Towns
| File | City | Attractions |
|------|------|-------------|
| sacramento_attractions.json | Sacramento, CA | 103 |
| salem_attractions.json | Salem, OR | 89 |
| olympia_attractions.json | Olympia, WA | 99 |
| berkeley_attractions.json | Berkeley, CA (UC Berkeley) | 93 |
| davis_attractions.json | Davis, CA (UC Davis) | 85 |
| santacruz_attractions.json | Santa Cruz, CA (UC Santa Cruz) | 89 |
| slo_attractions.json | San Luis Obispo, CA (Cal Poly) | 91 |
| chico_attractions.json | Chico, CA (CSU Chico) | 89 |
| corvallis_attractions.json | Corvallis, OR (Oregon State) | 67 |
| eugene_attractions.json | Eugene, OR (U of Oregon) | 64 |
| bellingham_attractions.json | Bellingham, WA (WWU) | 67 |
| pullman_attractions.json | Pullman, WA (WSU) | 66 |

## Schema
```json
{
  "name": "string",
  "category": "string",
  "description": "string",
  "address": "string",
  "city": "string",
  "region": "string",
  "hours": "string",
  "days_open": "string",
  "admission": "string",
  "website": "string",
  "phone": "string",
  "image_url": "string",
  "highlights": ["string"],
  "tips": "string",
  "nearby": "string"
}
```
