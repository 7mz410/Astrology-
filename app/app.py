# /app/app.py

import os
# The .env loading is now handled inside config.py, so we don't need it here.

import sys
import streamlit as st
import time
from datetime import time as dt_time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orchestration.main_orchestrator import MainOrchestrator

st.set_page_config(page_title="Planets Vibe Bot", page_icon="🔮", layout="centered")

@st.cache_resource
def get_orchestrator():
    return MainOrchestrator()
orchestrator = get_orchestrator()

# --- Session State ---
if 'is_generating' not in st.session_state: st.session_state.is_generating = False

# --- UI Layout ---
st.image("assets/visual_identity/channel_logo.png", width=150)
st.title("Planets Vibe Content Bot")
st.caption("Your Autonomous Astrology Content Agent ✨")
st.divider()

# --- 1. Connection Section ---
st.header("1. Connect Your Instagram Account")
insta_status = orchestrator.get_instagram_status()

if insta_status.get("is_logged_in"):
    st.success(f"Connected as: **{insta_status.get('username')}**")
    if st.button("Logout from Instagram"):
        orchestrator.logout_from_instagram()
        st.toast("Logged out successfully.")
        time.sleep(1); st.rerun()
else:
    st.info("Please log in to your Instagram account to enable posting.")
    with st.form("login_form"):
        username = st.text_input("Instagram Username")
        password = st.text_input("Instagram Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                with st.spinner("Logging in..."):
                    result = orchestrator.login_to_instagram(username, password)
                if result.get("success"):
                    st.success("Login successful!")
                    time.sleep(1); st.rerun()
                else:
                    st.error(f"Login Failed: {result.get('message')}")

st.divider()

# --- 2. Generation Section (Only visible if logged in) ---
if insta_status.get("is_logged_in"):
    st.header("2. Generate & Post Content")
    
    # Automation Control Section
    st.subheader("Daily Automation")
    schedule_time = st.time_input("Scheduled Time (UTC)", value=dt_time(10, 30))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Daily Automation", use_container_width=True):
            run_time_str = schedule_time.strftime("%H:%M")
            orchestrator.start_automation(run_time_str)
            st.success(f"Automation started! Posts will be generated daily at {run_time_str} UTC.")
    with col2:
        if st.button("⏹️ Stop Automation", use_container_width=True):
            orchestrator.stop_automation()
            st.warning("Automation stopped.")

    st.subheader("Manual Generation")
    # --- MODIFIED: Changed the function name called by the button ---
    if st.button("🔮 Generate & Post Today's 12 Posts Now", use_container_width=True, type="primary"):
        with st.spinner("Generating & Publishing 12 astrology posts... This will take several minutes."):
            posts = orchestrator.generate_and_publish_all_astrology_posts() # <-- The change is here
        
        if posts and len(posts) > 0:
            st.success(f"Successfully published {len(posts)} posts to Instagram!")
            st.balloons()
        else:
            st.error("Process failed. Check the terminal for details.")
