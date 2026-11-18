# Job Radar — project instructions

This folder is Dorian's personal job-search agent. It finds Salesforce / CRM vacancies, proves each one is still open, scores it against his profile, and keeps the list in `data/jobs.json`. The dashboard `tracker.html` is generated from that file by `scripts/render.py`.

Run the sweep with `/job-radar` (full), `/job-radar recheck` (only re-verify existing roles) or `/job-radar search` (only look for new roles).

## Profile (the only facts you may use about Dorian)
- Salesforce since 2022: Junior SF Admin (2022–23), SF Developer and product owner of an app published on AppExchange (2023), SF Consultant / Team Lead incl. Senior SF Admin on a multi-country engagement (2023–25), now Business Analyst & Salesforce Consultant at a CRM consultancy in Warsaw (2026–).
- Certifications: Administrator, Platform App Builder, Associate, Platform Developer I, AI Associate, Agentforce Specialist; Trailhead Ranger.
- Delivery: Amazon Connect go-lives in the US and Canada (UAT, call flows, queues, voicemail, go-live, hypercare); Service Cloud Voice and Omni-Channel across several countries; Record-Triggered Flows, report types, dashboards; data migration of 1M+ accounts during a full move off Salesforce; MCAE/Pardot sync fixes.
- Presales: commercial offers (scope, timeline, pricing), demos to 30+ people, RFP and public-tender work, C-level stakeholders.
- Also: Jira and Confluence; Claude-based AI workflows; editor-in-chief of a Salesforce apps blog (100+ articles).
- Languages: Ukrainian native, English C1, **Polish B1**, Italian B1, Spanish conversational.
- Wants: B2B contract; remote (Poland/EU) or hybrid/onsite in Warsaw.
- CV rule: never name clients; describe them (industry, size).

## Hard exclusions
Spyrosoft (any entity) and its clients · quota-carrying sales / SDR · senior pure-developer roles (Apex/LWC/Java coding) · architect roles needing 8+ years · roles needing a language other than English/Polish/Ukrainian/Italian (German "nice to have" is fine).

## Already applied (Nov 2026) — don't re-add as new
Digital Forms (Salesforce Consultant), Tukano (Salesforce Administrator), Madiff (Salesforce Consultant), a HubSpot implementation role (LinkedIn), Deloitte Digital (AI Marketing & Content Senior Consultant), Eurocash (Salesforce CRM Solution Consultant), act digital (Analityk Biznesowy – Salesforce CRM).

## Data rules
- `data/jobs.json` → `{"schema":"job-radar/1","jobs":[...]}`. One object per role. Field meanings are in `.claude/skills/job-radar/SKILL.md`.
- `status` belongs to Dorian (New / Interested / Applied / Interview / Rejected). Write "New" only when adding a role; change it only when he asks.
- Never delete a role. Dead roles get `live: "closed"`.
- After every change to `data/jobs.json`, run `python3 scripts/validate.py` and then `python3 scripts/render.py`.

## Liveness lessons (learned the hard way)
- **justjoin.it / rocketjobs.pl:** expired offers stay online with no "expired" banner and often with an Apply button. Their search pages are cached copies, sometimes weeks old, so "N days left" in search results is not reliable. The reliable signal is the absolute date on the ad page: "N day left (until DD.MM.YYYY)" next to the ad's own salary/Apply block. Date in the past → closed. An explicit "Offer expired" banner → closed. Dates inside "Similar offers" blocks don't count.
- **Employer and ATS pages** (Greenhouse, Lever, Workable, Teamtailor, Recruitee, Personio, SmartRecruiters, the company's careers site): a live page with an apply form/button and no closed notice = open. Lever and Greenhouse remove closed postings.
- **Mirrors** (czyjesteldorado, hexjobs, jobimi, jobgether, jobleads, builtin, workingnomads, remotive, dailyremote, djinni, talent.com): never proof. Find the original.
- **LinkedIn and pracuj.pl** can't be read automatically. Only list them as "unverified".
- Polish level matters: an ad asking for Polish B2, C1, "fluent" or "excellent" is a missing hard requirement for Dorian (B1).
