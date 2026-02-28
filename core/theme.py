"""
core/theme.py — Dashin Research Platform
Shared light / dark theme CSS injected globally from app.py.
Overrides use !important to beat per-dashboard STYLES.
Targets both Streamlit built-in components and custom HTML classes.
"""

import streamlit as st

DARK_CSS = """
<style>
/* ── DARK THEME ─────────────────────────────────────────────────────── */

/* App background */
.stApp { background: #0D0D0D !important; color: #C8C4BE !important; }
.main .block-container { background: #0D0D0D !important; }

/* Base text — only headings and paragraphs, not every div (avoids killing badge colors) */
.stApp p { color: #C8C4BE !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: #F0EDE8 !important; }
.stApp a  { color: #C9A96E !important; }

/* Streamlit labels / captions */
.stApp label                          { color: #AAA !important; }
div[data-testid="stCaptionContainer"] { color: #666 !important; }

/* ── Streamlit native components ──────────────────────────────────────── */

/* Metrics */
div[data-testid="metric-container"] {
    background: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 8px !important;
}
div[data-testid="metric-container"] label { color: #777 !important; }
div[data-testid="stMetricValue"]          { color: #F0EDE8 !important; }

/* Inputs */
div.stTextInput input,
div.stTextArea textarea,
div.stNumberInput input {
    background: #1A1A1A !important;
    border-color: #333 !important;
    color: #F0EDE8 !important;
}
div[data-baseweb="select"] > div {
    background: #1A1A1A !important;
    border-color: #333 !important;
    color: #F0EDE8 !important;
}
div.stCheckbox label span { color: #C8C4BE !important; }

/* Dataframe */
div[data-testid="stDataFrame"]    { background: #1A1A1A !important; }
div[data-testid="stDataFrame"] th { background: #222 !important; color: #C9A96E !important; }
div[data-testid="stDataFrame"] td { color: #C8C4BE !important; }

/* Expander */
details         { background: #1A1A1A !important; border-color: #2A2A2A !important; }
details summary { color: #C9A96E !important; }

/* Tabs */
button[data-baseweb="tab"]                           { color: #777 !important; }
button[data-baseweb="tab"][aria-selected="true"]     { color: #C9A96E !important; border-bottom-color: #C9A96E !important; }

/* Alerts */
div[data-testid="stAlert"] { background: #1A1A1A !important; border-color: #2A2A2A !important; }

/* Secondary buttons */
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #C8C4BE !important;
    border-color: #444 !important;
}

/* ── Custom HTML classes (scraper / inventory / research dashboards) ── */

/* Page titles & subtitles */
.page-title, .sec-header, .sec-hd { color: #F0EDE8 !important; border-color: #2A2A2A !important; }
.page-sub                          { color: #666 !important; }

/* Stat cards */
.stat-card  { background: #1A1A1A !important; border-color: #2A2A2A !important; }
.stat-val   { color: #F0EDE8 !important; }
.stat-label { color: #666 !important; }
.stat-note  { color: #C9A96E !important; }

/* General white panels / boxes */
.launch-box  { background: #1A1A1A !important; border-color: #2A2A2A !important; }
.filter-bar  { background: #1A1A1A !important; border-color: #2A2A2A !important; }
.detail-panel{ background: #1A1A1A !important; border-color: #2A2A2A !important; }
.list-card   { background: #1A1A1A !important; border-color: #2A2A2A !important; }

/* Detail panel text */
.detail-name      { color: #F0EDE8 !important; }
.detail-sub       { color: #888 !important; }
.detail-field     { background: #222 !important; }
.detail-field-label{ color: #666 !important; }
.detail-field-val  { color: #F0EDE8 !important; }

/* List card text */
.list-card-name { color: #F0EDE8 !important; }
.list-card-meta { color: #666 !important; }
.list-card-desc { color: #C8C4BE !important; }

/* HTML table (custom .tbl) */
.tbl              { background: #1A1A1A !important; border-color: #2A2A2A !important; }
.tbl th           { background: #222 !important; color: #C9A96E !important; border-color: #2A2A2A !important; }
.tbl td           { color: #C8C4BE !important; border-color: #1E1E1E !important; }
.tbl td.n         { color: #F0EDE8 !important; }
.tbl td.co        { color: #AAA !important; }
.tbl tr:hover td  { background: #222 !important; }

/* Tip / info boxes */
.tip { background: #1A1800 !important; border-color: #4A3800 !important; color: #C9A96E !important; }

/* Campaign / research cards */
.card, .r-card, .q-card, .camp-card {
    background: #1A1A1A !important;
    border-color: #2A2A2A !important;
}
.card-title, .r-card-title, .q-card-title { color: #F0EDE8 !important; }
.card-meta,  .r-card-meta,  .q-card-meta  { color: #666 !important; }

/* Superadmin org cards */
.org-card  { background: #141414 !important; border-color: #2A2A2A !important; }
.org-name  { color: #F0EDE8 !important; }
.org-meta  { color: #555 !important; }

/* Platform stat boxes */
.platform-stat { background: #141414 !important; border-color: #2A2A2A !important; }
</style>
"""

LIGHT_CSS = """
<style>
/* ── LIGHT THEME ─────────────────────────────────────────────────────── */

/* App background — restore defaults overridden when switching from dark */
.stApp { background: #F7F6F3 !important; color: #1A1917 !important; }
.main .block-container { background: #F7F6F3 !important; }

/* Streamlit inputs — restore light styling */
div.stTextInput input,
div.stTextArea textarea,
div.stNumberInput input {
    background: #FAF9F7 !important;
    border-color: #E0DBD4 !important;
    color: #1A1917 !important;
}
div[data-baseweb="select"] > div {
    background: #FAF9F7 !important;
    border-color: #E0DBD4 !important;
    color: #1A1917 !important;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
}
div[data-testid="metric-container"] label { color: #888 !important; }
div[data-testid="stMetricValue"]          { color: #1A1917 !important; }

/* Dataframe */
div[data-testid="stDataFrame"]    { background: #FFFFFF !important; }
div[data-testid="stDataFrame"] th { background: #F0EDE8 !important; color: #1A1917 !important; }
div[data-testid="stDataFrame"] td { color: #1A1917 !important; }

/* Expander */
details         { background: #FFFFFF !important; border-color: #E8E6E1 !important; }
details summary { color: #1A1917 !important; }

/* Tabs */
button[data-baseweb="tab"]                           { color: #999 !important; }
button[data-baseweb="tab"][aria-selected="true"]     { color: #1A1917 !important; border-bottom-color: #C9A96E !important; }

/* Secondary buttons */
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #1A1917 !important;
    border-color: #D0CCC5 !important;
}
</style>
"""


def apply_theme() -> bool:
    """
    Inject the current theme CSS into the page.
    Returns True if dark mode is active.
    Called once per render from app.py.
    """
    dark = st.session_state.get("dark_mode", False)
    st.markdown(DARK_CSS if dark else LIGHT_CSS, unsafe_allow_html=True)
    return dark
