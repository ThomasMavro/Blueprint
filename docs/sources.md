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
| `wsl_official` | WSL official site (fixtures, results, attendances) | https://www.wslfootball.com | | | | | not checked | A · fixtures at /fixtures/index (from Thomas) |
| `fbref` | FBref women's match logs | https://fbref.com | | | | | not checked | A · known strict bot rate limits |
| `wikipedia` | Wikipedia WSL season pages | https://en.wikipedia.org | | | | | not checked | A · open licence; long history |
| `transfermarkt` | Transfermarkt attendances | https://www.transfermarkt.com | | | | | not checked | A · terms may forbid scraping |
| `chelsea_fc` | Chelsea FC fixtures and ticketing pages | https://www.chelseafc.com | | | | | not checked | A · prices, venues |
| `open_meteo` | Open-Meteo historical weather API | https://open-meteo.com | | | | | not checked | A · free, no key |
| `pl_fixtures` | Premier League men's fixture list | https://www.premierleague.com | | | | | not checked | A · clash dates |
| `bbc_tv` | BBC TV listings and match picks | https://www.bbc.co.uk | | | | | not checked | A · TV picks |
| `sky_tv` | Sky Sports TV picks | https://www.skysports.com | | | | | not checked | A · TV picks |
| `club_partner_pages` | Club partner pages (WSL + European elite) | | | | | | not checked | B · one URL per club, listed when checked |
| `sportbusiness` | SportBusiness news | https://www.sportbusiness.com | | | | | not checked | B · RSS if available |
| `sportspro` | SportsPro news | https://www.sportspromedia.com | | | | | not checked | B · RSS if available |
| `fc_business` | FC Business news | https://www.fcbusiness.co.uk | | | | | not checked | B · RSS if available |
| `youtube_api` | YouTube Data API v3 | https://developers.google.com/youtube/v3 | | | | | not checked | B · official, free daily quota |
| `instagram` | Instagram public profiles | https://www.instagram.com | | | | | not checked | B · spec's biggest risk |
| `tiktok` | TikTok public profiles | https://www.tiktok.com | | | | | not checked | B · spec's biggest risk |
| `x` | X public profiles | https://x.com | | | | | not checked | B · spec's biggest risk |
| `google_trends` | Google Trends (via pytrends) | https://trends.google.com | | | | | not checked | B · unofficial library |
| `companies_house` | Companies House API (annual accounts) | https://developer.company-information.service.gov.uk | | | | | not checked | B · free, needs a free key |

## Hosting free tiers (priority C)

Not data sources, so not loaded into the warehouse. Checked for limits in Phase 0.

| Service | Use | Limits checked on | Findings |
|---|---|---|---|
| Hugging Face Spaces | Host the Dash app | | |
| Render free plan | Host the Dash app (alternative) | | |
| Hugging Face datasets | Store raw and warehouse data files | | |
| GitHub releases | Store data files (alternative) | | |
