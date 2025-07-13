import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("VP Registration (Construction)")

# Important Note and Caution
st.warning("""
**State buffs plan**  
14-July Monday: Construction  
17-June Thursday: Training  
18-June Friday: Research  
""")

st.error("""
**CAUTION:**  
- Resource Preparation: Ensure you have sufficient resources to fully maximize your score  
- Fair Participation: Scores will be actively monitored. If you are assigned the buff, please contribute fairly to maintain equity for all participants. Your cooperation is greatly appreciated  
- **Registration Deadline: Registration closes at 12:00 UTC on 13th July**  
""")


# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS Prep Ministry Buffs")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    game_id = st.text_input("Enter Your Game ID*", key="game_id")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["TCW", "MRA", "FOX", "SHR" ,"mra", "CCB" , "RFA" , "GoR" , "DIU"],
        index=0
    )
    
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?*",
        ["F28","F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Speedups Information
    st.subheader("Inventory")
    general_speedups = st.number_input(
        "How many General Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    
    building_speedups = st.number_input(
        "How many Building Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    

    
    fc_count = st.number_input(
        "How many FCs do you have?*",
        min_value=0,
        step=1,
        value=0
    )
    
    # Preferred timing for ministry buff
    buff_timing = st.selectbox(
        "What is your Preferred time zone For ministry Buff?*",
        [
            "00:00 UTC to 02:00 UTC",
            "02:00 UTC to 04:00 UTC",
            "04:00 UTC to 06:00 UTC",
            "06:00 UTC to 08:00 UTC",
            "08:00 UTC to 10:00 UTC",
            "10:00 UTC to 12:00 UTC",
            "12:00 UTC to 14:00 UTC",
            "14:00 UTC to 16:00 UTC",
            "16:00 UTC to 18:00 UTC",
            "18:00 UTC to 20:00 UTC",
            "20:00 UTC to 22:00 UTC",
            "22:00 UTC to 23:59 UTC"
        ],
        index=0
    )
    
    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        if not player_name or not game_id:
            st.error("Please enter your in-game name and Game ID")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [
                timestamp,
                player_name,
                game_id,
                alliance,
                fc_level,
                general_speedups,
                building_speedups,
                fc_count,
                buff_timing
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")
