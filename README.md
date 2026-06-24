# Tourist Attractions Data

JSON datasets for tourist attractions across US cities and international destinations. Each file contains structured attraction data including name, category, description, address, hours, admission, website, phone, image_url, highlights, tips, and nearby attractions.

## Pipeline Documentation

| File | Purpose |
|------|---------|
| [PIPELINE_PLAYBOOK.md](PIPELINE_PLAYBOOK.md) | **Start here.** Full end-to-end instructions for running the research pipeline — entity list preparation, wide_browse execution, compile, zip, and GitHub push. Covers credit management, retry patterns, and the international roadmap. |
| [compile_template.py](compile_template.py) | Reusable Python compile script. Copy, fill in the `CITIES` list with your batch's CSV suffixes, and run to produce JSON files. |
| [monitoring/AGENT_INSTRUCTIONS.md](monitoring/AGENT_INSTRUCTIONS.md) | Instructions for a monitoring agent to run monthly change-detection against the baseline snapshot. |
| [monitoring/baseline_snapshot.json](monitoring/baseline_snapshot.json) | Fingerprint snapshot of 521 attractions across 6 cities — used for change detection. |

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

## East Coast Capitals & College Towns
| File | City | Attractions |
|------|------|-------------|
| boston_attractions.json | Boston, MA | — |
| cambridge_ma_attractions.json | Cambridge, MA (Harvard/MIT) | — |
| providence_attractions.json | Providence, RI | — |
| hartford_attractions.json | Hartford, CT | — |
| albany_attractions.json | Albany, NY | — |
| new_haven_attractions.json | New Haven, CT (Yale) | — |
| trenton_attractions.json | Trenton, NJ | — |
| harrisburg_attractions.json | Harrisburg, PA | — |
| annapolis_attractions.json | Annapolis, MD | — |
| dover_de_attractions.json | Dover, DE | — |
| richmond_attractions.json | Richmond, VA | — |
| raleigh_attractions.json | Raleigh, NC | — |
| columbia_sc_attractions.json | Columbia, SC | — |
| augusta_me_attractions.json | Augusta, ME | — |
| concord_nh_attractions.json | Concord, NH | — |
| montpelier_attractions.json | Montpelier, VT | — |
| princeton_attractions.json | Princeton, NJ | — |
| ithaca_attractions.json | Ithaca, NY (Cornell) | — |
| hanover_nh_attractions.json | Hanover, NH (Dartmouth) | — |
| amherst_ma_attractions.json | Amherst, MA | — |
| college_park_attractions.json | College Park, MD (UMD) | — |
| charlottesville_attractions.json | Charlottesville, VA (UVA) | — |
| chapel_hill_attractions.json | Chapel Hill, NC (UNC) | — |
| burlington_vt_attractions.json | Burlington, VT (UVM) | — |
| newark_de_attractions.json | Newark, DE (U of Delaware) | — |
| durham_nc_attractions.json | Durham, NC (Duke) | — |

## East Coast Major Metros
| File | City | Attractions |
|------|------|-------------|
| nyc_attractions.json | New York City, NY | — |
| philadelphia_attractions.json | Philadelphia, PA | — |
| washington_dc_attractions.json | Washington, DC | — |
| baltimore_attractions.json | Baltimore, MD | — |
| miami_attractions.json | Miami, FL | — |
| atlanta_attractions.json | Atlanta, GA | — |
| charlotte_nc_attractions.json | Charlotte, NC | — |
| nashville_attractions.json | Nashville, TN | — |
| pittsburgh_attractions.json | Pittsburgh, PA | — |
| buffalo_ny_attractions.json | Buffalo, NY | — |
| portland_me_attractions.json | Portland, ME | — |
| savannah_ga_attractions.json | Savannah, GA | — |
| charleston_sc_attractions.json | Charleston, SC | — |
| newport_ri_attractions.json | Newport, RI | — |

## Nevada
| File | City | Attractions |
|------|------|-------------|
| las_vegas_attractions.json | Las Vegas, NV | — |
| carson_city_attractions.json | Carson City, NV | — |
| henderson_nv_attractions.json | Henderson, NV | — |
| lake_tahoe_nv_attractions.json | Lake Tahoe, NV | — |

## Midwest Capitals & College Towns
| File | City | Attractions |
|------|------|-------------|
| madison_wi_attractions.json | Madison, WI | 128 |
| ann_arbor_mi_attractions.json | Ann Arbor, MI (U of Michigan) | 95 |
| columbus_oh_attractions.json | Columbus, OH | 107 |
| indianapolis_in_attractions.json | Indianapolis, IN | 99 |
| springfield_il_attractions.json | Springfield, IL | 85 |
| iowa_city_ia_attractions.json | Iowa City, IA (U of Iowa) | 84 |
| minneapolis_mn_attractions.json | Minneapolis, MN | 100 |
| lansing_mi_attractions.json | Lansing, MI | 77 |
| lincoln_ne_attractions.json | Lincoln, NE | 84 |
| lawrence_ks_attractions.json | Lawrence, KS (KU) | 78 |
| bloomington_in_attractions.json | Bloomington, IN (IU) | 78 |
| columbia_mo_attractions.json | Columbia, MO (Mizzou) | 83 |

