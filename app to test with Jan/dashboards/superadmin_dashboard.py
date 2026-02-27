"""
dashboards/superadmin_dashboard.py — Dashin Research Platform
Super Admin only. Full platform visibility.
- All organisations + usage
- AI cost per org + platform total
- Create / suspend orgs
- Change tier / limits
- Light / Dark mode toggle
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from core.db import get_connection
from core.ai_tracker import (
    get_all_org_usage, get_platform_summary,
    get_monthly_trend, get_feature_breakdown,
)

TIERS = ["scraper", "starter", "growth", "agency", "enterprise"]
TIER_BUDGETS = {
    "scraper": 3.0, "starter": 8.0,
    "growth": 20.0, "agency": 50.0, "enterprise": 200.0,
}
TIER_LIMITS = {
    "scraper":    (1,  0,   5000),
    "starter":    (5,  3,   10000),
    "growth":     (15, 10,  50000),
    "agency":     (9999, 9999, 9999999),
    "enterprise": (9999, 9999, 9999999),
}

# ── THEME ─────────────────────────────────────────────────────────────────────

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Manrope:wght@300;400;600;700&display=swap');

.stApp { background: #0D0D0D !important; font-family: 'Manrope', sans-serif; color: #F0EDE8; }
.main .block-container { background: #0D0D0D !important; }

/* Force text colour in dark mode */
.stApp p, .stApp label, .stApp span, .stApp div { color: #C8C4BE; }
.stApp h1,.stApp h2,.stApp h3 { color: #F0EDE8 !important; }

/* Metrics */
div[data-testid="metric-container"] {
    background: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 8px !important;
    padding: 14px !important;
}
div[data-testid="metric-container"] label { color: #777 !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #F0EDE8 !important; }

/* Selectbox, inputs */
div[data-baseweb="select"] > div { background: #1A1A1A !important; border-color: #333 !important; }
div.stTextInput input, div.stTextArea textarea, div.stNumberInput input {
    background: #1A1A1A !important;
    border-color: #333 !important;
    color: #F0EDE8 !important;
}
div.stCheckbox label span { color: #C8C4BE !important; }

/* Expander */
details { background: #1A1A1A !important; border-color: #2A2A2A !important; }
details summary { color: #C9A96E !important; }

/* Tabs */
button[data-baseweb="tab"] { color: #777 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #C9A96E !important; border-bottom-color: #C9A96E !important; }

/* Dataframe */
div[data-testid="stDataFrame"] { background: #1A1A1A !important; }

/* Caption */
div[data-testid="stCaptionContainer"] { color: #666 !important; }

.sa-header {
    background: linear-gradient(135deg, #141414, #1E1E1E);
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 24px;
}
.sa-title { font-family: 'JetBrains Mono', monospace; font-size: 18px;
            font-weight: 600; color: #F0EDE8; letter-spacing: -0.3px; }
.sa-badge { background: #C9A96E; color: #0A0A0A; padding: 3px 12px;
            border-radius: 20px; font-size: 11px; font-weight: 700;
            letter-spacing: 1px; text-transform: uppercase; }
.sa-sub   { font-size: 12px; color: #555; margin-top: 4px; }

.org-card { background: #141414; border: 1px solid #2A2A2A;
            border-radius: 8px; padding: 16px 20px; margin-bottom: 10px; }
.org-card:hover { border-color: #444; }
.org-name  { font-weight: 700; font-size: 15px; color: #F0EDE8; }
.org-meta  { font-size: 12px; color: #555; margin-top: 4px;
             font-family: 'JetBrains Mono', monospace; }

.tier-chip { display:inline-block; padding:2px 10px; border-radius:12px;
             font-size:11px; font-weight:700; text-transform:uppercase; }
.tier-scraper    { background:#1A1A2E; color:#4FC3F7; }
.tier-starter    { background:#1A2E1A; color:#81C784; }
.tier-growth     { background:#2E1A1A; color:#FFB74D; }
.tier-agency     { background:#2A1A2E; color:#CE93D8; }
.tier-enterprise { background:#2E2A1A; color:#C9A96E; }

.ai-bar-wrap { background:#1E1E1E; border-radius:4px; height:6px;
               margin-top:8px; overflow:hidden; }
.ai-bar-fill { height:100%; border-radius:4px; transition:width 0.3s; }
.ai-green  { background:#4CAF50; }
.ai-yellow { background:#FFC107; }
.ai-red    { background:#F44336; }

.platform-stat { background:#141414; border:1px solid #2A2A2A;
                 border-radius:8px; padding:18px; text-align:center; }
.platform-num  { font-family:'JetBrains Mono',monospace; font-size:28px;
                 font-weight:600; color:#C9A96E; }
.platform-label { font-size:11px; color:#555; text-transform:uppercase;
                  letter-spacing:0.5px; margin-top:4px; }
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Manrope:wght@300;400;600;700&display=swap');

.stApp { background: #F7F6F3 !important; font-family: 'Manrope', sans-serif; color: #1A1917; }
.main .block-container { background: #F7F6F3 !important; }

.stApp h1,.stApp h2,.stApp h3 { color: #1A1917 !important; }

div[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
    border-radius: 8px !important;
    padding: 14px !important;
}

.sa-header {
    background: linear-gradient(135deg, #1A1917, #2C2A27);
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 24px;
    color: #F0EDE8;
}
.sa-title { font-family: 'JetBrains Mono', monospace; font-size: 18px;
            font-weight: 600; color: #F0EDE8; letter-spacing: -0.3px; }
.sa-badge { background: #C9A96E; color: #1A1917; padding: 3px 12px;
            border-radius: 20px; font-size: 11px; font-weight: 700;
            letter-spacing: 1px; text-transform: uppercase; }
.sa-sub   { font-size: 12px; color: #AAA; margin-top: 4px; }

.org-card { background: #FFFFFF; border: 1px solid #E8E6E1;
            border-radius: 8px; padding: 16px 20px; margin-bottom: 10px; }
.org-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
.org-name  { font-weight: 700; font-size: 15px; color: #1A1917; }
.org-meta  { font-size: 12px; color: #888; margin-top: 4px;
             font-family: 'JetBrains Mono', monospace; }

.tier-chip { display:inline-block; padding:2px 10px; border-radius:12px;
             font-size:11px; font-weight:700; text-transform:uppercase; }
.tier-scraper    { background:#E3F2FD; color:#0277BD; }
.tier-starter    { background:#E8F5E9; color:#2E7D32; }
.tier-growth     { background:#FFF3E0; color:#E65100; }
.tier-agency     { background:#F3E5F5; color:#6A1B9A; }
.tier-enterprise { background:#FFF8E1; color:#8D6E0A; }

.ai-bar-wrap { background:#F0EDE8; border-radius:4px; height:6px;
               margin-top:8px; overflow:hidden; }
.ai-bar-fill { height:100%; border-radius:4px; transition:width 0.3s; }
.ai-green  { background:#4CAF50; }
.ai-yellow { background:#FFC107; }
.ai-red    { background:#F44336; }

.platform-stat { background:#FFFFFF; border:1px solid #E8E6E1;
                 border-radius:8px; padding:18px; text-align:center; }
.platform-num  { font-family:'JetBrains Mono',monospace; font-size:28px;
                 font-weight:600; color:#C9A96E; }
.platform-label { font-size:11px; color:#999; text-transform:uppercase;
                  letter-spacing:0.5px; margin-top:4px; }
</style>
"""


