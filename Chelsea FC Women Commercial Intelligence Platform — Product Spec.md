# Chelsea FC Women Commercial Intelligence Platform — Product Spec.md

Nov 11, 2026 · @Thomas

## Purpose, users and principles

Blueprint (working name) is a commercial intelligence platform for Chelsea FC Women: it turns public data into insights that support decisions on partnerships, matchday revenue, fan growth and player-led deals. It is built as if by an in-house analyst, using only data the club or a motivated outsider can reach, and benchmarked against the WSL, Europe's elite clubs and Chelsea's men's team only for shared assets such as the Circle shirt deal, since the club builds its brand independently.

**Context that shapes it.** From 2026/27 all 13 WSL home games are at Stamford Bridge, so the core matchday problem is filling a 40,000-seat stadium every fortnight. Current partners include Circle (front of shirt, shared with the men's team), Škoda UK (back of shirt, five player ambassadors), Rimmel London and Champagne PIAFF (hospitality). Champions League home games are at Plough Lane (AFC Wimbledon). Chelsea FC Women is a separate legal entity with minority investment, led by CEO Aki Mandhar, COO Nadia Shahrestani and CRO Giulia Mazzia. Central league income is modest, so growth has to come from fans, partnerships and ticketing.

**Users.**

| User | What they need from Blueprint |
| --- | --- |
| Partnership sales manager | Which categories and brands to approach next, with a pitch-ready evidence pack |
| Partner account manager | A renewal report showing each partner the exposure and engagement they received |
| Brand activation manager | Which activations (campaigns, matchday moments, player content) performed best for each partner, and which formats to repeat |
| Partnerships operations executive | A tracker of what each contract promises (posts, boards, appearances) against what has been delivered so far |
| Ticketing and matchday lead | Which fixtures need help to fill the Bridge, and which levers work |
| Marketing lead and content team | What content, players and channels grow the audience |
| CRO and leadership | One page: where revenue growth will come from, against peers |

**Design principles.**

1. **Insight first, decision human.** Every screen opens with three to five plain-language findings, each with its number and the context needed to judge it (peer comparison, trend, confidence). Charts sit underneath as proof. Blueprint never tells staff what to do: it shows what is happening and why, and the decision stays with them.
2. **No data expertise needed.** No jargon on screen; every metric has a one-line definition on hover; filters use football words (season, competition, opponent), not database fields.
3. **Always benchmarked.** A number on its own means nothing to a commercial team; every metric shows Chelsea's rank and gap against a chosen peer set.
4. **Honest about uncertainty.** Estimated values (media value, attendance forecasts) show a range and their method, never a single false-precise figure.
5. **Exportable.** Any finding becomes a slide or a one-page PDF for a partner meeting in one click.
6. **Fresh.** Pipelines refresh automatically (weekly for social and sponsors, after each match for matchday data), and each screen shows when its data was last updated.

## The five modules

Blueprint has five modules, one per commercial decision, plus a Home page that pulls the top finding from each. Each module answers a short list of questions a real commercial team asks.

### 1. Partnerships: where the opportunities are

- Which sponsor categories have peers sold that Chelsea has not (category gap map)?
- Which brands already invest in women's sport but not with Chelsea (target shortlist, ranked by fit)?
- Which brands are new to women's football this season, and with whom did they sign?
- What do comparable deals look like (reported values where public, asset packages where not)?

**Signature views:** category heatmap (clubs × categories), brand fit ranking, deal tracker, one-click target pack.

**Club context.** Whether an opportunity is right also depends on what public data cannot show: the club's revenue targets, budget, brand values, categories it rules out (betting or alcohol, for example) and the inventory still unsold. Blueprint keeps these as editable settings, shared by all modules. When they are set, views are filtered by them; when they are not, findings are labelled "public view" so nobody mistakes a market gap for a fit with the club's strategy.

### 2. Partner value: proving ROI for renewals

- How much exposure did each partner receive (logo appearances in club posts and match imagery, mentions, partner-tagged content)?
- How did partner content perform against Chelsea's normal posts, and against similar partners at rival clubs?
- What is the estimated media value, shown as a range with the method?
- What activations and benefits do partners receive at peer clubs and in other sports (player appearances, content series, hospitality, fan transport, community programmes), and which could Chelsea deliver? Each one is tagged with what it needs (assets, staff time, cost band, lead time), so the team can judge feasibility for itself.

**Signature views:** partner scorecard, season-to-date exposure timeline, activation library with feasibility tags, renewal report export.

### 3. Matchday: filling Stamford Bridge

- What drives attendance: opponent, kick-off time, day, competition, TV pick, weather, men's fixture clashes, title race stakes?
- Which upcoming fixtures are at risk of a low crowd, and by how much (forecast with a range)?
- How does Chelsea's occupancy and growth compare with Arsenal at the Emirates and with European clubs playing in big stadiums?
- How much pricing headroom is there? At Kingsmeadow, raising season-ticket prices to £10–£20 a game took occupancy above 90%; Blueprint tests what the equivalent move looks like at a 40,000-seat Bridge, against peers' prices.
- Does a Bridge matchday pay for itself? Revenue per game (tickets, hospitality, partner activation) against an estimated staging cost (stewarding, stadium opening, operations), giving a break-even attendance per fixture. The estimate shows as a range until the club enters its own costs.
- How do revenues compare with the wage bill? Wages-to-revenue ratio for Chelsea and peers from published accounts (staff costs against matchday plus commercial revenue), its trend since the move to big stadiums, and how much attendance or partner growth would close the gap.
- How much does each extra 1,000 fans add per season, and how does that compare with the cost of a squad salary rise?

**Signature views:** fixture risk calendar, attendance driver chart, peer occupancy league, price benchmark, matchday break-even view, wages-to-revenue tracker.

### 4. Fanbase: growing the audience

- How fast are Chelsea's followers and engagement growing on each platform, against peers?
- Which content types, formats and posting times perform best?
- Where is interest coming from (countries and UK regions, from search trends and audience data where public)?
- How big and how fast-growing is each fan segment the club itself names (young, often female fans inspired by the Lionesses; long-time supporters; newcomers who follow one player), and how is interest growing in the US and Australian tour markets?
- What fan-growth initiatives do peer clubs and other women's sports run (memberships, junior clubs, supporters' group partnerships, matchday entertainment, international tours, creator collaborations, community programmes), and what happened to their audience and attendance afterwards? Each initiative is tagged with what it needs (assets, staff time, cost band), so the team can judge whether it fits Chelsea.

