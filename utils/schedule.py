import streamlit as st
import os
from streamlit_lottie import st_lottie
import pandas as pd
from datetime import datetime, date, time


SCHEDULED_CSV = "scheduled.csv"

# Does the CSV exist and are the headers correct?
def init_csv():
    if not os.path.exists(SCHEDULED_CSV):
        df = pd.DataFrame(columns=["title", "message", "date", "time"])
        df.to_csv(SCHEDULED_CSV, index=False)


# Append the new scheduled notification
def save_scheduled_notification(title, message, selected_date, selected_time):
    new_entry = pd.DataFrame([{
        "title": title,
        "message": message,
        "date": selected_date,
        "time": selected_time
    }])
    new_entry.to_csv(SCHEDULED_CSV, mode='a', header=not os.path.exists(SCHEDULED_CSV), index=False)


# Load the current schedule
def load_scheduled_notifications():
    if os.path.exists(SCHEDULED_CSV):
        return pd.read_csv(SCHEDULED_CSV)
    return pd.DataFrame(columns=["title", "message", "date", "time"])

def show_schedule_page():
    init_csv()
    st.title("Schedule Push Notification")

    st.markdown("Hi Zia, you'll use this form to schedule a notification to be sent at a future date and time.")

    with st.form("schedule_form"):
        title = st.text_input("Notification Title")
        message = st.text_area("Notification Message")
        scheduled_date = st.date_input("Date", value=date.today())
        scheduled_time = st.time_input("Time", value=datetime.now().time())

        submitted = st.form_submit_button("Schedule Notification")
        if submitted:
            if title and message:
                save_scheduled_notification(title, message, scheduled_date, scheduled_time)
                st.success(f"Scheduled for {scheduled_date} at {scheduled_time}")
            else:
                st.error("Please fill in all fields.")


    # Show any of the current scheduled items
    st.markdown("___")
    st.subheader("Current Scheduled Notifications")

    scheduled_df = load_scheduled_notifications()
    if not scheduled_df.empty:
        st.dataframe(scheduled_df, use_container_width=True)
    else:
        st.info("No scheduled notifications found.")