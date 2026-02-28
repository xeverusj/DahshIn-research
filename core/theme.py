"""
core/theme.py — Dashin Research Platform
Shared light / dark theme CSS injected globally from app.py.
All overrides use !important so they win over individual dashboard STYLES.
"""

import streamlit as st

DARK_CSS = """
<style>
/* ── DARK THEME ────────────────────────────────────────────────────── */
.stApp {
    background: #0D0D0D !important;
    color: #C8C4BE !important;
}
.main .block-container {
    background: #0D0D0D !important;
}

/* Text */
.stApp p, .stApp label, .stApp span, .stApp div { color: #C8C4BE !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: #F0EDE8 !important; }
.stApp a { color: #C9A96E !important; }

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
div[data-baseweb="select"] option { background: #1A1A1A !important; }
div.stCheckbox label span { color: #C8C4BE !important; }

/* Dataframe / table */
div[data-testid="stDataFrame"]     { background: #1A1A1A !important; }
div[data-testid="stDataFrame"] th  { background: #222 !important; color: #C9A96E !important; }
div[data-testid="stDataFrame"] td  { color: #C8C4BE !important; }

/* Expander */
details                 { background: #1A1A1A !important; border-color: #2A2A2A !important; }
details summary         { color: #C9A96E !important; }

/* Tabs */
button[data-baseweb="tab"]                              { color: #777 !important; }
button[data-baseweb="tab"][aria-selected="true"]        { color: #C9A96E !important; border-bottom-color: #C9A96E !important; }

/* Caption */
div[data-testid="stCaptionContainer"] { color: #666 !important; }

/* Alerts / info boxes */
div[data-testid="stAlert"]            { background: #1A1A1A !important; border-color: #2A2A2A !important; }

/* Buttons */
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #C8C4BE !important;
    border-color: #444 !important;
}
</style>
"""

LIGHT_CSS = """
<style>
/* ── LIGHT THEME ───────────────────────────────────────────────────── */
.stApp {
    background: #F7F6F3 !important;
    color: #1A1917 !important;
}
.main .block-container {
    background: #F7F6F3 !important;
}

/* Text */
.stApp p, .stApp label, .stApp span, .stApp div { color: #1A1917 !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4      { color: #1A1917 !important; }
.stApp a { color: #C9A96E !important; }

/* Metrics */
div[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
    border-radius: 8px !important;
}
div[data-testid="metric-container"] label { color: #888 !important; }
div[data-testid="stMetricValue"]          { color: #1A1917 !important; }

/* Inputs */
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

/* Dataframe / table */
div[data-testid="stDataFrame"]    { background: #FFFFFF !important; }
div[data-testid="stDataFrame"] th { background: #F0EDE8 !important; color: #1A1917 !important; }
div[data-testid="stDataFrame"] td { color: #1A1917 !important; }

/* Expander */
details         { background: #FFFFFF !important; border-color: #E8E6E1 !important; }
details summary { color: #1A1917 !important; }

/* Tabs */
button[data-baseweb="tab"]                           { color: #999 !important; }
button[data-baseweb="tab"][aria-selected="true"]     { color: #1A1917 !important; border-bottom-color: #C9A96E !important; }

/* Buttons */
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
    Should be called once per page render (app.py handles this).
    """
    dark = st.session_state.get("dark_mode", False)
    st.markdown(DARK_CSS if dark else LIGHT_CSS, unsafe_allow_html=True)
    return dark
