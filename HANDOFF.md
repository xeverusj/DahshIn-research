# Dashin — Full Session Handoff Document

## Context for the New Chat

This document is a complete handoff from the previous Claude Code session.
All work was done in `xeverusj/DahshIn-research` (the wrong repo — linked by mistake).
Everything has since been **merged into `xeverusj/DahshIn` (main branch)**.

The new session should work in: **`xeverusj/DahshIn`**

---

## Repo Structure

```
DahshIn/
├── app.py                        # Streamlit entry point — routing, auth, sidebar, theme toggle
├── worker.py                     # Universal AI-powered event website scraper (Claude Vision)
├── clutch_scraper.py             # Dedicated Clutch.co company scraper
├── cleaner.py                    # CSV data cleaner
├── check_and_fix.py              # Data validation utility
├── migrate.py                    # DB schema migration
├── setup.py                      # One-time bootstrap
├── requirements.txt              # Python dependencies
├── Procfile                      # Deployment process definition
├── start.sh                      # Startup script
│
├── core/
│   ├── db.py                     # SQLite schema, get_connection(), init_db(), migrate_db()
│   ├── auth.py                   # Login, session management, RBAC
│   ├── ai_tracker.py             # Anthropic API usage tracking + budget enforcement
│   ├── styles.py                 # *** NEW *** Master CSS design system
│   ├── theme.py                  # *** NEW *** Dark/light mode CSS injection
│   └── html_selector.py          # *** NEW *** In-house lxml+cssselect selector engine
│
├── services/
│   ├── lead_service.py
│   ├── flag_service.py
│   ├── invite_service.py
│   ├── learning_service.py
│   ├── notification_service.py
│   ├── report_service.py
│   ├── task_service.py
│   └── access_control.py         # *** NEW *** Multi-tenant data visibility rules
│
├── dashboards/
│   ├── superadmin_dashboard.py
│   ├── admin_dashboard.py
│   ├── scraper_dashboard.py
│   ├── inventory_dashboard.py
│   ├── research_dashboard.py
│   ├── research_manager_dashboard.py
│   ├── campaigns_dashboard.py
│   ├── campaign_manager_dashboard.py
│   ├── estimator_dashboard.py
│   ├── client_dashboard.py
│   └── onboarding_wizard.py      # *** NEW *** First-login onboarding flow
│
├── scripts/
│   └── seed_sales_academy.py     # *** NEW *** Seeds agency org + test clients
│
└── data/system/
    ├── dashin.db                 # SQLite database
    ├── layout_patterns.json      # Learned scraper CSS selector patterns (+ fingerprints)
    └── sessions/                 # Per-scrape CSV exports
```

---

## What Was Built This Session

### 1. Unified Design System (`core/styles.py`)
- Single master CSS file replacing 9 different Google Font families scattered across dashboards
- Font stack: **Inter** (body) + **Playfair Display** (headings)
- CSS custom properties: `--bg`, `--surface`, `--border`, `--accent`, `--success`, `--error`, `--info`, `--purple`, `--radius-*`, `--shadow-*`
- Shared components: stat-cards, KPI cards, tables (`.tbl`), badges (lead status, priority, persona, role chips, campaign/CRM statuses), panels, cards, detail panels, alert boxes, terminal, buttons, form elements, tabs, Streamlit native overrides
- All dashboard headers normalized to identical `#1A1917` + Playfair title + Inter subtitle
- `inject_shared_css()` called at the start of every dashboard `render()`
- Per-dashboard CSS blocks reduced from ~100 lines each to <15 lines of unique CSS

### 2. Global Dark / Light Mode (`core/theme.py`)
- Theme toggle button in the sidebar (applies to every page globally)
- Works via CSS custom property overrides — no per-component class overrides needed
- `DARK_CSS` overrides `:root` variables + fixes any hardcoded colors
- `LIGHT_CSS` restores defaults
- Covers: stat-cards, tables, launch-box, filter-bar, detail-panel, list-card, org-card, all badge/accent colors preserved
- Deep-targets all Streamlit BaseWeb components (select boxes, dropdown listboxes, option lists, multi-value tags, tabs, labels, radio, checkbox, file uploader) at all nesting levels

### 3. In-House HTML Selector Engine (`core/html_selector.py`)
- Built on `lxml` + `cssselect` (same underlying libraries Scrapling wraps)
- Parsel-compatible API: `Selector`, `SelectorList`, `.css()`, `::text`, `::attr()`, `.find_all()`, `.get()`, `.getall()`, `.html`
- Replaced `scrapling[fetchers]` as a dependency — no external scraping library needed
- Used in both `worker.py` and `clutch_scraper.py`

### 4. Adaptive Fingerprint Healing in Scraper (`worker.py`)
Scraper now self-heals when CSS selectors go stale — similar to how Scrapling works, but built in-house:

- **`build_fingerprint_from_page()`** — after Claude Vision finds a selector, samples the live DOM to build a structural fingerprint: tag, class keywords, attr names, child count, parent context, img ratio, DOM depth, text samples
- **`fingerprint_score()`** — pure JS scorer that evaluates all candidate elements against the stored fingerprint using weighted similarity (no AI call required)
- **`heal_selector()`** — when cached selector returns 0 cards, runs fingerprint similarity scan to recover the element automatically, then rebuilds the fingerprint from the healed live DOM and updates the cache
- **Fallback chain**: cached selector → fingerprint healing → Claude Vision deep inspection → generic divs → network intercept
- Fingerprints + sub-selectors stored in both SQLite (`layout_patterns` table JSON blob) and `data/system/layout_patterns.json`

