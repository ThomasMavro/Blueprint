# Source register

Every data source Blueprint uses or considers, with what was checked and when.
`python -m blueprint.models.build` loads the register table below into the warehouse
`source` table, so keep its columns as they are.

- **robots_ok**: `yes` / `no` / blank (not checked yet)
- **verdict**: `use`, `use with limits`, `don't use` or `not checked`
- Dates are YYYY-MM-DD. A blank URL means the right address is still to be confirmed.

## Data sources

| source_id | name | url | robots_ok | terms_checked_on | history_depth | polite_rate | verdict | notes |
|---|---|---|---|---|---|---|---|---|
| `wsl_official` | WSL official site (fixtures, results, attendances) | https://www.wslfootball.com | yes | 2026-11-12 | Current season seen on /fixtures/index (kick-off, venue, broadcaster); older seasons not checked yet | 1 request / 5 s (no Crawl-delay set; our default) | use with limits | A · Terms (/terms-and-conditions, updated 2026-08-18) allow copies "for solely educational, non-commercial purposes"; commercial use needs a licence; WSL must be credited as author. Fixtures list the broadcaster per match, so they replace the BBC/Sky TV-pick sources. Page is heavy (~2 MB) |
| `fbref` | FBref women's match logs | https://fbref.com | | | | | don't use | A · Every request, robots.txt included, gets a Cloudflare bot challenge (HTTP 403, 2026-11-12). Robots and terms can't be read without getting round the challenge, which we won't do. See `statsbomb_open` for event data |
| `wikipedia` | Wikipedia WSL season pages | https://en.wikipedia.org | yes | 2026-11-12 | Season pages from 2011; per-match attendance seen on the 2025–26 page; detail on earlier pages not checked yet | 1 request / 5 s | use | A · Text is CC BY-SA 4.0 (Wikipedia:Copyrights): credit and link back, share-alike. Wikimedia's User-Agent policy sits on meta.wikimedia.org (not reachable here) and is not read yet. Good cross-check for `ewf_database` and source for the current season |
| `transfermarkt` | Transfermarkt attendances | https://www.transfermarkt.com | yes | 2026-11-12 | | | don't use | A · robots.txt allows all bots, but the terms (/intern/anb) forbid "bots, spiders, screen scraping or other automated processes" and reserve text and data mining (§44b UrhG) |
| `chelsea_fc` | Chelsea FC fixtures and ticketing pages | https://www.chelseafc.com | yes | 2026-11-12 | | | don't use | A · Terms (/en/terms-and-conditions; page needs JavaScript) 2.4: personal, non-commercial use only; 3(d): no automated scraping for use in a third-party app; 5.3: no public use without written consent. Ticket prices need another route: Thomas to decide |
| `open_meteo` | Open-Meteo historical weather API | https://open-meteo.com | no | 2026-11-12 | 1940 to now (Historical Weather API docs page) | Free tier: under 600 calls/min, 5,000/hour, 10,000/day; we need about 1 call per match | use with limits | A · Terms (/en/terms): free API for non-commercial use only; data under CC BY 4.0 (credit Open-Meteo). robots.txt on open-meteo.com allows all, but the API host archive-api.open-meteo.com says "Disallow: /", so a normal crawler would skip it. 2026-11-12: Thomas approved skipping robots for this documented API only (`DOCUMENTED_APIS` in ingest/_common.py); the 5 s delay and published limits still apply. Sample call OK (HTTP 200, limit headers 600/min). One earlier call got HTTP 429: limits are per IP and cloud IPs are shared, so collection runs must log 429s and retry later, never skip silently |
| `pl_fixtures` | Premier League men's fixture list | https://www.premierleague.com | yes | 2026-11-12 | | | don't use | A · Terms forbid "creating a database ... that includes material downloaded or otherwise obtained from the Website". Replaced by `openfootball_pl` |
| `bbc_tv` | BBC TV listings and match picks | https://www.bbc.co.uk | no | | | | don't use | A · The robots.txt header says no scraping or crawling, no datasets from BBC content and no business use without permission. /terms page not opened, since robots.txt already rules it out. TV picks come from `wsl_official` |
| `sky_tv` | Sky Sports TV picks | https://www.skysports.com | yes | | | | not checked | A · robots.txt allows /watch/football-on-sky (one sample page fetched). The terms are on www.sky.com, which this environment doesn't allow, so they're not read. Probably not needed: `wsl_official` lists broadcasters |
| `ewf_database` | English Women's Football (EWF) Database | https://github.com/probjects/ewf-database | | 2026-11-12 | WSL matches 2011 to 2024–25 (2,540 rows incl. tier 2 from 2014); attendance on 75–100% of matches per season, none for 2020–21 (behind closed doors); 110 of 128 Chelsea home WSL matches have attendance; updated after each season | One CSV download per season | use | A (new) · Licence CC BY-SA 4.0 (README): cite "The English Women's Football (EWF) Database"; derived data stays CC BY-SA. File download from GitHub, not crawling. Suggested by Thomas |
| `statsbomb_open` | StatsBomb open data (event data) | https://github.com/statsbomb/open-data | | 2026-11-12 | WSL 2018/19, 2019/20, 2020/21, 2023/24; also Liga F, Frauen-Bundesliga, Serie A Women 2023/24, NWSL 2018 and 2023, Euros 2022 and 2025, World Cups 2019 and 2023 | One-off download | use with limits | A (new) · README terms: credit StatsBomb as the data source and show their logo in published work. Full user agreement (LICENSE.pdf) not read yet. Match events only, no attendance |
| `openfootball_pl` | openfootball Premier League fixtures (football.json) | https://github.com/openfootball/football.json | | 2026-11-12 | 2025–26 and 2026–27 checked (380 matches each); older seasons in the repo not checked | One JSON file per season | use | A (new) · Public domain ("use as you please with no restrictions"). Replaces `pl_fixtures` for clash dates |
| `club_partner_pages` | Club partner pages (WSL + European elite) | | | | | | not checked | B · one URL per club, listed when checked |
| `sportbusiness` | SportBusiness news | https://www.sportbusiness.com | | | | | not checked | B · RSS if available |
| `sportspro` | SportsPro news | https://www.sportspromedia.com | | | | | not checked | B · RSS if available |
| `fc_business` | FC Business news | https://www.fcbusiness.co.uk | | | | | not checked | B · RSS if available |
| `youtube_api` | YouTube Data API v3 | https://developers.google.com/youtube/v3 | | | | | not checked | B · official, free daily quota |
| `instagram` | Instagram public profiles | https://www.instagram.com | | | | | not checked | B · spec's biggest risk |
| `tiktok` | TikTok public profiles | https://www.tiktok.com | | | | | not checked | B · spec's biggest risk |
| `x` | X public profiles | https://x.com | | | | | not checked | B · spec's biggest risk |
| `google_trends` | Google Trends (via pytrends) | https://trends.google.com | | | | | not checked | B · unofficial library |
| `sportsdatastack` | Sports Data Stack, WSL pages | https://sportsdatastack.com/leagues/wsl/ | | | | | not checked | B · suggested by Thomas; host not allowed yet |
| `wfdata` | WF Data | https://wfdata.co.uk/ | | | | | not checked | B · suggested by Thomas; host not allowed yet |
| `companies_house` | Companies House API (annual accounts) | https://developer.company-information.service.gov.uk | | | | | not checked | B · free, needs a free key |

## Hosting free tiers (priority C)

Not data sources, so not loaded into the warehouse. Checked for limits in Phase 0.

| Service | Use | Limits checked on | Findings |
|---|---|---|---|
| Hugging Face Spaces | Host the Dash app | | |
| Render free plan | Host the Dash app (alternative) | | |
| Hugging Face datasets | Store raw and warehouse data files | | |
| GitHub releases | Store data files (alternative) | | |
