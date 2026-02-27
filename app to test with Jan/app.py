"""
app.py — Dashin Research Platform V2
Entry point. Run with: streamlit run app.py

Roles and their nav:
  super_admin       → Super Admin panel + all internal views
  org_admin         → All internal views + Admin panel
  manager           → Scraper, Inventory, Campaigns, Estimator, Research queue
  research_manager  → Research queue, Research manager view, Inventory
  campaign_manager  → Campaign manager view, Campaigns
  researcher        → Research queue, Inventory (own leads only)
  client_admin      → Full client portal
  client_user       → Full client portal
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from core.db import init_db, migrate_db, ensure_defaults, get_connection

# ── STARTUP SECURITY CHECK ────────────────────────────────────────────────────
def _check_committed_secrets():
    """Warn if the ANTHROPIC_API_KEY may have been committed to git history."""
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    if api_key.startswith('sk-ant-'):
        try:
            result = subprocess.run(
                ['git', 'log', '--all', '--full-history', '--', '.env'],
                capture_output=True, text=True, timeout=5,
                cwd=Path(__file__).parent
            )
            if result.stdout.strip():
                logging.warning(
                    "WARNING: .env appears to have been committed to git history. "
                    "Rotate your ANTHROPIC_API_KEY immediately at https://console.anthropic.com"
                )
                print(
                    "\n⚠️  SECURITY WARNING: .env may have been committed to git history.\n"
                    "   Rotate your ANTHROPIC_API_KEY at: https://console.anthropic.com\n"
                )
        except Exception:
            pass  # git not available or timeout — skip silently

_check_committed_secrets()

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title  = "Dashin Research",
    page_icon   = "⚡",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #F7F6F3 !important;
}
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111111 !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 24px 18px 20px;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #888 !important;
    font-size: 12px !important;
}
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: transparent !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    width: 100% !important;
    cursor: pointer !important;
    color: #777 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all .12s !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #1E1E1E !important;
    color: #DDD !important;
}

/* Main content area */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1280px !important;
    background: #F7F6F3 !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all .15s !important;
}
div.stButton > button[kind="primary"] {
    background: #1A1917 !important;
    color: #FFF !important;
    border: none !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #C9A96E !important;
}
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #1A1917 !important;
    border: 1px solid #D0CCC5 !important;
}

/* Text inputs */
div.stTextInput input {
    border: 1px solid #E0DBD4 !important;
    border-radius: 7px !important;
    background: #FAF9F7 !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    color: #1A1917 !important;
}
div.stTextInput input:focus {
    border-color: #C9A96E !important;
    box-shadow: 0 0 0 3px rgba(201,169,110,.12) !important;
}

/* Sidebar components */
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: #FFF;
    padding-bottom: 16px;
    margin-bottom: 12px;
    border-bottom: 1px solid #222;
    letter-spacing: -0.5px;
}
.sb-logo span { color: #C9A96E; }

.sb-user {
    font-size: 11px;
    color: #555;
    margin-bottom: 16px;
    line-height: 1.7;
}
.sb-user strong { color: #999; font-weight: 600; }

.sb-role {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}
.sb-role-super_admin     { background:rgba(201,169,110,.2); color:#C9A96E; }
.sb-role-org_admin       { background:rgba(201,169,110,.15); color:#B8943C; }
.sb-role-manager         { background:rgba(100,160,255,.15); color:#64A0FF; }
.sb-role-research_manager{ background:rgba(180,100,255,.15); color:#B464FF; }
.sb-role-campaign_manager{ background:rgba(255,160,50,.15);  color:#FFA032; }
.sb-role-researcher      { background:rgba(100,200,130,.15); color:#64C882; }
.sb-role-client_admin    { background:rgba(255,100,100,.15); color:#FF6464; }
.sb-role-client_user     { background:rgba(255,180,50,.15);  color:#FFB432; }

.sb-org {
    font-size: 10px;
    color: #444;
    font-style: italic;
    margin-top: 2px;
}

.sb-div {
    border: none;
    border-top: 1px solid #1E1E1E;
    margin: 12px 0;
}

.sb-notif {
    background: #C9A96E;
    color: #111;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 700;
    display: inline-block;
    margin-left: 6px;
}
</style>
""", unsafe_allow_html=True)


# ── NAV DEFINITIONS ───────────────────────────────────────────────────────────
# Maps display label → page key → which roles can see it

NAV_ITEMS = [
    # (label, page_key, allowed_roles)
    ("⚡  Platform",         "superadmin",   {"super_admin"}),
    ("🔍  Smart Scraper",    "scraper",      {"super_admin","org_admin","manager","researcher"}),
    ("📦  Inventory",        "inventory",    {"super_admin","org_admin","manager","research_manager","researcher"}),
    ("🔬  Research Queue",   "research",     {"super_admin","org_admin","manager","research_manager","researcher"}),
    ("📋  Research Manager", "res_manager",  {"super_admin","org_admin","manager","research_manager"}),
    ("🚀  Campaigns",        "campaigns",    {"super_admin","org_admin","manager","campaign_manager"}),
    ("📊  Campaign Manager", "camp_manager", {"super_admin","org_admin","manager","campaign_manager"}),
    ("💰  Estimator",        "estimator",    {"super_admin","org_admin","manager"}),
    ("⚙️  Admin",            "admin",        {"super_admin","org_admin"}),
]

