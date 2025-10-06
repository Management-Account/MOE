import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("2089 MOE Registration")

# Important Note and Caution
st.warning("""
**State buffs plan**  
6-Oct Monday : Construction                 
7-Oct Tuesday : Research  
9-Oct Thursday: Training  
  
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
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("MOE BUFF")

# Time slot options
time_slots = [
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
]

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    game_id = st.text_input("Enter Your Game ID*", key="game_id")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["TCW", "EFE", "MRA", "FOX" ,"SHR", "MMD" ],
        index=0
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?*",
        ["F28","F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5" ,FC6,FC7,FC8],
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
    
    training_speedups = st.number_input(
        "How many Training Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    
    # Preferred timing for ministry buff
    buff_timing = st.selectbox(
        "What is your Preferred time zone For ministry Buff?*",
        time_slots,
        index=0
    )

    # Preferred alternative timings (multiple selection)
    alt_buff_timings = st.multiselect(
        "What are your Alternative preferred timings? (Select all that apply)",
        time_slots,
        default=[time_slots[1]]  # Default to second option
    )

    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        if not player_name or not game_id:
            st.error("Please enter your in-game name and Game ID")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Join multiple alt timings with comma separator
            alt_timings_str = ", ".join(alt_buff_timings) if alt_buff_timings else "None"
            
            new_row = [
                timestamp,
                player_name,
                game_id,
                alliance,
                fc_level,
                general_speedups,
                training_speedups,
                buff_timing,
                alt_timings_str  # This now contains all selected alt timings
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")