## Midwest Major Metros
| File | City | Attractions |
|------|------|-------------|
| chicago_il_attractions.json | Chicago, IL | 128 |
| detroit_mi_attractions.json | Detroit, MI | 89 |
| cleveland_oh_attractions.json | Cleveland, OH | 94 |
| milwaukee_wi_attractions.json | Milwaukee, WI | 88 |
| cincinnati_oh_attractions.json | Cincinnati, OH | 66 |
| stlouis_mo_attractions.json | St. Louis, MO | 89 |
| kansascity_mo_attractions.json | Kansas City, MO | 89 |
| omaha_ne_attractions.json | Omaha, NE | 86 |

## Texas, Oklahoma & Arkansas
| File | City | Attractions |
|------|------|-------------|
| dallas_tx_attractions.json | Dallas, TX | 93 |
| houston_tx_attractions.json | Houston, TX | 98 |
| austin_tx_attractions.json | Austin, TX | 56 |
| sanantonio_tx_attractions.json | San Antonio, TX | 92 |
| oklahomacity_ok_attractions.json | Oklahoma City, OK | 87 |
| tulsa_ok_attractions.json | Tulsa, OK | 88 |
| littlerock_ar_attractions.json | Little Rock, AR | 80 |
| batonrouge_la_attractions.json | Baton Rouge, LA | 86 |

## Mountain & Southwest
| File | City | Attractions |
|------|------|-------------|
| denver_co_attractions.json | Denver, CO | 112 |
| boulder_co_attractions.json | Boulder, CO | 92 |
| fortcollins_co_attractions.json | Fort Collins, CO | 85 |
| coloradosprings_co_attractions.json | Colorado Springs, CO | 92 |
| phoenix_az_attractions.json | Phoenix, AZ | 104 |
| tucson_az_attractions.json | Tucson, AZ | 91 |
| scottsdale_az_attractions.json | Scottsdale, AZ | 86 |
| albuquerque_nm_attractions.json | Albuquerque, NM | 91 |
| santafe_nm_attractions.json | Santa Fe, NM | 92 |
| saltlakecity_ut_attractions.json | Salt Lake City, UT | 98 |
| provo_ut_attractions.json | Provo, UT | 102 |

## South & Southeast
| File | City | Attractions |
|------|------|-------------|
| memphis_tn_attractions.json | Memphis, TN | — |
| louisville_ky_attractions.json | Louisville, KY | — |
| lexington_ky_attractions.json | Lexington, KY | — |
| jackson_ms_attractions.json | Jackson, MS | — |
| desmoines_ia_attractions.json | Des Moines, IA | — |
| knoxville_tn_attractions.json | Knoxville, TN | — |
| chattanooga_tn_attractions.json | Chattanooga, TN | — |
| birmingham_al_attractions.json | Birmingham, AL | — |

## Great Plains & Additions
| File | City | Attractions |
|------|------|-------------|
| bismarck_nd_attractions.json | Bismarck, ND | 88 |
| pierre_sd_attractions.json | Pierre, SD | 81 |
| topeka_ks_attractions.json | Topeka, KS | 89 |
| jeffersoncity_mo_attractions.json | Jefferson City, MO | 82 |
| helena_mt_attractions.json | Helena, MT | 90 |
| cheyenne_wy_attractions.json | Cheyenne, WY | 87 |
| fargo_nd_attractions.json | Fargo, ND | 85 |
| siouxfalls_sd_attractions.json | Sioux Falls, SD | 87 |
| rapidcity_sd_attractions.json | Rapid City, SD | 89 |
| boise_id_attractions.json | Boise, ID | 89 |
| ogden_ut_attractions.json | Ogden, UT | 86 |
| laramie_wy_attractions.json | Laramie, WY | 82 |

## Zip Archives
| File | Contents |
|------|----------|
| major_cities_attractions.zip | SF Bay, Reno, Seattle, Portland, Mammoth Lakes, New Orleans, Santa Barbara |
| west_coast_capitals_colleges_attractions.zip | Sacramento, Salem, Olympia + 9 college towns |
| east_coast_capitals_colleges_attractions.zip | 26 East Coast capital & college town cities |
| east_coast_metros_attractions.zip | 14 East Coast major metro cities |
| nevada_attractions.zip | Las Vegas, Carson City, Henderson, Lake Tahoe |
| midwest_capitals_colleges_attractions.zip | 12 Midwest capitals & college towns |
| midwest_major_metros_attractions.zip | 8 Midwest major metros |
| texas_oklahoma_arkansas_attractions.zip | 8 cities: TX, OK, AR, LA |
| mountain_southwest_attractions.zip | 11 Mountain & Southwest cities |
| south_southeast_attractions.zip | 8 South & Southeast cities |
| great_plains_additions_attractions.zip | 12 Great Plains + Boise, Ogden, Laramie |

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