CLIENT_NAV_ITEMS = [
    ("🏠  Home",             "client_home"),
    ("👥  My Leads",         "client_leads"),
    ("📁  Campaigns",        "client_campaigns"),
    ("📎  Files",            "client_files"),
    ("💬  Notes",            "client_notes"),
]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

def render_sidebar(user: dict) -> str:
    """Render sidebar and return selected page key."""
    role     = user.get("role", "researcher")
    is_client = role in ("client_admin", "client_user")

    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sb-logo">Dashin<span>.</span></div>
        """, unsafe_allow_html=True)

        # User info
        org_name = user.get("org_name", "")
        client_name = user.get("client_name", "")
        display_context = client_name if is_client else org_name

        st.markdown(f"""
        <div class="sb-user">
            <strong>{user['name']}</strong><br>
            {user['email']}<br>
            <span class="sb-role sb-role-{role}">{role.replace('_',' ')}</span>
            <div class="sb-org">{display_context}</div>
        </div>
        <hr class="sb-div">
        """, unsafe_allow_html=True)

        # Notification count — cached 30s to avoid a DB round-trip on every rerun
        try:
            import time as _time
            _uid = user["id"]
            _ck  = f"_unread_{_uid}"
            _ct  = f"_unread_ts_{_uid}"
            if _time.time() - st.session_state.get(_ct, 0) > 30:
                from services.notification_service import unread_count as _uc
                st.session_state[_ck] = _uc(_uid)
                st.session_state[_ct] = _time.time()
            n = st.session_state.get(_ck, 0)
            if n > 0:
                st.markdown(
                    f'<div style="margin-bottom:8px;">'
                    f'🔔 <span class="sb-notif">{n} new</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        except Exception as _notif_err:
            logging.warning(f"[app.sidebar] unread_count: {_notif_err}")

        # Navigation
        if is_client:
            nav_labels = [item[0] for item in CLIENT_NAV_ITEMS]
            nav_keys   = [item[1] for item in CLIENT_NAV_ITEMS]
        else:
            visible = [(label, key)
                       for label, key, roles in NAV_ITEMS
                       if role in roles]
            nav_labels = [item[0] for item in visible]
            nav_keys   = [item[1] for item in visible]

        if not nav_labels:
            st.warning("No pages available for your role.")
            return "none"

        # Keep selected page in session state
        if "page" not in st.session_state:
            st.session_state["page"] = nav_keys[0]

        # If current page not in nav (e.g. after role change), reset
        if st.session_state["page"] not in nav_keys:
            st.session_state["page"] = nav_keys[0]

        current_idx = nav_keys.index(st.session_state["page"])
        choice = st.radio(
            "Navigation",
            nav_labels,
            index=current_idx,
            label_visibility="collapsed",
        )
        selected_key = nav_keys[nav_labels.index(choice)]
        st.session_state["page"] = selected_key

        st.markdown('<hr class="sb-div">', unsafe_allow_html=True)

        if st.button("Sign Out", use_container_width=True):
            for k in ["user", "org_id", "page"]:
                st.session_state.pop(k, None)
            st.rerun()

    return selected_key


# ── ROUTER ────────────────────────────────────────────────────────────────────

def route(page: str, user: dict):
    """Route to the correct dashboard based on page key and role."""
    role = user.get("role", "researcher")

    # ── Client portal (completely separate visual) ─────────────────────
    if role in ("client_admin", "client_user"):
        from dashboards.client_dashboard import render
        render(user)
        return

    # ── Super admin ────────────────────────────────────────────────────
    if page == "superadmin":
        if role != "super_admin":
            _access_denied()
            return
        from dashboards.superadmin_dashboard import render
        render(user)

    # ── Smart Scraper ──────────────────────────────────────────────────
    elif page == "scraper":
        if role not in ("super_admin","org_admin","manager","researcher"):
            _access_denied(); return
        try:
            from dashboards.scraper_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Scraper", e)

    # ── Inventory ─────────────────────────────────────────────────────
    elif page == "inventory":
        try:
            from dashboards.inventory_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Inventory", e)

    # ── Research Queue ─────────────────────────────────────────────────
    elif page == "research":
        try:
            from dashboards.research_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Research Queue", e)

    # ── Research Manager ───────────────────────────────────────────────
    elif page == "res_manager":
        if role not in ("super_admin","org_admin","manager","research_manager"):
            _access_denied(); return
        try:
            from dashboards.research_manager_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Research Manager", e)

    # ── Campaigns ─────────────────────────────────────────────────────
    elif page == "campaigns":
        if role not in ("super_admin","org_admin","manager","campaign_manager"):
            _access_denied(); return
        try:
            from dashboards.campaigns_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Campaigns", e)

    # ── Campaign Manager ───────────────────────────────────────────────
    elif page == "camp_manager":
        if role not in ("super_admin","org_admin","manager","campaign_manager"):
            _access_denied(); return
        try:
            from dashboards.campaign_manager_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Campaign Manager", e)

    # ── Estimator ─────────────────────────────────────────────────────
    elif page == "estimator":
        if role not in ("super_admin","org_admin","manager"):
            _access_denied(); return
        try:
            from dashboards.estimator_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Estimator", e)

    # ── Admin ──────────────────────────────────────────────────────────
    elif page == "admin":
        if role not in ("super_admin","org_admin"):
            _access_denied(); return
        try:
            from dashboards.admin_dashboard import render
            render(user)
        except Exception as e:
            _dashboard_error("Admin", e)

    else:
        st.info(f"Page '{page}' not found.")


def _access_denied():
    st.error("🚫 You don't have permission to access this page.")


def _dashboard_error(name: str, err: Exception):
    st.error(f"⚠ {name} dashboard failed to load.")
    with st.expander("Error details"):
        st.code(str(err))
    import traceback
    with st.expander("Traceback"):
        st.code(traceback.format_exc())


# ── LOGIN / SIGNUP ────────────────────────────────────────────────────────────

def render_login(invite_token: str = None):
    """Login page — or signup form if invite token present."""

    # Centered layout
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("""
        <div style="max-width:400px;margin:0 auto;background:white;
                    border:1px solid #E8E4DD;border-radius:14px;
                    padding:40px;box-shadow:0 4px 24px rgba(0,0,0,.06);
                    margin-top:60px;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;
                        font-weight:700;color:#1A1917;margin-bottom:4px;">
                Dashin<span style="color:#C9A96E;">.</span>
            </div>
            <div style="font-size:13px;color:#999;margin-bottom:28px;">
                Research Operations Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        if invite_token:
            _render_signup(invite_token)
        else:
            _render_login_form()


