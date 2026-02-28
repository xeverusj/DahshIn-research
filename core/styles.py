"""
core/styles.py — Dashin Research Platform
Master design system. Single source of truth for all shared visual styles.
All dashboards call inject_shared_css() from here instead of defining their own fonts,
base layout, buttons, badges, tables, and shared components.
"""

import streamlit as st

# ── CSS CUSTOM PROPERTIES + SHARED COMPONENTS ─────────────────────────────────
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700;900&display=swap');

/* ── CSS VARIABLES ──────────────────────────────────────────────────────── */
:root {
    --bg:           #F7F6F3;
    --surface:      #FFFFFF;
    --surface-2:    #F8F7F4;
    --border:       #E8E4DD;
    --border-light: #F0EDE8;

    --text-1: #1A1917;
    --text-2: #555555;
    --text-3: #999999;

    --accent:        #C9A96E;
    --accent-bg:     rgba(201,169,110,.08);
    --accent-border: rgba(201,169,110,.25);

    --success:        #3D9E6A;
    --success-bg:     #ECF7F0;
    --success-border: #B8DFC8;

    --error:        #D45050;
    --error-bg:     #FDECEA;
    --error-border: #F0B8B8;

    --info:        #4A6CF7;
    --info-bg:     #EEF1FF;
    --info-border: #C0CEFF;

    --purple:        #7C3AED;
    --purple-bg:     #F3F0FF;
    --purple-border: #D0C0FF;

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 4px rgba(0,0,0,.05);
    --shadow-md: 0 2px 12px rgba(0,0,0,.08);
}

/* ── BASE ────────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-1) !important;
}
.main .block-container {
    background: var(--bg) !important;
    padding: 2rem 2.5rem !important;
    max-width: 1280px !important;
}

/* ── NORMALIZE ALL DASHBOARD HEADER BARS ─────────────────────────────────── */
/* Overrides the per-dashboard header bars to be visually identical */
.rq-header, .rm-header, .cb-header, .cm-header,
.admin-header, .est-header, .sa-header {
    background: var(--text-1) !important;
    border-radius: var(--radius-md) !important;
    padding: 20px 28px !important;
    color: #F7F6F3 !important;
    margin-bottom: 24px !important;
    display: flex !important;
    align-items: flex-start !important;
    justify-content: space-between !important;
}

/* Header title text — unified Playfair serif */
.rq-header-title, .rm-title, .cb-title,
.cm-title, .admin-title, .est-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
    color: #F7F6F3 !important;
}

/* Header subtitle text */
.rq-header-sub, .rm-sub, .cb-sub,
.cm-sub, .admin-sub, .est-sub {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    color: #888 !important;
    margin-top: 5px !important;
    font-weight: 400 !important;
    letter-spacing: 0 !important;
}

/* ── PAGE TITLES (clean header without dark bar) ─────────────────────────── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--text-1);
    letter-spacing: -0.5px;
    margin-bottom: 4px;
    line-height: 1.2;
}
.page-sub {
    font-size: 13px;
    color: var(--text-3);
    margin-bottom: 24px;
    line-height: 1.5;
}

/* ── SECTION HEADERS ─────────────────────────────────────────────────────── */
.sec-hd, .sec-header {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--text-1);
    margin: 28px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── STAT CARDS ──────────────────────────────────────────────────────────── */
.stat-row { display: flex; gap: 14px; margin-bottom: 28px; flex-wrap: wrap; }
.stat-card {
    flex: 1;
    min-width: 130px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    box-shadow: var(--shadow-sm);
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--text-1);
    line-height: 1;
}
.stat-label {
    font-size: 10px;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 5px;
    font-weight: 600;
}
.stat-note { font-size: 11px; margin-top: 5px; font-weight: 600; }
.note-green { color: var(--success); }
.note-gold  { color: var(--accent);  }
.note-blue  { color: var(--info);    }
.note-red   { color: var(--error);   }
.note-grey  { color: var(--text-3);  }

/* ── KPI CARDS ───────────────────────────────────────────────────────────── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    text-align: center;
    box-shadow: var(--shadow-sm);
}
.kpi-val {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--text-1);
}
.kpi-label {
    font-size: 10px;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
    font-weight: 600;
}

/* ── PANELS ──────────────────────────────────────────────────────────────── */
.panel, .launch-box, .camp-selector {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-sm);
}
.filter-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
}