**Signature views:** platform growth league, content performance matrix, interest map, fan initiative library with before-and-after results.

### 5. Player commercial value: player-led deals

- Which players drive the most reach and engagement on club channels and their own?
- Which players over-index with which audiences or regions (useful for brand fit and international partners)?
- Who are the rising profiles to sign as ambassadors before their value peaks?
- How do on-pitch profiles (from the player galaxy project) relate to commercial reach?

**Signature views:** player commercial index, player × brand fit, rising-profile watchlist.

## Insight engine and UX

The insight engine is what turns Blueprint from a dashboard into a tool: rule-based detectors scan every metric after each refresh and write ranked findings in plain English.

**How a finding is made.**

1. **Detect.** Each detector checks one pattern: a rank change against peers, a trend break, an outlier fixture or post, a gap against the peer median, or a forecast below target.
2. **Score.** Findings are ranked by size of the effect, confidence (sample size, data freshness) and commercial relevance (a weight per module).
3. **Write.** A template turns the finding into one sentence with its number, then the context to read it: what it is compared with and how confident the figure is. No finding is worded as an instruction. Example: "Engagement per post is 2nd in the WSL but down 18% since September; player-led video is the only format still growing."
4. **Prove.** Each finding links to the chart and rows behind it, so a user can check it in one click.

An optional LLM layer can rewrite findings for tone and draft the weekly brief, but numbers always come from the detectors, never from the model.

**Navigation.**

- **Home:** the five top findings across modules, a KPI strip (average attendance, occupancy, follower growth, engagement rate, partner count, wages-to-revenue ratio) with peer rank, and what changed this week.
- **Module pages:** findings at the top, then two or three signature views, then a full data table with export.
- **Global controls:** season, competition and peer set (WSL, European elite, custom), always visible.
- **Entity pages:** one page per club, partner, brand and player, so a user can search "Rimmel" or "Arsenal" and see everything.

**Outputs.** A weekly commercial brief (PDF and email-ready text), partner renewal reports and a target-brand pack, all generated from the same findings.