def _render_login_form():
    with st.form("login_form"):
        email    = st.text_input("Email", placeholder="you@company.com")
        password = st.text_input("Password", type="password",
                                  placeholder="••••••••")
        submit   = st.form_submit_button("Sign In",
                                          use_container_width=True,
                                          type="primary")

    if submit:
        if not email or not password:
            st.error("Please enter your email and password.")
            return
        from core.auth import login, set_session
        user = login(email, password)
        if user:
            set_session(user)
            st.rerun()
        else:
            st.error("Invalid email or password, or account is inactive.")

    st.markdown(
        '<p style="text-align:center;font-size:11px;color:#BBB;margin-top:12px;">'
        'Default: admin@dashin.com / admin123'
        '</p>',
        unsafe_allow_html=True
    )


def _render_signup(token: str):
    """Self-serve signup form shown when following an invite link."""
    from services.invite_service import validate_token, redeem_token
    from core.auth import login, set_session

    invite = validate_token(token)
    if not invite:
        st.error("This invite link is invalid or has expired. "
                 "Please contact your account manager.")
        if st.button("Back to Sign In"):
            st.query_params.clear()
            st.rerun()
        return

    st.subheader(f"Create your account")
    st.caption(
        f"You're joining **{invite.get('client_name', 'your team')}** "
        f"as {invite.get('role','client_user').replace('_',' ').title()}"
    )

    with st.form("signup_form"):
        name      = st.text_input("Your full name *")
        email_val = invite.get("email") or ""
        email     = st.text_input(
            "Email *",
            value=email_val,
            disabled=bool(email_val)
        )
        password  = st.text_input("Password *", type="password",
                                   help="Minimum 8 characters")
        confirm   = st.text_input("Confirm password *", type="password")
        submit    = st.form_submit_button("Create Account",
                                           use_container_width=True,
                                           type="primary")

    if submit:
        errors = []
        if not name.strip():          errors.append("Name is required.")
        if not email.strip():         errors.append("Email is required.")
        if len(password) < 8:         errors.append("Password must be at least 8 characters.")
        if password != confirm:        errors.append("Passwords don't match.")

        if errors:
            for e in errors:
                st.error(e)
            return

        result = redeem_token(token, name, email, password)
        if result["success"]:
            user = login(email, password)
            if user:
                set_session(user)
                st.query_params.clear()
                st.rerun()
        else:
            st.error(result["error"])


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    # Initialise DB on every cold start
    init_db()
    migrate_db()
    ensure_defaults()

    # Check for invite token in URL params
    params = st.query_params
    invite_token = params.get("invite")

    # Not logged in
    if "user" not in st.session_state:
        render_login(invite_token=invite_token)
        return

    user = st.session_state["user"]

    # Re-validate user is still active (catch deactivations)
    conn = get_connection()
    live = conn.execute(
        "SELECT is_active, role FROM users WHERE id=?",
        (user["id"],)
    ).fetchone()
    conn.close()

    if not live or not live["is_active"]:
        st.session_state.pop("user", None)
        st.error("Your account has been deactivated. "
                 "Please contact your administrator.")
        st.stop()

    # Sync role if changed by admin
    if live["role"] != user.get("role"):
        user["role"] = live["role"]
        st.session_state["user"] = user

    # Render
    page = render_sidebar(user)
    route(page, user)


if __name__ == "__main__":
    main()