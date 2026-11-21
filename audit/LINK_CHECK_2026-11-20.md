# Link check (2026-11-20)

Read-only check of all 176 pages in the live draft book. Nothing was changed. The 1,122 unique outside links on the live
pages are identical to the set in `drafts/` (same SHA-256 of the sorted list).

| What | Count | Result |
|---|---|---|
| YouTube videos | 107 | All public and embeddable (oEmbed 200) |
| Video timestamps | 618 links | None past the last line of that video's transcript |
| Try It topic keys | 94 keys, 143 links | All exist in `bank/` |
| Game and lab links, opened live at 328 px | 86 | All load with no script errors; none wider than the frame, except the hub below |
| Internal `@go/page` links | 123 | All resolve to pages in this book; none to retired pages |
| OpenStax source links | 32 | All open the named page |
| Other sources | 8 | 5 return 200; 3 block automated checks (below) |

## Fix needed (not made)

**Elements opens in CHEM 1A.** The Practice Games pages embed `elements/` with no course, and the game then starts on
CHEM 1A. Affects 1.13 and 2.9 (frame and new-tab link on each). `elements/?course=3A` opens CHEM 3A.

`sigfig/` and `metric/` on 1.13 also have no course. They opened on CHEM 3A in this check, but adding `?course=3A` makes
that explicit, matching every other course-based game in the book. Both were tested with the parameter.

## Needs a person to click

These sites answer automated requests with a bot check, which was not bypassed:

- 12.1: https://doi.org/10.1002/2014GL060018 (Crossref confirms the DOI and title: "Winter fog is decreasing in the fruit
  growing region of the Central Valley of California," *Geophysical Research Letters* 41)
- 1.8: https://escholarship.org/uc/item/3791z02f (UC ANR Publication 8519; page not confirmed)
- 2.4: https://www.usgs.gov/publications/biogeochemical-cycling-selenium-san-joaquin-valley-california-usa (page not
  confirmed)

## Notes

- The Study Hub (`games/`) is linked in a new tab, never framed. It is 371 px wide at 328 px but fits a 375 px phone.
  Its 404s are the hub probing repos for an optional `meta.json`, and it still loads.
- Whether each video timestamp lands on the exact topic named in the text was not rechecked here.

## Fixed (2026-11-20, Dr. Dan approved)

Added `?course=3A` to the frame and new-tab link for Sig Fig Sleuth, Metric and Elements on 1.13, and Elements on 2.9.
