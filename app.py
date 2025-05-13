import hashlib
import os
import streamlit as st
import requests

# --------------------------------------------------------------------
# CONFIG / SECRETS
# --------------------------------------------------------------------
def _secret(key, default=None):
    return st.secrets.get(key, default) if hasattr(st, "secrets") else os.getenv(key, default)

APILIX_ENDPOINT = "https://api.apilix.com/send-notification"   # ← use exact path from docs
APILIX_API_KEY  = _secret("APILIX_API_KEY", "")
TEST_MODE       = _secret("TEST_MODE", "false").lower() == "true"           # True = simulate only

ADMIN_USER      = _secret("ADMIN_USER")
ADMIN_HASH      = _secret("ADMIN_PASS_HASH")

if not (ADMIN_USER and ADMIN_HASH):
    st.error("Missing ADMIN_USER or ADMIN_PASS_HASH in secrets. Add them to secrets.toml or env vars.")
    st.stop()


# --------------------------------------------------------------------
# SESSION FLAG
# --------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# --------------------------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------------------------
def login():
    st.title("Hi there, Zia!")
    st.subheader("Please Login")
    
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        if user == ADMIN_USER and pwd_hash == ADMIN_HASH:
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")


# --------------------------------------------------------------------
# NOTIFICATION PAGE
# --------------------------------------------------------------------
def send_notification():
    st.title("Send Push Notification")

    title = st.text_input("Notification Title")
    message = st.text_area("Notification Message")

    if st.button("Send Notification"):
        if TEST_MODE:
            st.success("TEST MODE ON - no call made.")
            st.json({"title": title, "message": message})
        else:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {APILIX_API_KEY}"
            }
            payload = {
                "title": title,
                "message": message,
                "target": "allUsers"
            }

            try:
                response = requests.post(APILIX_ENDPOINT, headers=headers, json=payload, timeout=10)
                if response.ok:
                    st.success("Notification sent to iOS and Android!")
                else:
                    st.error(f"Apilix error {response.status_code}: {response.text}")
            except Exception as exc:
                st.error(f"Request failed: {exc}")


    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()


# --------------------------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------------------------
if not st.session_state.authenticated:
    login()
else:
    send_notification()