def _r(row):
    """Convert sqlite3.Row (or dict) to plain dict safely."""
    if row is None:
        return {}
    if isinstance(row, dict):
        return row
    return dict(row)


def render(user: dict):
    # ── Theme toggle ──────────────────────────────────────────────────
    if "sa_dark_mode" not in st.session_state:
        st.session_state["sa_dark_mode"] = True

    dark = st.session_state["sa_dark_mode"]
    st.markdown(DARK_CSS if dark else LIGHT_CSS, unsafe_allow_html=True)

    # Toggle button in top-right via columns
    header_col, toggle_col = st.columns([8, 1])
    with toggle_col:
        label = "☀ Light" if dark else "🌙 Dark"
        if st.button(label, key="theme_toggle", use_container_width=True):
            st.session_state["sa_dark_mode"] = not dark
            st.rerun()

    with header_col:
        st.markdown(f"""
        <div class="sa-header">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="sa-title">⚡ Dashin Platform</div>
                    <div class="sa-sub">Super Admin · {date.today().strftime('%d %b %Y')}</div>
                </div>
                <span class="sa-badge">Super Admin</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏢 All Orgs",
        "💰 AI Costs",
        "➕ New Org",
        "📊 Platform Stats",
        "🧠 Site Library",
        "💾 Backups",
    ])

    with tab1:
        _render_all_orgs(dark)
    with tab2:
        _render_ai_costs(dark)
    with tab3:
        _render_new_org()
    with tab4:
        _render_platform_stats(dark)
    with tab5:
        from dashboards.site_library_dashboard import render as render_site_lib
        render_site_lib(user, allow_delete=True, allow_mark_stable=True)
    with tab6:
        _render_backup_ui()


# ── ALL ORGS ──────────────────────────────────────────────────────────────────

def _render_all_orgs(dark: bool = True):
    conn = get_connection()
    rows = conn.execute("""
        SELECT o.*,
               (SELECT COUNT(*) AS c FROM users
                WHERE org_id=o.id AND is_active=1
                  AND role NOT IN ('client_admin','client_user')) AS user_count,
               (SELECT COUNT(*) AS c FROM clients
                WHERE org_id=o.id AND is_active=1)               AS client_count,
               (SELECT COUNT(*) AS c FROM leads
                WHERE org_id=o.id)                               AS lead_count,
               (SELECT COUNT(*) AS c FROM campaigns
                WHERE org_id=o.id)                               AS campaign_count
        FROM organisations o
        ORDER BY o.is_active DESC, o.created_at DESC
    """).fetchall()
    conn.close()

    # Convert ALL rows to dict immediately — no more sqlite3.Row anywhere below
    orgs = [dict(r) for r in rows]

    usage_by_org = {u["org_id"]: u for u in get_all_org_usage()}

    active = sum(1 for o in orgs if o.get("is_active"))
    st.caption(f"{active} active / {len(orgs)} total organisations")

    tier_filter = st.selectbox(
        "Filter by tier",
        ["All"] + TIERS,
        label_visibility="collapsed",
        format_func=lambda x: x.title()
    )

    for org in orgs:
        if tier_filter != "All" and org.get("tier") != tier_filter:
            continue

        u           = usage_by_org.get(org["id"], {})
        pct         = u.get("pct_used", 0) or 0
        bar_cls     = ("ai-red" if pct >= 80 else
                       "ai-yellow" if pct >= 60 else "ai-green")
        active_icon = "🟢" if org.get("is_active") else "🔴"
        alert       = " ⚠" if u.get("alert_80_sent") else ""
        budget      = org.get("ai_budget_usd") or 0
        cost        = u.get("cost_usd") or 0

        st.markdown(f"""
        <div class="org-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div class="org-name">{active_icon} {org.get('name','')}</div>
                        <span class="tier-chip tier-{org.get('tier','starter')}">{org.get('tier','')}</span>
                    </div>
                    <div class="org-meta">
                        👥 {org.get('user_count',0)} users ·
                        🏢 {org.get('client_count',0)} clients ·
                        🧑 {org.get('lead_count',0):,} leads ·
                        📁 {org.get('campaign_count',0)} campaigns
                    </div>
                </div>
                <div style="text-align:right;min-width:140px;">
                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:13px;color:#C9A96E;">
                        ${cost:.3f} / ${budget:.0f}{alert}
                    </div>
                    <div style="font-size:11px;color:#666;">AI this period</div>
                    <div class="ai-bar-wrap">
                        <div class="ai-bar-fill {bar_cls}"
                             style="width:{min(pct,100):.0f}%"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"Manage — {org.get('name','')}"):
            _render_org_editor(org)


