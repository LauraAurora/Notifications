import hashlib
import streamlit as st
from streamlit_lottie import st_lottie
import json
import os
from utils.notification import send_notification_page
from utils.schedule import show_schedule_page
import os

# --------------------------------------------------------------------
# COSMETICS
# --------------------------------------------------------------------
json_path = os.path.join("assets", "wine.json")
with open("assets/wine.json", "r") as f:
    wine_lottie = json.load(f)


# man_lottie_url = "https://raw.githubusercontent.com/LauraAurora/Lottie_Assets/main/Animation%20-%201747177633984.json"
# man_lottie = load_lottie_url(man_lottie_url)

# --------------------------------------------------------------------
# CONFIG / SECRETS
# --------------------------------------------------------------------  
def _secret(key, default=None):
    return st.secrets.get(key, default) if hasattr(st, "secrets") else os.getenv(key, default)

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
    st.subheader("Login to send an Notification")
    
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        if user == ADMIN_USER and pwd_hash == ADMIN_HASH:
            st.success("Login successful! Loading your dashboard...")
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password.")
    

    st_lottie(wine_lottie, height=300, key="wine-login-footer")


# --------------------------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------------------------
if st.session_state.authenticated:
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Send Now", "Schedule"])

    if page == "Send Now":
        send_notification_page()
    elif page == "Schedule":
        show_schedule_page()
else:
    login()