**Meeting prep.** A user picks who they are meeting (a current partner, a prospect brand, leadership, a supporters' group) and Blueprint assembles a draft brief from the data: the relevant findings, key numbers against peers, the counterpart's history with the club (deals, activations delivered, exposure received, content performance), comparable cases at other clubs, and the data gaps to be aware of. It also lists open questions the data raises, framed as questions rather than advice. The user edits the brief, adds their own notes, and exports it as a one-page PDF or slides; past briefs stay attached to the partner or brand page for the next meeting.

**Look and feel.** Chelsea-adjacent but neutral (navy, white, one accent), dense like StatsBomb IQ, with consistent chart types across modules and a light and dark theme.

## Data sources and collection

All data is public or collected by scrapers you build; every source below must be checked in Phase 0 for availability, terms of use and history depth before any module depends on it.

| Dataset | Likely sources | Method | Refresh | Feeds |
| --- | --- | --- | --- | --- |
| Fixtures, results, attendances | League and club match reports, FBref, Wikipedia season pages, Transfermarkt | Scraper + manual backfill for past seasons | After each match | Matchday, Home |
| Kick-off context | Fixture lists, TV picks (BBC, Sky), weather history API, men's fixture list | Scraper + API | Weekly | Matchday |
| Ticket prices | Club ticketing pages for each fixture | Scheduled snapshots (price over time) | Daily before matches | Matchday |
| Sponsor portfolios | Club partner pages (WSL + European elite + Chelsea men), press releases | Scraper + curated table with category tags | Weekly | Partnerships |
| Sponsorship deal news | Trade press (SportBusiness, SportsPro, FC Business), club news feeds | RSS or scraper + brand and category extraction | Daily | Partnerships |
| Social accounts | YouTube Data API (official, free); Instagram, TikTok, X public profiles | API where official; otherwise weekly public snapshots | Weekly | Fanbase, Players |
| Social posts | Club posts with captions, media and engagement counts | API or snapshot scraper, stored with images | Weekly | Partner value, Fanbase, Players |
| Logo exposure | Images and video frames from club posts | Computer-vision logo detection on stored media | After post ingest | Partner value |
| Search interest | Google Trends (clubs, players, brands by country and region) | pytrends or equivalent | Weekly | Fanbase, Players, Partnerships |
| Player profiles | Squad lists, player social accounts, event data from the player galaxy pipeline | Scraper + link to existing project | Monthly | Players |
| Market context | Women's Sport Trust, Deloitte and league reports on audiences and revenue | Manual extraction into reference tables | Per release | All (benchmarks) |

**Two further inputs.** Published annual accounts (Companies House for Chelsea FC Women and English peers, club reports abroad) give revenue benchmarks where they exist. A first-party slot accepts the club's own data (ticketing CRM, the women's fan forum, post-match and annual surveys, mystery-shopper results) once Blueprint is used internally; the public version runs without it.

**Collection rules.**

- Prefer official APIs; where scraping, respect robots.txt and rate limits, store only public data, and never collect personal data about individual fans.
- Store raw snapshots unchanged, then clean into analysis tables, so any figure can be traced back to its source page and date.
- Keep a source register (URL, terms checked, date) inside the repo.
- Never fail silently. Every run writes a collection log (rows collected against rows expected, blocked requests, page-layout changes, missing fields). Any failure or shortfall is reported to Thomas straight away, with what broke and the options; data is never skipped, guessed or back-filled without his approval. A data health page in the app shows each source's last successful run.

**Known gaps and how Thomas can help.**

| Gap | Why it matters | How Thomas can help |
| --- | --- | --- |
| Sponsorship deal values | Price benchmarks for Partnerships | Note any figures heard at events (Hudl, Field of Play) or in trade press behind paywalls the university can access |
| Matchday staging costs | Break-even attendance | Ask industry contacts for typical cost ranges per stadium size |
| Social data on blocked platforms | Fanbase, Partner value, Players | Weekly manual check of a short list of accounts if scraping is blocked |
| Activations seen in person | Activation and fan initiative libraries | Photos and notes from WSL matches attended |
| Logo training images | Logo detection accuracy | Hand-label a sample of 200 to 300 images per partner |
| Historical attendances before 2023 | Longer attendance model | Check university library databases and club annual reports |
| Women's-team accounts abroad | European revenue benchmarks | Use French and Spanish to read Lyon, PSG and Barcelona reports |

## Architecture, stack and data model

Blueprint is Python end to end, so you can learn one language well: scheduled pipelines feed a DuckDB warehouse, analytics and the insight engine run on top, and a Dash app serves the result.

&#91;embedded content: Blueprint architecture · 7 layers\]

Each layer only reads from the one above it, so a broken scraper never breaks the app; the app simply shows the last good data and its date.

**Stack.**