/* ── CARDS ───────────────────────────────────────────────────────────────── */
.card, .camp-card, .task-card, .task-review-card, .list-card, .user-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow .15s;
}
.card, .camp-card { padding: 18px 22px; }
.task-card, .task-review-card { padding: 16px 20px; }
.list-card { padding: 18px 20px; }
.user-row  { padding: 14px 18px; display: flex; align-items: center; justify-content: space-between; }
.card:hover, .camp-card:hover, .task-card:hover { box-shadow: var(--shadow-md); }

/* Task card priority left-border accent */
.task-card { border-left: 4px solid var(--border); }
.task-card.urgent { border-left-color: var(--error); }
.task-card.normal { border-left-color: var(--accent); }
.task-card.low    { border-left-color: var(--success); }

/* Card text elements */
.card-title, .task-title, .camp-title, .task-review-title { font-weight: 600; color: var(--text-1); font-size: 15px; margin-bottom: 3px; }
.camp-title { font-size: 17px; font-weight: 700; }
.camp-client { font-size: 11px; color: var(--accent); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }
.card-meta, .task-meta, .camp-meta { font-size: 12px; color: var(--text-3); margin-top: 5px; }
.task-meta span { margin-right: 16px; }
.user-name  { font-weight: 600; font-size: 14px; color: var(--text-1); }
.user-email { font-size: 12px; color: var(--text-3); margin-top: 2px; }

/* ── LIST CARDS ──────────────────────────────────────────────────────────── */
.list-card-name { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: var(--text-1); margin-bottom: 2px; }
.list-card-meta { font-size: 11px; color: var(--text-3); margin-bottom: 8px; }
.list-card-desc { font-size: 12px; color: var(--text-2); line-height: 1.5; }

/* ── DETAIL PANEL ────────────────────────────────────────────────────────── */
.detail-panel { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 24px; margin-bottom: 16px; box-shadow: var(--shadow-sm); }
.detail-name  { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: var(--text-1); margin-bottom: 4px; }
.detail-sub   { font-size: 13px; color: var(--text-3); margin-bottom: 20px; }
.detail-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.detail-field { background: var(--surface-2); border-radius: 7px; padding: 12px 14px; }
.detail-field-label { font-size: 9px; color: var(--text-3); text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin-bottom: 4px; }
.detail-field-val   { font-size: 13px; color: var(--text-1); font-weight: 500; }

/* ── TABLE ───────────────────────────────────────────────────────────────── */
.tbl {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
}
.tbl table { width: 100%; border-collapse: collapse; font-size: 12px; }
.tbl th {
    background: var(--surface-2);
    padding: 10px 16px;
    text-align: left;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    border-bottom: 1px solid var(--border);
}
.tbl td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--border-light);
    color: var(--text-2);
    vertical-align: middle;
    line-height: 1.4;
}
.tbl td.n  { color: var(--text-1); font-weight: 600; font-size: 13px; }
.tbl td.co { color: var(--text-2); font-weight: 500; }
.tbl tr:last-child td { border-bottom: none; }
.tbl tr:hover td { background: var(--surface-2); }

/* ── BADGES ──────────────────────────────────────────────────────────────── */
.badge, .status-badge, .priority-badge, .status-pill, .role-chip, .chip {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif !important;
}
.status-badge { padding: 3px 12px; font-size: 10px; }
.status-pill  { padding: 3px 10px; font-size: 10px; }
.role-chip, .chip { padding: 3px 10px; font-size: 10px; border-radius: 12px; }