def _render_org_editor(org: dict):
    """org must already be a plain dict."""
    org_id = org.get("id")

    with st.form(f"edit_org_{org_id}"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name",
                                  value=org.get("name") or "",
                                  key=f"on_{org_id}")
            current_tier = org.get("tier") or "starter"
            tier = st.selectbox(
                "Tier", TIERS,
                index=TIERS.index(current_tier)
                      if current_tier in TIERS else 1,
                key=f"ot_{org_id}",
                format_func=lambda x: x.title()
            )
        with col2:
            ai_budget = st.number_input(
                "AI Budget ($/month)",
                value=float(org.get("ai_budget_usd") or 8.0),
                min_value=0.0, step=1.0,
                key=f"oai_{org_id}"
            )
            is_active = st.checkbox(
                "Active",
                value=bool(org.get("is_active", 1)),
                key=f"oa_{org_id}"
            )

        max_users = st.number_input(
            "Max users",
            value=int(org.get("max_users") or 5),
            min_value=1,
            key=f"ou_{org_id}"
        )
        notes = st.text_area(
            "Admin notes",
            value=org.get("notes") or "",
            height=60,
            key=f"onotes_{org_id}"
        )

        col_save, col_fill = st.columns([1, 2])
        with col_save:
            saved = st.form_submit_button("Save", use_container_width=True)
        with col_fill:
            st.form_submit_button("Apply Tier Defaults (save to apply)",
                                   use_container_width=True)

        if saved:
            conn = get_connection()
            conn.execute("""
                UPDATE organisations
                SET name=?, tier=?, ai_budget_usd=?,
                    is_active=?, max_users=?, notes=?,
                    suspended_at=?
                WHERE id=?
            """, (name, tier, ai_budget, int(is_active),
                  max_users, notes,
                  None if is_active else datetime.utcnow().isoformat(),
                  org_id))
            conn.commit()
            conn.close()
            st.success("Saved!")
            st.rerun()


