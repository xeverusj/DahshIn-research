"""
dashboards/admin_dashboard.py — Dashin Research Platform
Org Admin workspace.
- User management (create, deactivate, change role)
- Client management (create, edit)
- Generate invite links for client portal access
- View pending invites
- Org settings
"""

import streamlit as st
import hashlib
from datetime import datetime, timezone, date
from core.db import get_connection
from core.auth import ROLE_LEVELS, INTERNAL_ROLES
from services.invite_service import (
    create_invite, get_pending_invites, revoke_token,
)

def _rows(cursor_result):
    """Convert list of sqlite3.Row to list of dicts."""
    return [dict(r) for r in cursor_result]

def _row(cursor_result):
    """Convert sqlite3.Row to dict, or return {} if None."""
    return dict(cursor_result) if cursor_result else {}


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

.stApp { background: #F8F7F4; font-family: 'Space Grotesk', sans-serif; }
section[data-testid="stSidebar"] { background: #111 !important; }
section[data-testid="stSidebar"] * { color: #EEE !important; }

.admin-header {
    background: #111;
    border-radius: 10px;
    padding: 22px 28px;
    color: #F8F7F4;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.admin-title { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
.admin-sub   { font-size: 12px; color: #888; margin-top: 3px; }

.user-row {
    background: white;
    border: 1px solid #E8E6E1;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.user-name  { font-weight: 600; font-size: 14px; }
.user-email { font-size: 12px; color: #888; margin-top: 2px; }
.role-chip {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.role-org_admin        { background:#E8F5E9; color:#1B5E20; }
.role-manager          { background:#E3F2FD; color:#0D47A1; }
.role-research_manager { background:#F3E5F5; color:#4A148C; }
.role-campaign_manager { background:#FFF3E0; color:#E65100; }
.role-researcher       { background:#F5F5F5; color:#333; }
.role-client_admin     { background:#FCE4D6; color:#BF360C; }
.role-client_user      { background:#FFF8E1; color:#827717; }

.client-card {
    background: white;
    border: 1px solid #E8E6E1;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.client-name { font-weight: 700; font-size: 15px; }
.client-meta { font-size: 12px; color: #888; margin-top: 4px; }

.invite-card {
    background: #FFFBF0;
    border: 1px solid #FFE082;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.invite-token {
    font-family: monospace;
    background: #F5F5F5;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    word-break: break-all;
}

.stat-chip {
    display: inline-block;
    background: #F0EDE8;
    color: #555;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin-right: 6px;
}
</style>
"""

INTERNAL_ROLE_OPTIONS = [
    "researcher", "campaign_manager", "research_manager",
    "manager", "org_admin",
]
CLIENT_ROLE_OPTIONS = ["client_user", "client_admin"]


def render(user: dict):
    st.markdown(STYLES, unsafe_allow_html=True)

    org_id  = user["org_id"]
    user_id = user["id"]

    # ── Org stats ─────────────────────────────────────────────────────
    conn  = get_connection()
    org   = conn.execute(
        "SELECT * FROM organisations WHERE id=?", (org_id,)
    ).fetchone()
    users = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE org_id=? AND is_active=1",
        (org_id,)
    ).fetchone()["c"]
    clients = conn.execute(
        "SELECT COUNT(*) AS c FROM clients WHERE org_id=? AND is_active=1",
        (org_id,)
    ).fetchone()["c"]
    leads = conn.execute(
        "SELECT COUNT(*) AS c FROM leads WHERE org_id=?", (org_id,)
    ).fetchone()["c"]
    conn.close()

    tier_label = (org["tier"] or "starter").title()

    st.markdown(f"""
    <div class="admin-header">
        <div>
            <div class="admin-title">{org['name']}</div>
            <div class="admin-sub">Admin Panel · {tier_label} Plan</div>
        </div>
        <div>
            <span class="stat-chip">👥 {users} users</span>
            <span class="stat-chip">🏢 {clients} clients</span>
            <span class="stat-chip">🧑 {leads:,} leads</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Users",
        "🏢 Clients",
        "🔗 Invite Links",
        "⚙️ Org Settings",
        "🧠 Site Library",
    ])

    with tab1:
        _render_users(org_id, user_id)
    with tab2:
        _render_clients(org_id, user_id)
    with tab3:
        _render_invites(org_id, user_id)
    with tab4:
        _render_org_settings(org_id, org)
    with tab5:
        from dashboards.site_library_dashboard import render as render_site_lib
        # Admins can re-learn but not delete or mark stable (super_admin only)
        render_site_lib(user, allow_delete=False, allow_mark_stable=False)


# ── USERS ─────────────────────────────────────────────────────────────────────

def _render_users(org_id: int, user_id: int):
    conn  = get_connection()
    users = conn.execute("""
        SELECT u.*, c.name AS client_name
        FROM users u
        LEFT JOIN clients c ON c.id = u.client_id
        WHERE u.org_id=?
        ORDER BY u.role, u.name
    """, (org_id,)).fetchall()
    conn.close()

    st.caption(f"{len(users)} user(s)")

    # Filter
    role_filter = st.selectbox(
        "Filter by role",
        ["All"] + INTERNAL_ROLE_OPTIONS + CLIENT_ROLE_OPTIONS,
        label_visibility="collapsed"
    )
    filtered = [u for u in users
                if role_filter == "All" or u["role"] == role_filter]

    for u in filtered:
        active_badge = "🟢" if u["is_active"] else "🔴"
        client_str   = f" → {u['client_name']}" if u.get("client_name") else ""

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="user-row">
                <div>
                    <div class="user-name">
                        {active_badge} {u['name']}
                    </div>
                    <div class="user-email">
                        {u['email']}{client_str}
                    </div>
                </div>
                <span class="role-chip role-{u['role']}">{u['role'].replace('_',' ')}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if u["id"] != user_id:
                with st.expander("Edit", expanded=False):
                    _render_edit_user(u, org_id)

    st.markdown("---")
    st.subheader("Add User")
    _render_add_user(org_id)


def _render_edit_user(u: dict, org_id: int):
    with st.form(f"edit_user_{u['id']}"):
        new_role = st.selectbox(
            "Role",
            INTERNAL_ROLE_OPTIONS,
            index=INTERNAL_ROLE_OPTIONS.index(u["role"])
            if u["role"] in INTERNAL_ROLE_OPTIONS else 0,
            key=f"er_{u['id']}"
        )
        hourly = st.number_input(
            "Hourly rate (£)",
            value=float(u["hourly_rate"] or 0),
            min_value=0.0, step=0.5,
            key=f"eh_{u['id']}"
        )
        active = st.checkbox("Active", value=bool(u["is_active"]),
                             key=f"ea_{u['id']}")

        if st.form_submit_button("Save"):
            conn = get_connection()
            conn.execute("""
                UPDATE users
                SET role=?, hourly_rate=?, is_active=?
                WHERE id=? AND org_id=?
            """, (new_role, hourly, int(active), u["id"], org_id))
            conn.commit()
            conn.close()
            st.success("Saved!")
            st.rerun()


def _render_add_user(org_id: int):
    conn    = get_connection()
    clients = conn.execute(
        "SELECT id, name FROM clients WHERE org_id=? AND is_active=1",
        (org_id,)
    ).fetchall()
    conn.close()

    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            name     = st.text_input("Full name *")
            email    = st.text_input("Email *")
        with col2:
            password = st.text_input("Password *", type="password",
                                     help="Min 8 characters")
            role     = st.selectbox("Role", INTERNAL_ROLE_OPTIONS,
                                    format_func=lambda x:
                                    x.replace("_"," ").title())

        hourly = st.number_input("Hourly rate (£)", min_value=0.0,
                                  value=0.0, step=0.5)

        if st.form_submit_button("Create User", use_container_width=True):
            if not name or not email or not password:
                st.error("Name, email and password are required.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                try:
                    pw   = hashlib.sha256(password.encode()).hexdigest()
                    conn = get_connection()
                    conn.execute("""
                        INSERT INTO users
                            (org_id, name, email, password, role,
                             hourly_rate, is_active, created_at)
                        VALUES (?,?,?,?,?,?,1,?)
                    """, (org_id, name, email.lower().strip(),
                          pw, role, hourly,
                          datetime.now(timezone.utc).replace(tzinfo=None).isoformat()))
                    conn.commit()
                    conn.close()
                    st.success(f"User {name} created!")
                    st.rerun()
                except Exception as e:
                    if "UNIQUE" in str(e):
                        st.error("That email is already registered.")
                    else:
                        st.error(f"Error: {e}")


# ── CLIENTS ───────────────────────────────────────────────────────────────────

def _render_clients(org_id: int, user_id: int):
    conn    = get_connection()
    clients = conn.execute("""
        SELECT c.*,
               (SELECT COUNT(*) FROM campaigns
                WHERE client_id=c.id)                    AS campaign_count,
               (SELECT COUNT(*) FROM users
                WHERE client_id=c.id AND is_active=1)    AS portal_users
        FROM clients c
        WHERE c.org_id=?
        ORDER BY c.is_active DESC, c.name
    """, (org_id,)).fetchall()
    conn.close()

    for c in clients:
        active = "🟢" if c["is_active"] else "🔴"
        st.markdown(f"""
        <div class="client-card">
            <div style="display:flex;justify-content:space-between;">
                <div>
                    <div class="client-name">{active} {c['name']}</div>
                    <div class="client-meta">
                        {c.get('industry','') or 'No industry set'} ·
                        {c['campaign_count']} campaigns ·
                        {c['portal_users']} portal users
                    </div>
                    {f'<div style="font-size:12px;color:#888;margin-top:4px;">{c["icp_notes"][:80]}…</div>' if c.get('icp_notes') else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Edit client"):
            _render_edit_client(c, org_id)

    st.markdown("---")
    st.subheader("Add Client")
    _render_add_client(org_id)


def _render_edit_client(c: dict, org_id: int):
    with st.form(f"edit_client_{c['id']}"):
        name     = st.text_input("Name", value=c["name"])
        industry = st.text_input("Industry",
                                  value=c.get("industry") or "")
        website  = st.text_input("Website",
                                  value=c.get("website") or "")
        icp      = st.text_area("ICP Notes",
                                 value=c.get("icp_notes") or "",
                                 height=80)
        active   = st.checkbox("Active", value=bool(c["is_active"]))

        if st.form_submit_button("Save Changes"):
            conn = get_connection()
            conn.execute("""
                UPDATE clients
                SET name=?, industry=?, website=?,
                    icp_notes=?, is_active=?
                WHERE id=? AND org_id=?
            """, (name, industry, website, icp,
                  int(active), c["id"], org_id))
            conn.commit()
            conn.close()
            st.success("Client updated!")
            st.rerun()


def _render_add_client(org_id: int):
    with st.form("add_client_form"):
        col1, col2 = st.columns(2)
        with col1:
            name     = st.text_input("Client name *")
            industry = st.text_input("Industry")
        with col2:
            website  = st.text_input("Website")

        icp = st.text_area("ICP / Target Audience Notes",
                            height=80,
                            placeholder="e.g. B2B SaaS companies 50-500 employees, "
                                        "UK/US, looking for VP Sales / Head of Revenue")

        if st.form_submit_button("Add Client", use_container_width=True):
            if not name.strip():
                st.error("Client name is required.")
            else:
                conn = get_connection()
                conn.execute("""
                    INSERT INTO clients
                        (org_id, name, industry, website,
                         icp_notes, is_active, created_at)
                    VALUES (?,?,?,?,?,1,?)
                """, (org_id, name, industry, website, icp,
                      datetime.now(timezone.utc).replace(tzinfo=None).isoformat()))
                conn.commit()
                conn.close()
                st.success(f"Client '{name}' added!")
                st.rerun()


# ── INVITE LINKS ──────────────────────────────────────────────────────────────

def _render_invites(org_id: int, user_id: int):
    # Pending invites
    pending = get_pending_invites(org_id)

    if pending:
        st.subheader(f"Active Invite Links ({len(pending)})")
        for inv in pending:
            import os
            base = os.getenv("DASHIN_BASE_URL", "http://localhost:8501")
            url  = f"{base}/?invite={inv['token']}"

            st.markdown(f"""
            <div class="invite-card">
                <div style="font-weight:600;margin-bottom:6px;">
                    {inv.get('client_name','Unknown Client')} —
                    {inv.get('role','client_user').replace('_',' ').title()}
                </div>
                <div class="invite-token">{url}</div>
                <div style="font-size:11px;color:#888;margin-top:6px;">
                    Created by {inv.get('created_by_name','?')} ·
                    Expires {(inv.get('expires_at',''))[:10]}
                    {f'· Pre-filled: {inv["email"]}' if inv.get('email') else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Revoke", key=f"rev_{inv['id']}",
                             type="secondary"):
                    revoke_token(inv["id"], org_id)
                    st.rerun()
            with col2:
                st.code(url, language=None)

        st.markdown("---")

    # Generate new invite
    st.subheader("Generate New Invite Link")

    conn    = get_connection()
    clients = conn.execute(
        "SELECT id, name FROM clients WHERE org_id=? AND is_active=1 ORDER BY name",
        (org_id,)
    ).fetchall()
    conn.close()

    if not clients:
        st.info("Add a client first before generating invite links.")
        return

    with st.form("gen_invite_form"):
        client_map = {c["name"]: c["id"] for c in clients}
        client_sel = st.selectbox("Client", list(client_map.keys()))
        role       = st.selectbox(
            "Role",
            CLIENT_ROLE_OPTIONS,
            format_func=lambda x: x.replace("_", " ").title(),
            help="Client Admin can manage team members within their account."
        )
        email_hint = st.text_input(
            "Pre-fill email (optional)",
            placeholder="jane@company.com"
        )
        expiry_days = st.slider("Link valid for (days)", 1, 30, 7)

        if st.form_submit_button("Generate Link",
                                  use_container_width=True):
            result = create_invite(
                org_id      = org_id,
                client_id   = client_map[client_sel],
                created_by  = user_id,
                role        = role,
                email       = email_hint.strip() or None,
                expiry_days = expiry_days,
            )
            st.success("Invite link generated!")
            st.code(result["invite_url"], language=None)
            st.caption(f"Expires: {result['expires_at'][:10]}")
            st.info("Share this link with your client. "
                    "It works once and expires in "
                    f"{expiry_days} days.")
            st.rerun()


# ── ORG SETTINGS ─────────────────────────────────────────────────────────────

def _render_org_settings(org_id: int, org):
    conn = get_connection()

    st.subheader("Organisation Settings")

    with st.form("org_settings_form"):
        name = st.text_input("Organisation name", value=org["name"])
        slug = st.text_input("Slug (URL-friendly)", value=org["slug"],
                             help="Lowercase letters and hyphens only")

        st.markdown("---")
        st.markdown("**Plan & Limits** *(read-only — contact Dashin to change)*")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tier", org["tier"].title())
        col2.metric("AI Budget", f"${org['ai_budget_usd']:.0f}/mo")
        col3.metric("Max Users", str(org["max_users"]))

        billing_day = st.number_input(
            "Billing anniversary day",
            min_value=1, max_value=28,
            value=int(org["billing_day"] or 1),
            help="Day of month when AI usage resets"
        )

        if st.form_submit_button("Save Settings"):
            conn.execute("""
                UPDATE organisations
                SET name=?, slug=?, billing_day=?
                WHERE id=?
            """, (name, slug.lower().strip(), billing_day, org_id))
            conn.commit()
            st.success("Settings saved!")
            st.rerun()

    conn.close()