/* Lead status */
.b-new      { background: var(--info-bg);    color: var(--info);    border: 1px solid var(--info-border); }
.b-assigned { background: var(--accent-bg);  color: var(--accent);  border: 1px solid var(--accent-border); }
.b-progress { background: var(--purple-bg);  color: var(--purple);  border: 1px solid var(--purple-border); }
.b-enriched { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.b-used     { background: #F5F5F5;           color: #888;           border: 1px solid #DDD; }
.b-archived { background: var(--text-1);     color: var(--accent);  border: 1px solid #3A3530; }

/* Task / general status */
.status-pending, .s-pending  { background: #F5F5F5;           color: #777;           border: 1px solid #E0E0E0; }
.status-in_progress          { background: var(--info-bg);    color: var(--info);    border: 1px solid var(--info-border); }
.status-submitted            { background: #FFF3E0;           color: #B45309;        border: 1px solid #FDE68A; }
.status-approved             { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.status-rejected             { background: var(--error-bg);   color: var(--error);   border: 1px solid var(--error-border); }

/* Campaign status */
.s-building  { background: var(--info-bg);    color: var(--info);    border: 1px solid var(--info-border); }
.s-active    { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.s-paused    { background: #FFF3E0;           color: #B45309;        border: 1px solid #FDE68A; }
.s-ready     { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.s-completed { background: var(--purple-bg);  color: var(--purple);  border: 1px solid var(--purple-border); }
.s-closed    { background: #F5F5F5;           color: #888;           border: 1px solid #E0E0E0; }

/* Scraper session status */
.b-run  { background: var(--accent-bg);  color: var(--accent);  border: 1px solid var(--accent-border); }
.b-done { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.b-fail { background: var(--error-bg);   color: var(--error);   border: 1px solid var(--error-border); }

/* Priority */
.priority-urgent, .p-urgent { background: var(--error-bg);   color: var(--error);   border: 1px solid var(--error-border); }
.priority-normal, .p-normal { background: var(--accent-bg);  color: var(--accent);  border: 1px solid var(--accent-border); }
.priority-low,    .p-low    { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }

/* Persona */
.p-dm  { background: rgba(212,80,80,.08);   color: var(--error);   border: 1px solid rgba(212,80,80,.15); }
.p-si  { background: var(--accent-bg);      color: var(--accent);  border: 1px solid var(--accent-border); }
.p-inf { background: rgba(74,108,247,.08);  color: var(--info);    border: 1px solid rgba(74,108,247,.15); }
.p-ic  { background: rgba(61,158,106,.08);  color: var(--success); border: 1px solid rgba(61,158,106,.15); }
.p-unk { background: #F5F5F5; color: var(--text-3); }

/* Role chips — identical to sidebar sb-role palette */
.chip-super_admin,      .role-super_admin      { background: rgba(201,169,110,.18); color: #9A7030; border: 1px solid rgba(201,169,110,.3); }
.chip-org_admin,        .role-org_admin        { background: rgba(201,169,110,.12); color: #8A6020; border: 1px solid rgba(201,169,110,.22); }
.chip-manager,          .role-manager          { background: rgba(74,108,247,.10);  color: #3A4FD0; border: 1px solid rgba(74,108,247,.2); }
.chip-research_manager, .role-research_manager { background: rgba(124,58,237,.10);  color: #6020C0; border: 1px solid rgba(124,58,237,.2); }
.chip-campaign_manager, .role-campaign_manager { background: rgba(180,83,9,.10);    color: #904010; border: 1px solid rgba(180,83,9,.2); }
.chip-researcher,       .role-researcher       { background: rgba(61,158,106,.10);  color: #2A7040; border: 1px solid rgba(61,158,106,.2); }
.chip-client_admin,     .role-client_admin     { background: rgba(212,80,80,.10);   color: #A02828; border: 1px solid rgba(212,80,80,.2); }
.chip-client_user,      .role-client_user      { background: rgba(184,148,60,.10);  color: #805818; border: 1px solid rgba(184,148,60,.2); }

/* CRM contact statuses (campaign manager) */
.s-new               { background: #F5F5F5;           color: #666;           border: 1px solid #E0E0E0; }
.s-contacted         { background: var(--info-bg);    color: #2F52C2;        border: 1px solid var(--info-border); }
.s-waiting           { background: #FFF9EC;            color: #8D6E0A;        border: 1px solid #F0D97A; }
.s-responded         { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.s-interested        { background: #EEF6FF;            color: #1A6FA8;        border: 1px solid #BFD9F2; }
.s-meeting_requested { background: #FFF3E0;            color: #B45309;        border: 1px solid #FDE68A; }
.s-booked            { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }
.s-not_interested    { background: var(--error-bg);   color: var(--error);   border: 1px solid var(--error-border); }
.s-no_show           { background: var(--purple-bg);  color: var(--purple);  border: 1px solid var(--purple-border); }

/* ── TIP / ALERT BOXES ───────────────────────────────────────────────────── */
.tip, .alert-warn {
    background: #FFFDF5;
    border: 1px solid #E8D5A8;
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    font-size: 12px;
    color: #8A7040;
    margin: 12px 0;
    line-height: 1.5;
}
.alert-err, .conflict-warn {
    background: var(--error-bg);
    border: 1px solid var(--error-border);
    border-left: 3px solid var(--error);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 12px;
    color: var(--error);
    margin: 8px 0;
}
.alert-ok, .conflict-ok {
    background: var(--success-bg);
    border: 1px solid var(--success-border);
    border-left: 3px solid var(--success);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 12px;
    color: var(--success);
    margin: 8px 0;
}

/* KPI performance indicators (research manager) */
.kpi-good { color: var(--success) !important; font-weight: 600; }
.kpi-warn { color: #B45309 !important; font-weight: 600; }
.kpi-bad  { color: var(--error) !important; font-weight: 600; }

/* ── TERMINAL ────────────────────────────────────────────────────────────── */
.terminal {
    background: #111;
    color: #C8C8C8;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    max-height: 380px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.6;
    margin-top: 12px;
}

/* ── BUTTONS ─────────────────────────────────────────────────────────────── */
div.stButton > button {
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all .15s !important;
    padding: 8px 16px !important;
}
div.stButton > button[kind="primary"] {
    background: var(--text-1) !important;
    color: #FFF !important;
    border: none !important;
}
div.stButton > button[kind="primary"]:hover {
    background: var(--accent) !important;
}
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--text-1) !important;
    border: 1px solid var(--border) !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── FORM ELEMENTS ───────────────────────────────────────────────────────── */
div.stTextInput input,
div.stTextArea textarea,
div.stNumberInput input {
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
    background: var(--surface-2) !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-1) !important;
    padding: 10px 14px !important;
}
div.stTextInput input:focus,
div.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-bg) !important;
}
div[data-baseweb="select"] > div {
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
    background: var(--surface-2) !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── TABS ────────────────────────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-3) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--text-1) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── STREAMLIT NATIVE COMPONENTS ─────────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm) !important;
}
div[data-testid="metric-container"] label { color: var(--text-3) !important; font-size: 12px !important; }
div[data-testid="stMetricValue"] { color: var(--text-1) !important; font-weight: 700 !important; }

div[data-testid="stDataFrame"] th { background: var(--surface-2) !important; color: var(--text-1) !important; border-color: var(--border) !important; }
div[data-testid="stDataFrame"] td { color: var(--text-2) !important; border-color: var(--border-light) !important; }

details         { background: var(--surface) !important; border-color: var(--border) !important; border-radius: var(--radius-sm) !important; }
details summary { color: var(--text-1) !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }

div[data-testid="stAlert"] { border-radius: var(--radius-sm) !important; }

/* ── ORG / PLATFORM CARDS (superadmin) ───────────────────────────────────── */
.org-card, .platform-stat {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
}
.org-name  { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: var(--text-1); margin-bottom: 3px; }
.org-meta  { font-size: 12px; color: var(--text-3); }

/* ── COST CARDS (estimator) ──────────────────────────────────────────────── */
.cost-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px;
    text-align: center;
    box-shadow: var(--shadow-sm);
}
.cost-num {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--text-1);
}
.cost-num.green { color: var(--success); }
.cost-num.gold  { color: var(--accent); }
.cost-label {
    font-size: 11px;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}
.breakdown-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
}
.breakdown-row:last-child { border-bottom: none; }

/* ── CAMPAIGN BANNERS ────────────────────────────────────────────────────── */
.ready-banner {
    background: var(--success-bg);
    border: 1.5px solid var(--success-border);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.not-ready-banner {
    background: #FFFBF0;
    border: 1px dashed var(--accent);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin: 10px 0;
}
.lead-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
}
.lead-row:last-child { border-bottom: none; }

/* ── KPI TABLE (research manager) ────────────────────────────────────────── */
.kpi-table {
    background: var(--surface);
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
}
.kpi-table-header {
    background: var(--text-1);
    color: #F7F6F3;
    padding: 10px 16px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr 1fr;
    gap: 8px;
}
.kpi-table-row {
    padding: 12px 16px;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr 1fr;
    gap: 8px;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
    align-items: center;
}
.kpi-table-row:last-child { border-bottom: none; }
.kpi-table-row:hover { background: var(--surface-2); }

/* ── CRM TABLE (campaign manager) ────────────────────────────────────────── */
.crm-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    background: var(--surface);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}
.crm-table th {
    background: var(--text-1);
    color: var(--accent);
    padding: 10px 14px;
    text-align: left;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.crm-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-light);
    color: var(--text-2);
    vertical-align: middle;
}
.crm-table tr:last-child td { border-bottom: none; }
.crm-table tr:hover td { background: var(--surface-2); }

/* ── CLIENT CARDS (admin) ────────────────────────────────────────────────── */
.client-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
}
.invite-token {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    color: var(--text-2);
    word-break: break-all;
}
</style>
"""


def inject_shared_css():
    """
    Inject the master design system CSS.
    Call this at the start of every dashboard's render() function.
    """
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
