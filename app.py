import streamlit as st
import pandas as pd
import os
import time

# --- APP SETUP ---
st.set_page_config(page_title="Harmony Healer", page_icon="🎵", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Therapy Session", "Admin Data"])

# ==========================================
# PAGE 1: THERAPY SESSION
# ==========================================
if page == "Therapy Session":
    st.title("Harmony Healer 🎵")
    st.subheader("Personalized Music Therapy & Wellness")
    st.write("Welcome. This system uses personalized data to suggest music for your emotional state.")
    
    # 1. User Input
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Enter your name:")
        mood = st.selectbox("How are you feeling?", ["Calm", "Anxiety", "Stress", "Depression", "Sadness"])
    with col2:
        stress = st.slider("Rate your stress level (1-10):", 1, 10, 5)
    
    # 2. The Recommendation Engine
    if st.button("Get Music Recommendation", type="primary"):
        if user_name:
            st.success(f"Hello {user_name}, analyzing your mood: **{mood}**...")
            
            # Load Database
            if os.path.exists("songs.csv"):
                try:
                    df = pd.read_csv("songs.csv")
                    # Clean up spaces in column names
                    df.columns = df.columns.str.strip()
                    
                    # FILTER LOGIC (Case Insensitive)
                    # This fixes the "Sadness" vs "sadness" issue
                    results = df[df['MoodCategory'].str.strip().str.lower() == mood.lower()]
                    
                    if not results.empty:
                        # Pick 1 random song
                        song = results.sample(1).iloc[0]
                        song_title = song['SongTitle']
                        artist = song['Artist']
                        file_path = song['YoutubeLink'].strip()
                        
                        # Display Results
                        st.divider()
                        st.subheader(f"🎧 Prescribed Track: {song_title}")
                        st.write(f"**Artist:** {artist}")
                        
                        # Play Audio (Local File Check)
                        if os.path.exists(file_path):
                            st.audio(file_path)
                        else:
                            st.error(f"⚠️ Error: Could not find the file at '{file_path}'")
                            st.info("Please check your 'music' folder. The filename in songs.csv must match exactly.")
                        
                        # Save Data for Admin (Simulation Study)
                        log_data = f"{user_name},{mood},{stress},{song_title}\n"
                        with open("user_usage_logs.csv", "a") as f:
                            f.write(log_data)
                            
                    else:
                        st.warning(f"No songs found for '{mood}' in the database.")
                        st.info("Check your songs.csv file to ensure this mood category exists.")
                except Exception as e:
                    st.error(f"Error reading database: {e}")
            else:
                st.error("System Error: 'songs.csv' file is missing!")
        else:
            st.warning("Please enter your name to begin the session.")

# 3. Guided Breathing Mode (With Stop Button)
    st.divider()
    with st.expander("🧘 Guided Breathing Mode (Anxiety Relief)"):
        st.write("This feature helps reduce stress using the 4-7-8 technique.")
        
        # Create 2 columns for buttons side-by-side
        col1, col2 = st.columns([1, 5]) # col1 is small, col2 is wide
        
        with col1:
            start_btn = st.button("▶ Start", type="primary")
        with col2:
            stop_btn = st.button("⏹ Stop / Reset")
        
        # Create a container for the timer so it can be cleared
        animation_placeholder = st.empty()

        # STOP BUTTON LOGIC
        if stop_btn:
            animation_placeholder.empty() # Remove the timer
            st.rerun() # Reload the app instantly

        # START BUTTON LOGIC
        if start_btn:
            with animation_placeholder.container():
                
                # PHASE 1: INHALE (4 Seconds)
                st.info("🌬️ INHALE... (Through Nose)")
                timer = st.empty()
                for i in range(4, 0, -1):
                    timer.metric("Seconds", i)
                    time.sleep(1)
                timer.empty()
                
                # PHASE 2: HOLD (7 Seconds)
                st.warning("HOLD... (Keep it in)")
                timer = st.empty()
                for i in range(7, 0, -1):
                    timer.metric("Seconds", i)
                    time.sleep(1)
                timer.empty()
                
                # PHASE 3: EXHALE (8 Seconds)
                st.success("💨 EXHALE... (Through Mouth)")
                timer = st.empty()
                for i in range(8, 0, -1):
                    timer.metric("Seconds", i)
                    time.sleep(1)
                timer.empty()
                
                st.balloons()
                st.success("Cycle Complete.")

# ==========================================
# PAGE 2: ADMIN DATA
# ==========================================
elif page == "Admin Data":
    st.title("🔐 Admin Research Portal")
    password = st.sidebar.text_input("Enter Admin Password:", type="password")
    
    if password == "admin123":
        st.success("Access Granted: Research Data View")
        
        if os.path.exists("user_usage_logs.csv"):
            st.subheader("📋 Participant Usage Logs")
            
            try:
                # Read file as a Table
                df_logs = pd.read_csv("user_usage_logs.csv", names=["User Name", "Mood", "Stress Level", "Song Prescribed"])
                
                # Show Metrics
                col1, col2 = st.columns(2)
                col1.metric("Total Sessions", len(df_logs))
                col2.metric("Avg Stress Level", round(df_logs["Stress Level"].mean(), 1))
                
                # Show Table
                st.dataframe(df_logs, use_container_width=True)
                
            except Exception as e:
                st.error("Log file exists but is empty or unreadable.")
            
            # Clear History Button
            st.write("---")
            if st.button("⚠️ Clear All Research Data"):
                os.remove("user_usage_logs.csv")
                st.success("History deleted successfully.")
                st.rerun()
        else:
            st.info("No data recorded yet. Go to 'Therapy Session' and use the app first.")
            
    elif password != "":
        st.error("Incorrect Password.")