| Layer | Choice | Why |
| --- | --- | --- |
| Language | Python 3.12 | One language for everything; strong data and ML libraries |
| Scraping | httpx, BeautifulSoup, Playwright for JavaScript pages | Covers static and dynamic sites |
| Scheduling | GitHub Actions (cron) | Free, versioned, no server to run |
| Storage | Parquet (raw) + DuckDB (warehouse) | Fast, a single file, SQL you already know from your MSc |
| Analysis | pandas or polars, statsmodels, scikit-learn | Attendance regression and forecasts, clustering, ranking |
| Computer vision | A YOLO-family detector fine-tuned on partner logos, trained on free Google Colab or Kaggle GPUs | Logo exposure in images and video frames |
| App | Dash with Dash Mantine Components, Plotly charts | Professional multi-page UI without learning JavaScript |
| Reports | Jinja2 templates + WeasyPrint to PDF | Branded briefs and partner reports from the same findings |
| Quality | pytest, ruff, data tests on every table | Catches broken scrapers before bad data reaches the app |
| Hosting | Free tier: Hugging Face Spaces or Render free plan for the app; data files in a free Hugging Face dataset or GitHub release | Shareable link for recruiters at £0; free-tier limits checked in Phase 0 |

**Core data model.**

| Table | One row per | Key fields |
| --- | --- | --- |
| club | Club | name, league, country, stadiums, peer groups |
| fixture | Match | date, kick-off, competition, venue, opponent, TV, attendance, capacity |
| ticket\_price | Price snapshot | fixture, seat band, price (GBP), snapshot date |
| partner\_deal | Club × brand deal | club, brand, category, tier, start, end, reported value |
| brand | Brand | name, category, sector, parent company, women's sport deals count |
| social\_account | Account | owner (club or player), platform, handle |
| social\_snapshot | Account × week | followers, posts, average engagement |
| post | Social post | account, date, format, caption, likes, comments, shares, views |
| logo\_detection | Post × brand | brand, seconds or frames visible, size, position |
| player | Player | club, position, nationality, linked galaxy profile |
| trend\_interest | Term × region × week | search interest index |
| finding | Insight | module, detector, score, sentence, context, confidence, evidence query, date |

## Build roadmap

The full build is about 320 hours: at 5 to 10 hours a week, that is 8 to 10 months. There is no deadline; this is a personal project built at its own pace. The core release (Phases 0 to 3, plus Home and meeting prep) comes first, at about 190 hours; Partner value and Player value follow as extensions. A usable public release still lands after Phase 1.

&#91;embedded content: Build roadmap · 7 phases, about 320 hours\]

Matchday comes first because its data is the easiest to collect and the Bridge question is the club's most visible problem. Partner value comes late because logo detection is the hardest part and needs weeks of stored posts first. Each phase ends with a Substack article on its main finding, which also feeds your sport analytics writing objective.

**Working rules for each phase.**

- Start each phase in Claude Code by planning it first: a short plan file listing tables, functions and tests, reviewed before any code.
- Build the data and tests first, the analysis second and the screen last.
- Ship to the hosted app at the end of every phase, even if rough.

## Risks, limits and open questions

The biggest risk is social data access: Instagram, TikTok and X restrict scraping, so the Fanbase, Partner value and Player modules must work from weekly public snapshots and degrade gracefully if a platform blocks collection.

| Risk | Effect | Mitigation |
| --- | --- | --- |
| Platform terms block social scraping | Gaps in Fanbase, Partner value and Player modules | Official APIs first (YouTube); low-frequency public snapshots; manual entry fallback; never scrape private data |
| Deal values are rarely public | Price benchmarks are thin | Use reported values where they exist, otherwise compare asset packages and exposure, labelled as estimates |
| Short attendance history at a 40,000-seat Bridge | Weak forecasts in 2026/27 | Model with all WSL clubs' history, then update after every Chelsea home game |
| Logo detection is hard on match photos | Noisy exposure figures | Start with the top four partners, hand-label a training set, report precision openly |
| Scope creep across five modules | Nothing finished | One module per phase, each shipped before the next starts |
| Using club logos and name | Brand or legal complaint | Present it as an independent portfolio project; no club crest, no implied endorsement |

**Open questions.**

- [ ] How many hours a week can you give Blueprint alongside the MSc? Answered: 5 to 10 hours; roadmap updated.
- [ ] Could Blueprint, or one module, become your MSc dissertation? If so, the university's AI rules apply to that part. Answered: no, Blueprint stays a separate portfolio project.
- [ ] What monthly budget is acceptable for hosting and any paid API (target: under £20)? Answered: as close to £0 as possible; the stack now uses free tiers only.
- [ ] Do you have any contact at Chelsea FC Women or a WSL club who could test the Phase 1 release? Not yet; Thomas plans to find a tester before Phase 1 ships (events, LinkedIn, MSc network).