# ── AI COSTS ──────────────────────────────────────────────────────────────────

def _render_ai_costs(dark: bool = True):
    summary   = get_platform_summary()
    all_usage = get_all_org_usage()

    c1, c2, c3, c4 = st.columns(4)

    total_budget = sum(u.get("budget_usd", 0) or 0 for u in all_usage)
    over_80      = sum(1 for u in all_usage if (u.get("pct_used") or 0) >= 80)
    total_tokens = (summary.get("total_input", 0) or 0) + \
                   (summary.get("total_output", 0) or 0)

    for col, (num, label) in zip(
        [c1, c2, c3, c4],
        [
            (f"${summary.get('total_cost', 0):.2f}", "Platform Cost This Month"),
            (f"${total_budget:.0f}",                  "Total Budget Allocated"),
            (str(over_80),                             "Orgs Over 80%"),
            (f"{total_tokens/1_000_000:.1f}M",         "Total Tokens This Month"),
        ]
    ):
        with col:
            st.markdown(f"""
            <div class="platform-stat" style="margin-bottom:12px;">
                <div class="platform-num">{num}</div>
                <div class="platform-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    if all_usage:
        df = pd.DataFrame([{
            "Organisation": u.get("org_name", ""),
            "Tier":         (u.get("tier") or "").title(),
            "Used ($)":     round(u.get("cost_usd") or 0, 4),
            "Budget ($)":   u.get("budget_usd") or 0,
            "Used %":       f"{u.get('pct_used') or 0}%",
            "Alert Sent":   "⚠ Yes" if u.get("alert_80_sent") else "No",
            "Period Start": (u.get("period_start") or "")[:10],
        } for u in sorted(all_usage,
                          key=lambda x: x.get("pct_used") or 0,
                          reverse=True)])
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Per-Org Breakdown")

    conn = get_connection()
    org_rows = conn.execute(
        "SELECT id, name FROM organisations WHERE is_active=1 ORDER BY name"
    ).fetchall()
    orgs = [dict(r) for r in org_rows]
    conn.close()

    if orgs:
        org_map  = {o["name"]: o["id"] for o in orgs}
        selected = st.selectbox("Select org", list(org_map.keys()))
        org_id   = org_map[selected]

        from core.ai_tracker import get_billing_period
        conn2 = get_connection()
        org_row = conn2.execute(
            "SELECT billing_day FROM organisations WHERE id=?", (org_id,)
        ).fetchone()
        conn2.close()

        if org_row:
            period_start, _ = get_billing_period(dict(org_row).get("billing_day", 1))
            breakdown = get_feature_breakdown(org_id, period_start)
            if breakdown:
                df2 = pd.DataFrame([{
                    "Feature":   (b.get("feature") or "").title(),
                    "API Calls": b.get("calls") or 0,
                    "Tokens In": f"{b.get('tokens_in') or 0:,}",
                    "Tokens Out":f"{b.get('tokens_out') or 0:,}",
                    "Cost ($)":  round(b.get("cost") or 0, 4),
                } for b in breakdown])
                st.dataframe(df2, use_container_width=True, hide_index=True)
            else:
                st.info("No AI usage recorded for this org yet.")

        trend = get_monthly_trend(org_id, months=6)
        if trend:
            df3 = pd.DataFrame(trend)
            if "period_start" in df3.columns and "cost_usd" in df3.columns:
                df3 = df3.set_index("period_start")
                st.line_chart(df3["cost_usd"], use_container_width=True)


# ── NEW ORG ───────────────────────────────────────────────────────────────────

def _render_new_org():
    st.subheader("Create New Organisation")
    st.caption("Creates the org and a default admin user.")

    with st.form("new_org_form"):
        col1, col2 = st.columns(2)
        with col1:
            org_name  = st.text_input("Organisation name *")
            slug      = st.text_input("Slug *",
                                       help="Lowercase letters and hyphens only")
            tier      = st.selectbox("Plan tier", TIERS, index=1,
                                      format_func=lambda x: x.title())
        with col2:
            admin_name  = st.text_input("Admin name *")
            admin_email = st.text_input("Admin email *")
            admin_pass  = st.text_input("Admin password *", type="password",
                                         help="Min 8 chars")

        billing_day = st.number_input("Billing day", min_value=1,
                                       max_value=28, value=1)
        notes       = st.text_area("Notes", height=60)

        if st.form_submit_button("Create Organisation",
                                  use_container_width=True):
            errors = []
            if not org_name.strip():   errors.append("Org name required")
            if not slug.strip():       errors.append("Slug required")
            if not admin_name.strip(): errors.append("Admin name required")
            if not admin_email.strip():errors.append("Admin email required")
            if len(admin_pass) < 8:    errors.append("Password min 8 chars")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                defaults = TIER_LIMITS.get(tier, (5, 3, 10000))
                budget   = TIER_BUDGETS.get(tier, 8.0)
                now      = datetime.utcnow().isoformat()
                conn     = get_connection()
                try:
                    cur = conn.execute("""
                        INSERT INTO organisations
                            (name, slug, tier, ai_budget_usd, billing_day,
                             max_users, max_clients, max_leads,
                             is_active, notes, created_at)
                        VALUES (?,?,?,?,?,?,?,?,1,?,?)
                    """, (org_name, slug.lower().strip(), tier,
                          budget, billing_day,
                          defaults[0], defaults[1], defaults[2],
                          notes, now))
                    new_org_id = cur.lastrowid

                    import hashlib
                    pw = hashlib.sha256(admin_pass.encode()).hexdigest()
                    conn.execute("""
                        INSERT INTO users
                            (org_id, name, email, password, role, is_active, created_at)
                        VALUES (?,?,?,?,'org_admin',1,?)
                    """, (new_org_id, admin_name,
                          admin_email.lower().strip(), pw, now))

                    conn.commit()
                    st.success(f"✅ Organisation '{org_name}' created! "
                               f"Admin: {admin_email}")
                except Exception as e:
                    if "UNIQUE" in str(e):
                        st.error("Slug or email already exists.")
                    else:
                        st.error(f"Error: {e}")
                finally:
                    conn.close()


# ── PLATFORM STATS ────────────────────────────────────────────────────────────

def _render_platform_stats(dark: bool = True):
    conn = get_connection()

    def _count(q, *args):
        return conn.execute(q, args).fetchone()["c"]

    total_orgs     = _count("SELECT COUNT(*) AS c FROM organisations")
    active_orgs    = _count("SELECT COUNT(*) AS c FROM organisations WHERE is_active=1")
    total_users    = _count("SELECT COUNT(*) AS c FROM users WHERE is_active=1")
    total_leads    = _count("SELECT COUNT(*) AS c FROM leads")
    total_enriched = _count("SELECT COUNT(*) AS c FROM enrichment WHERE email IS NOT NULL")
    total_campaigns= _count("SELECT COUNT(*) AS c FROM campaigns")
    total_scrapes  = _count("SELECT COUNT(*) AS c FROM scrape_sessions WHERE status='done'")
    ai_savings     = _count("SELECT COUNT(*) AS c FROM scrape_sessions WHERE pattern_used=1")

    tier_rows = conn.execute("""
        SELECT tier, COUNT(*) AS c FROM organisations
        WHERE is_active=1 GROUP BY tier ORDER BY c DESC
    """).fetchall()
    tier_data = [dict(r) for r in tier_rows]

    conn.close()

    stats = [
        ("Active Orgs",       active_orgs),
        ("Total Orgs",        total_orgs),
        ("Active Users",      total_users),
        ("Total Leads",       f"{total_leads:,}"),
        ("Emails Enriched",   f"{total_enriched:,}"),
        ("Campaigns",         total_campaigns),
        ("Scrape Sessions",   total_scrapes),
        ("AI-Saved Sessions", ai_savings),
    ]

    cols = st.columns(4)
    for i, (label, value) in enumerate(stats):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="platform-stat" style="margin-bottom:12px;">
                <div class="platform-num">{value}</div>
                <div class="platform-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    if tier_data:
        st.markdown("---")
        st.subheader("Orgs by Tier")
        df = pd.DataFrame([{
            "Tier":  (r.get("tier") or "").title(),
            "Count": r.get("c") or 0,
        } for r in tier_data])
        st.bar_chart(df.set_index("Tier"))


# ── BACKUP ────────────────────────────────────────────────────────────────────

def _render_backup_ui():
    from datetime import datetime as _dt
    from core.db import backup_database, list_backups

    st.subheader("Database Backups")
    st.caption("Backups are stored in `data/backups/` and are safe to run while the app is live.")

    col_btn, col_label = st.columns([1, 3])
    with col_btn:
        do_backup = st.button("💾 Create Backup Now", use_container_width=True)
    with col_label:
        label = st.text_input("Label (optional)", placeholder="pre-migration", label_visibility="collapsed")

    if do_backup:
        try:
            dest = backup_database(label=label.strip())
            st.success(f"Backup created: `{dest.name}`")
        except Exception as e:
            st.error(f"Backup failed: {e}")

    st.markdown("---")
    st.subheader("Existing Backups")

    backups = list_backups()
    if not backups:
        st.info("No backups found. Create one above.")
        return

    for b in backups:
        created = _dt.fromtimestamp(b["created_at"]).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.markdown(
            f"**{b['name']}** &nbsp;·&nbsp; {b['size_kb']} KB &nbsp;·&nbsp; {created}",
            unsafe_allow_html=True,
        )