### 5. Multi-Tenant Org Hierarchy (`core/db.py`, `services/access_control.py`)
New DB columns on `organisations`:
- `org_type` (dashin / agency / freelance / client)
- `parent_org_id`, `subscription_tier`, `subscription_status`, `onboarded_at`, `onboarded_by`

New DB columns on `leads`:
- `released_to_client`, `scraped_at`

New tables:
- `freelancer_client_assignments`
- `subscription_tiers` (seeded: free / starter / growth / enterprise / client_direct)

`services/access_control.py`:
- `get_visible_org_ids()` — enforces what orgs each role can see
- `get_visible_leads_query()` — single source of truth for lead visibility per role
- `can_create_user()` — validates user creation against org type + subscription
- `check_lead_limit()`, `get_subscription_limits()`

Clients only see `released_to_client = 1` leads.

### 6. Onboarding Wizard (`dashboards/onboarding_wizard.py`)
- 3-step first-login wizard shown until `onboarded_at` is set on the user + org
- Wired into `app.py` before dashboard routing

### 7. Scraper Lock Fix (`dashboards/scraper_dashboard.py`)
- `_clear_stale_sessions()` — auto-expires `running` sessions older than 4 hours on every page load (fixes phantom lock bug)
- `_force_clear_running()` + manual "Force clear lock" button for users

### 8. Admin Dashboard — Client Org Management (`dashboards/admin_dashboard.py`)
- Add User form now uses `ROLES_BY_ORG_TYPE` and `can_create_user()` validation
- New "Client Orgs" tab for creating `org_type='client'` child organisations linked to the agency

### 9. Superadmin Dashboard — Org Hierarchy Tab
- New "Org Hierarchy" tab showing all orgs by type with parent-child relationships
- New Org form includes `org_type` and `subscription_tier` fields

---

## Technology Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit >= 1.32.0 |
| Database | SQLite 3 (WAL mode, foreign keys enabled) |
| AI / LLM | Anthropic Claude Sonnet via `anthropic` SDK |
| Web Scraping | Playwright (sync API) + playwright-stealth |
| HTML Parsing | lxml + cssselect (in-house, replaces Scrapling) |
| Data | pandas, openpyxl, CSV |
| Translation | DeepL API (optional) |
| Image | Pillow |
| HTTP | requests |
| Environment | python-dotenv |
| Python | 3.14+ |

**Note on Scrapling:** The approach and concepts from Scrapling were studied and re-implemented in-house using `lxml` + `cssselect`. There is NO Scrapling dependency in `requirements.txt`.

---

## Dependencies Added This Session

```
lxml>=4.9.0
cssselect>=1.2.0
```

Removed:
```
scrapling[fetchers]>=0.4.1   # replaced by core/html_selector.py
```

---

## Design System Reference

Colors (CSS custom properties defined in `core/styles.py`):
- `--bg`: `#F7F6F3` (cream content area)
- `--surface`: `#FFFFFF`
- `--border`: `#E8E5E0`
- `--accent`: `#C9A96E` (gold)
- `--success`: `#2D6A4F`
- `--error`: `#C0392B`
- `--info`: `#2471A3`
- `--purple`: `#6C3483`

Sidebar: `#111111` (dark)

---

## RBAC Roles

```
super_admin (100)
  org_admin (80)
    manager (60)
      research_manager (50)
      campaign_manager (45)
        researcher (30)
          client_admin (20)
            client_user (10)
```

Always use helpers from `core/auth.py`: `has_role()`, `is_internal()`, `is_client()`, `can_manage_users()`, `same_org()`.

---

## Environment Variables Required

```bash
ANTHROPIC_API_KEY=sk-ant-...        # Required
DEEPL_API_KEY=...                   # Optional
SUPER_ADMIN_EMAIL=admin@dashin.com
SMTP_HOST=                          # Optional
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
```

---

## Immediate Outstanding Issue

**GitHub Actions CI is failing** on every push to `xeverusj/DahshIn` (all 6 workflow runs show red X).

The workflow file lives at `.github/workflows/` in the DahshIn repo. The failure needs to be investigated — likely causes:
- Missing secrets (e.g. `ANTHROPIC_API_KEY` not set in GitHub repo secrets)
- Python version mismatch (app uses 3.14+, workflow may specify an older version)
- Missing system dependencies (Playwright, Chromium)
- Test suite failures in `tests/` directory

**This is the first thing to fix in the new session.**

---

## Git Info

- Active repo: `xeverusj/DahshIn` (private)
- Main branch: `main`
- All work merged via: `Merge remote-tracking branch 'research/claude/claude-md-mm49z4...'` (commit `fb94265`, pushed ~26 minutes before this document was written)
- Previous working repo (do not use): `xeverusj/DahshIn-research` (public, staging/research only)

---

## How to Run

```bash
pip install -r requirements.txt
playwright install chromium
python setup.py
streamlit run app.py
```

Default login: `admin@dashin.com` / `admin123`