## CLAUDE.md starter

Copy this into `CLAUDE.md` at the root of the new repo, alongside an export of this spec as `docs/spec.md`.

```markdown
# Blueprint — Chelsea FC Women commercial intelligence

## What this is
An independent portfolio tool that turns public data into insights for commercial decisions at
Chelsea FC Women: partnerships, partner value, matchday (Stamford Bridge), fanbase,
player commercial value. Full spec: docs/spec.md. Read it before planning any phase.

## Who uses it
Commercial staff who are not data experts. Every screen opens with plain-English
findings (number + context: peer comparison, trend, confidence); charts sit
underneath as proof. It informs decisions; it never makes them.

## Owner
Thomas, MSc Sport Analytics & AI student, comfortable with Python but still learning.
Explain non-obvious code choices briefly in comments and in your replies.

## Stack
Python 3.12 · httpx, BeautifulSoup, Playwright · Parquet raw store · DuckDB warehouse
· pandas/polars, statsmodels, scikit-learn · Dash + Dash Mantine Components + Plotly
· Jinja2 + WeasyPrint · pytest, ruff · GitHub Actions for schedules.

## Repo layout
src/blueprint/ingest/<source>.py   one module per source, writes raw Parquet
src/blueprint/models/               SQL + Python that build warehouse tables
src/blueprint/analytics/            models, rankings, logo detection
src/blueprint/insights/             detectors and finding templates
src/blueprint/app/                  Dash pages, one per module
data/raw/<source>/<date>/           never edited by hand
docs/sources.md                     source register: URL, terms checked, date

## Rules
- Plan each phase in a short plan file before writing code; wait for approval.
- Order: data + tests first, analysis second, screens last.
- Never invent data. Every figure must trace to a raw snapshot and its source URL.
- Never fail silently: report any failed, blocked or partial collection to Thomas at
  once, with what broke and the options. Never skip, guess or back-fill without approval.
- When a source is missing or thin, say so and ask whether Thomas can help fill it.
- Scrape politely: respect robots.txt and rate limits; public data only; no personal
  data about fans.
- Estimates (media value, forecasts) always show a range and a method note.
- Benchmark every metric against the selected peer set (WSL, European elite, custom).
- No club crests or implied endorsement; label the app an independent project.
- Insights, not recommendations: no "you should" wording in findings or reports.
- Zero budget: free tiers and free APIs only. Flag any cost to Thomas before adding it.
- Run ruff and pytest before every commit.

## Skills to use when available
- frontend-design and dataviz: for any screen, chart, colour or layout work.
- tool-showcase: when a phase ships, for the GitHub, Substack and CV updates.
- lboro-ai-assignment-support: if any part becomes assessed MSc work.

## Current phase
Phase 0: Foundations (see docs/spec.md, Build roadmap).
```

## Sources

- [Chelsea FC Women announces new business leadership roles](https://www.chelseafc.com/en/news/article/chelsea-fc-women-announces-new-business-leadership-roles)
- [Chelsea Women: how fandom, data and bold ideas are rewriting the rules (Sport for Business)](https://sportforbusiness.com/chelsea-women-changing-the-game-how-fandom-data-and-bold-ideas-are-rewriting-the-rules/)
- [Chelsea Women hire Lola Ogunbote to run football operations (Business of Sports Africa)](https://www.businessofsportsafrica.com/latest-insights/chelsea-women-hire-burnleys-lola-ogunbote-to-run-football-operations)
- [Chelsea moves all WSL games to Stamford Bridge (Gamereactor)](https://www.gamereactor.eu/?p=123003)
- [Champagne PIAFF enters Chelsea FC Women's commercial ecosystem (Sports Mint Media)](https://sportsmintmedia.com/champagne-piaff-enters-chelsea-fc-womens-growing-commercial-ecosystem/)
- [Chelsea FC Women renews partnership with Škoda UK (Soccer Scene)](https://www.soccerscene.com.au/chelsea-fc-women-renews-partnership-with-skoda-uk/)
- [We Are Chelsea podcast, episode with Zarah Al-Kudcy](https://www.chelseafc.com/en/video/playlist/we-are-chelsea-podcast-s1/growing-the-game-on-and-off-the-pitch-with-commercial-director-zarah-al?ssoc=1)
