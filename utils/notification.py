import streamlit as st
import requests
import os

def _secret(key, default=None):
    return st.secrets.get(key, default) if hasattr(st, "secrets") else os.getenv(key, default)

APILIX_ENDPOINT = "https://api.apilix.com/send-notification"   # ← use exact path from docs
APILIX_API_KEY  = _secret("APILIX_API_KEY", "")
TEST_MODE       = _secret("TEST_MODE", "false").lower() == "true"           # True = simulate only

def send_notification_page():
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