import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# Get Snowflake session
session = get_active_session()

# List of playoff teams with their seed values
AFC_TEAMS = {
    1: "Kansas City Chiefs (1)",
    2: "Buffalo Bills (2)",
    3: "Baltimore Ravens (3)",
    4: "Houston Texans (4)",
    5: "LA Chargers (5)",
    6: "Pittsburgh Steelers (6)",
    7: "Denver Broncos (7)"
}

NFC_TEAMS = {
    1: "Detroit Lions (1)",
    2: "Philadelphia Eagles (2)",
    3: "Tampa Bay Buccaneers (3)",
    4: "LA Rams (4)",
    5: "Minnesota Vikings (5)",
    6: "Washington Commanders (6)",
    7: "Green Bay Packers (7)"
}

st.title("🏈 NFL Playoff Bracket Entry")


# Top section: Name, Email, Edit Key
st.text_input("Name ", key="name", placeholder="Enter your full name and any additional info to make it a unique entry name")
st.text_input("Email ", key="email", placeholder="flast@phdata.io")
st.text_input("Edit Key ", key="edit_key", type="password", 
                help="Create a secret key to edit your entry later. This along with your email uniquely identifies your entry, so make it different per entry.")

# two buttons: Retrieve Bracket and Clear Bracket
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("Retrieve Bracket", type="primary"):
        if not st.session_state.name:
            st.error("Please enter your name")
        elif not st.session_state.email:
            st.error("Please enter your email")
        elif not st.session_state.edit_key:
            st.error("Please enter your edit key")
        else:
            try:
                query = """
                    SELECT * FROM NFL_PLAYOFF_CONTEST.PROD.NFL_BRACKET_ENTRIES
                    WHERE PARTICIPANT_NAME = ? 
                    AND PARTICIPANT_EMAIL = ?
                    AND EDIT_KEY = ?
                """
                result = session.sql(query, params=[
                    st.session_state.name,
                    st.session_state.email,
                    st.session_state.edit_key
                ]).collect()
                
                if len(result) == 0:
                    st.error("No bracket found with the provided credentials")
                elif len(result) > 1:
                    st.error("Multiple brackets found. Please contact Nathan Mott to resolve this issue.")
                else:
                    row = result[0]
                    
                    # Populate tiebreaker
                    st.session_state.tiebreaker = int(row['TIE_BREAKER_POINTS']) if row['TIE_BREAKER_POINTS'] else 45
                    
                    # Helper function to set checkbox state based on winner
                    def set_checkbox_states(team1, team2, winner, key1, key2):
                        st.session_state[key1] = (winner == team1)
                        st.session_state[key2] = (winner == team2)
                    
                    # Wild Card winners
                    set_checkbox_states(row['WILDCARD1_TEAM_1'], row['WILDCARD1_TEAM_2'], row['WILDCARD1_WINNER'], 'afc_wc1_w1', 'afc_wc1_w2')
                    set_checkbox_states(row['WILDCARD2_TEAM_1'], row['WILDCARD2_TEAM_2'], row['WILDCARD2_WINNER'], 'afc_wc2_w1', 'afc_wc2_w2')
                    set_checkbox_states(row['WILDCARD3_TEAM_1'], row['WILDCARD3_TEAM_2'], row['WILDCARD3_WINNER'], 'afc_wc3_w1', 'afc_wc3_w2')
                    set_checkbox_states(row['WILDCARD4_TEAM_1'], row['WILDCARD4_TEAM_2'], row['WILDCARD4_WINNER'], 'nfc_wc1_w1', 'nfc_wc1_w2')
                    set_checkbox_states(row['WILDCARD5_TEAM_1'], row['WILDCARD5_TEAM_2'], row['WILDCARD5_WINNER'], 'nfc_wc2_w1', 'nfc_wc2_w2')
                    set_checkbox_states(row['WILDCARD6_TEAM_1'], row['WILDCARD6_TEAM_2'], row['WILDCARD6_WINNER'], 'nfc_wc3_w1', 'nfc_wc3_w2')
                    
                    # Divisional teams and winners
                    st.session_state.afc_div1_t1 = row['DIVISIONAL1_TEAM_1'] or ""
                    st.session_state.afc_div1_t2 = row['DIVISIONAL1_TEAM_2'] or ""
                    set_checkbox_states(row['DIVISIONAL1_TEAM_1'], row['DIVISIONAL1_TEAM_2'], row['DIVISIONAL1_WINNER'], 'afc_div1_w1', 'afc_div1_w2')
                    
                    st.session_state.afc_div2_t1 = row['DIVISIONAL2_TEAM_1'] or ""
                    st.session_state.afc_div2_t2 = row['DIVISIONAL2_TEAM_2'] or ""
                    set_checkbox_states(row['DIVISIONAL2_TEAM_1'], row['DIVISIONAL2_TEAM_2'], row['DIVISIONAL2_WINNER'], 'afc_div2_w1', 'afc_div2_w2')
                    
                    st.session_state.nfc_div1_t1 = row['DIVISIONAL3_TEAM_1'] or ""
                    st.session_state.nfc_div1_t2 = row['DIVISIONAL3_TEAM_2'] or ""
                    set_checkbox_states(row['DIVISIONAL3_TEAM_1'], row['DIVISIONAL3_TEAM_2'], row['DIVISIONAL3_WINNER'], 'nfc_div1_w1', 'nfc_div1_w2')
                    
                    st.session_state.nfc_div2_t1 = row['DIVISIONAL4_TEAM_1'] or ""
                    st.session_state.nfc_div2_t2 = row['DIVISIONAL4_TEAM_2'] or ""
                    set_checkbox_states(row['DIVISIONAL4_TEAM_1'], row['DIVISIONAL4_TEAM_2'], row['DIVISIONAL4_WINNER'], 'nfc_div2_w1', 'nfc_div2_w2')
                    
                    # Conference teams and winners
                    st.session_state.afc_conf_t1 = row['CONFERENCE1_TEAM_1'] or ""
                    st.session_state.afc_conf_t2 = row['CONFERENCE1_TEAM_2'] or ""
                    set_checkbox_states(row['CONFERENCE1_TEAM_1'], row['CONFERENCE1_TEAM_2'], row['CONFERENCE1_WINNER'], 'afc_conf_w1', 'afc_conf_w2')
                    
                    st.session_state.nfc_conf_t1 = row['CONFERENCE2_TEAM_1'] or ""
                    st.session_state.nfc_conf_t2 = row['CONFERENCE2_TEAM_2'] or ""
                    set_checkbox_states(row['CONFERENCE2_TEAM_1'], row['CONFERENCE2_TEAM_2'], row['CONFERENCE2_WINNER'], 'nfc_conf_w1', 'nfc_conf_w2')
                    
                    # Super Bowl teams and winner
                    st.session_state.sb_team1 = row['SUPERBOWL_TEAM_1'] or ""
                    st.session_state.sb_team2 = row['SUPERBOWL_TEAM_2'] or ""
                    set_checkbox_states(row['SUPERBOWL_TEAM_1'], row['SUPERBOWL_TEAM_2'], row['SUPERBOWL_WINNER'], 'sb_win1', 'sb_win2')
                    
                    st.success("✅ Bracket loaded successfully!")
                    
            except Exception as e:
                st.error(f"Error retrieving bracket: {e}")

with btn_col2:
    if st.button("Clear Bracket", type="primary", key="clear_bracket"):
        # Clear all Wild Card checkboxes
        st.session_state.afc_wc1_w1 = False
        st.session_state.afc_wc1_w2 = False
        st.session_state.afc_wc2_w1 = False
        st.session_state.afc_wc2_w2 = False
        st.session_state.afc_wc3_w1 = False
        st.session_state.afc_wc3_w2 = False
        st.session_state.nfc_wc1_w1 = False
        st.session_state.nfc_wc1_w2 = False
        st.session_state.nfc_wc2_w1 = False
        st.session_state.nfc_wc2_w2 = False
        st.session_state.nfc_wc3_w1 = False
        st.session_state.nfc_wc3_w2 = False
        
        # Clear all Divisional teams and checkboxes
        st.session_state.afc_div1_t1 = ""
        st.session_state.afc_div1_t2 = AFC_TEAMS.get(1)
        st.session_state.afc_div1_w1 = False
        st.session_state.afc_div1_w2 = False
        st.session_state.afc_div2_t1 = ""
        st.session_state.afc_div2_t2 = ""
        st.session_state.afc_div2_w1 = False
        st.session_state.afc_div2_w2 = False
        st.session_state.nfc_div1_t1 = ""
        st.session_state.nfc_div1_t2 = NFC_TEAMS.get(1)
        st.session_state.nfc_div1_w1 = False
        st.session_state.nfc_div1_w2 = False
        st.session_state.nfc_div2_t1 = ""
        st.session_state.nfc_div2_t2 = ""
        st.session_state.nfc_div2_w1 = False
        st.session_state.nfc_div2_w2 = False
        
        # Clear all Conference teams and checkboxes
        st.session_state.afc_conf_t1 = ""
        st.session_state.afc_conf_t2 = ""
        st.session_state.afc_conf_w1 = False
        st.session_state.afc_conf_w2 = False
        st.session_state.nfc_conf_t1 = ""
        st.session_state.nfc_conf_t2 = ""
        st.session_state.nfc_conf_w1 = False
        st.session_state.nfc_conf_w2 = False
        
        # Clear Super Bowl teams and checkboxes
        st.session_state.sb_team1 = ""
        st.session_state.sb_team2 = ""
        st.session_state.sb_win1 = False
        st.session_state.sb_win2 = False
        
        # Reset tiebreaker to default
        st.session_state.tiebreaker = 45
        
        st.success("🗑️ Bracket cleared!")


st.markdown("---")

# Wild Card Round
wc_col1, wc_col2 = st.columns(2)

with wc_col1:
    st.subheader("AFC Wild Card")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(AFC_TEAMS.get(7), key="afc_wc1_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(AFC_TEAMS.get(2), key="afc_wc1_w2")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(AFC_TEAMS.get(6), key="afc_wc2_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(AFC_TEAMS.get(3), key="afc_wc2_w2")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(AFC_TEAMS.get(5), key="afc_wc3_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(AFC_TEAMS.get(4), key="afc_wc3_w2")

with wc_col2:
    st.subheader("NFC Wild Card")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(NFC_TEAMS.get(7), key="nfc_wc1_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(NFC_TEAMS.get(2), key="nfc_wc1_w2")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(NFC_TEAMS.get(6), key="nfc_wc2_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(NFC_TEAMS.get(3), key="nfc_wc2_w2")
    
    with st.container(border=True):
        cb_col1, vs_col, cb_col2 = st.columns([5, 1, 5])
        with cb_col1:
            st.checkbox(NFC_TEAMS.get(5), key="nfc_wc3_w1")
        with vs_col:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>vs</div>", unsafe_allow_html=True)
        with cb_col2:
            st.checkbox(NFC_TEAMS.get(4), key="nfc_wc3_w2")

st.markdown("---")

# Divisional Round
div_col1, div_col2 = st.columns(2)

with div_col1:
    st.subheader("AFC Divisional Round")
    st.selectbox("", [""] + [AFC_TEAMS[seed] for seed in [4, 5, 6, 7]], key="afc_div1_t1")
    st.selectbox("vs", [AFC_TEAMS.get(1)], key="afc_div1_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("afc_div1_t1", "(select team above)") or "(select team above)", key="afc_div1_w1")
    st.checkbox(st.session_state.get("afc_div1_t2", "(select team above)") or "(select team above)", key="afc_div1_w2")
    
    st.selectbox("", [""] + list(AFC_TEAMS.values()), key="afc_div2_t1")
    st.selectbox("vs", [""] + list(AFC_TEAMS.values()), key="afc_div2_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("afc_div2_t1", "(select team above)") or "(select team above)", key="afc_div2_w1")
    st.checkbox(st.session_state.get("afc_div2_t2", "(select team above)") or "(select team above)", key="afc_div2_w2")

with div_col2:
    st.subheader("NFC Divisional Round")
    st.selectbox("", [""] + [NFC_TEAMS[seed] for seed in [4, 5, 6, 7]], key="nfc_div1_t1")
    st.selectbox("vs", [NFC_TEAMS.get(1)], key="nfc_div1_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("nfc_div1_t1", "(select team above)") or "(select team above)", key="nfc_div1_w1")
    st.checkbox(st.session_state.get("nfc_div1_t2", "(select team above)") or "(select team above)", key="nfc_div1_w2")
    
    st.selectbox("", [""] + list(NFC_TEAMS.values()), key="nfc_div2_t1")
    st.selectbox("vs", [""] + list(NFC_TEAMS.values()), key="nfc_div2_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("nfc_div2_t1", "(select team above)") or "(select team above)", key="nfc_div2_w1")
    st.checkbox(st.session_state.get("nfc_div2_t2", "(select team above)") or "(select team above)", key="nfc_div2_w2")

st.markdown("---")

# Conference Games
conf_col1, conf_col2 = st.columns(2)

with conf_col1:
    st.subheader("AFC Conference Game")
    st.selectbox("", [""] + list(AFC_TEAMS.values()), key="afc_conf_t1")
    st.selectbox("vs", [""] + list(AFC_TEAMS.values()), key="afc_conf_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("afc_conf_t1", "(select team above)") or "(select team above)", key="afc_conf_w1")
    st.checkbox(st.session_state.get("afc_conf_t2", "(select team above)") or "(select team above)", key="afc_conf_w2")

with conf_col2:
    st.subheader("NFC Conference Game")
    st.selectbox("", [""] + list(NFC_TEAMS.values()), key="nfc_conf_t1")
    st.selectbox("vs", [""] + list(NFC_TEAMS.values()), key="nfc_conf_t2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("nfc_conf_t1", "(select team above)") or "(select team above)", key="nfc_conf_w1")
    st.checkbox(st.session_state.get("nfc_conf_t2", "(select team above)") or "(select team above)", key="nfc_conf_w2")

st.markdown("---")

# Super Bowl Section
st.subheader("🏆 Super Bowl")
sb_col1, sb_col2 = st.columns([4, 1])
with sb_col1:
    st.selectbox("", [""] + list(AFC_TEAMS.values()), key="sb_team1")
    st.selectbox("vs", [""] + list(NFC_TEAMS.values()), key="sb_team2")
    st.markdown("<p style='text-align: center;'>Select a winner</p>", unsafe_allow_html=True)
    st.checkbox(st.session_state.get("sb_team1", "(select team above)") or "(select team above)", key="sb_win1")
    st.checkbox(st.session_state.get("sb_team2", "(select team above)") or "(select team above)", key="sb_win2")
with sb_col2:
    st.number_input("Tiebreaker (total points)", min_value=0, max_value=200, key="tiebreaker", help="Total points scored in the Super Bowl compared by absolute difference")

st.markdown("---")

# Submit button
if st.button("Submit Bracket", type="primary"):
    # st.write("🔍 DEBUG: Submit button clicked")
    
    # Validation
    if not st.session_state.name:
        st.error("Please enter your name")
        st.stop()
    elif not st.session_state.email:
        st.error("Please enter your email")
        st.stop()
    elif not st.session_state.edit_key:
        st.error("Please create an edit key")
        st.stop()
    elif "@" not in st.session_state.email:
        st.error("Please enter a valid email address")
        st.stop()
    
    # st.write("🔍 DEBUG: Basic validation passed")
    
    # Determine winners
    def get_winner(team1, team2, win1, win2):
        if win1 and not win2:
            return team1
        elif win2 and not win1:
            return team2
        return ""
    
    # Validate all winners are selected
    validation_errors = []
    
    # Wild Card validation - winners only (teams are predetermined)
    if not get_winner(AFC_TEAMS.get(7), AFC_TEAMS.get(2), st.session_state.afc_wc1_w1, st.session_state.afc_wc1_w2):
        validation_errors.append("AFC Wild Card Game 1: Select exactly one winner")
    if not get_winner(AFC_TEAMS.get(6), AFC_TEAMS.get(3), st.session_state.afc_wc2_w1, st.session_state.afc_wc2_w2):
        validation_errors.append("AFC Wild Card Game 2: Select exactly one winner")
    if not get_winner(AFC_TEAMS.get(5), AFC_TEAMS.get(4), st.session_state.afc_wc3_w1, st.session_state.afc_wc3_w2):
        validation_errors.append("AFC Wild Card Game 3: Select exactly one winner")
    if not get_winner(NFC_TEAMS.get(7), NFC_TEAMS.get(2), st.session_state.nfc_wc1_w1, st.session_state.nfc_wc1_w2):
        validation_errors.append("NFC Wild Card Game 1: Select exactly one winner")
    if not get_winner(NFC_TEAMS.get(6), NFC_TEAMS.get(3), st.session_state.nfc_wc2_w1, st.session_state.nfc_wc2_w2):
        validation_errors.append("NFC Wild Card Game 2: Select exactly one winner")
    if not get_winner(NFC_TEAMS.get(5), NFC_TEAMS.get(4), st.session_state.nfc_wc3_w1, st.session_state.nfc_wc3_w2):
        validation_errors.append("NFC Wild Card Game 3: Select exactly one winner")
    
    # Divisional Round validation - both teams and winners
    if not st.session_state.afc_div1_t1 or st.session_state.afc_div1_t1 == "":
        validation_errors.append("AFC Divisional Game 1: Select team 1")
    if not st.session_state.afc_div1_t2 or st.session_state.afc_div1_t2 == "":
        validation_errors.append("AFC Divisional Game 1: Select team 2")
    if st.session_state.afc_div1_t1 == st.session_state.afc_div1_t2:
        validation_errors.append("AFC Divisional Game 1: Teams cannot be the same")
    if not get_winner(st.session_state.afc_div1_t1, st.session_state.afc_div1_t2, st.session_state.afc_div1_w1, st.session_state.afc_div1_w2):
        validation_errors.append("AFC Divisional Game 1: Select exactly one winner")
    
    if not st.session_state.afc_div2_t1 or st.session_state.afc_div2_t1 == "":
        validation_errors.append("AFC Divisional Game 2: Select team 1")
    if not st.session_state.afc_div2_t2 or st.session_state.afc_div2_t2 == "":
        validation_errors.append("AFC Divisional Game 2: Select team 2")
    if st.session_state.afc_div2_t1 == st.session_state.afc_div2_t2:
        validation_errors.append("AFC Divisional Game 2: Teams cannot be the same")
    if not get_winner(st.session_state.afc_div2_t1, st.session_state.afc_div2_t2, st.session_state.afc_div2_w1, st.session_state.afc_div2_w2):
        validation_errors.append("AFC Divisional Game 2: Select exactly one winner")
    
    if not st.session_state.nfc_div1_t1 or st.session_state.nfc_div1_t1 == "":
        validation_errors.append("NFC Divisional Game 1: Select team 1")
    if not st.session_state.nfc_div1_t2 or st.session_state.nfc_div1_t2 == "":
        validation_errors.append("NFC Divisional Game 1: Select team 2")
    if st.session_state.nfc_div1_t1 == st.session_state.nfc_div1_t2:
        validation_errors.append("NFC Divisional Game 1: Teams cannot be the same")
    if not get_winner(st.session_state.nfc_div1_t1, st.session_state.nfc_div1_t2, st.session_state.nfc_div1_w1, st.session_state.nfc_div1_w2):
        validation_errors.append("NFC Divisional Game 1: Select exactly one winner")
    
    if not st.session_state.nfc_div2_t1 or st.session_state.nfc_div2_t1 == "":
        validation_errors.append("NFC Divisional Game 2: Select team 1")
    if not st.session_state.nfc_div2_t2 or st.session_state.nfc_div2_t2 == "":
        validation_errors.append("NFC Divisional Game 2: Select team 2")
    if st.session_state.nfc_div2_t1 == st.session_state.nfc_div2_t2:
        validation_errors.append("NFC Divisional Game 2: Teams cannot be the same")
    if not get_winner(st.session_state.nfc_div2_t1, st.session_state.nfc_div2_t2, st.session_state.nfc_div2_w1, st.session_state.nfc_div2_w2):
        validation_errors.append("NFC Divisional Game 2: Select exactly one winner")
    
    # Conference Game validation - both teams and winners
    if not st.session_state.afc_conf_t1 or st.session_state.afc_conf_t1 == "":
        validation_errors.append("AFC Conference Game: Select team 1")
    if not st.session_state.afc_conf_t2 or st.session_state.afc_conf_t2 == "":
        validation_errors.append("AFC Conference Game: Select team 2")
    if st.session_state.afc_conf_t1 == st.session_state.afc_conf_t2:
        validation_errors.append("AFC Conference Game: Teams cannot be the same")
    if not get_winner(st.session_state.afc_conf_t1, st.session_state.afc_conf_t2, st.session_state.afc_conf_w1, st.session_state.afc_conf_w2):
        validation_errors.append("AFC Conference Game: Select exactly one winner")
    
    if not st.session_state.nfc_conf_t1 or st.session_state.nfc_conf_t1 == "":
        validation_errors.append("NFC Conference Game: Select team 1")
    if not st.session_state.nfc_conf_t2 or st.session_state.nfc_conf_t2 == "":
        validation_errors.append("NFC Conference Game: Select team 2")
    if st.session_state.nfc_conf_t1 == st.session_state.nfc_conf_t2:
        validation_errors.append("NFC Conference Game: Teams cannot be the same")
    if not get_winner(st.session_state.nfc_conf_t1, st.session_state.nfc_conf_t2, st.session_state.nfc_conf_w1, st.session_state.nfc_conf_w2):
        validation_errors.append("NFC Conference Game: Select exactly one winner")
    
    # Super Bowl validation - both teams and winner
    if not st.session_state.sb_team1 or st.session_state.sb_team1 == "":
        validation_errors.append("Super Bowl: Select AFC team")
    if not st.session_state.sb_team2 or st.session_state.sb_team2 == "":
        validation_errors.append("Super Bowl: Select NFC team")
    if st.session_state.sb_team1 == st.session_state.sb_team2:
        validation_errors.append("Super Bowl: Teams cannot be the same")
    if not get_winner(st.session_state.sb_team1, st.session_state.sb_team2, st.session_state.sb_win1, st.session_state.sb_win2):
        validation_errors.append("Super Bowl: Select exactly one winner")
    
    if validation_errors:
        st.error("Please fix the following errors:")
        for error in validation_errors:
            st.write(f"❌ {error}")
        st.stop()
    
    # st.write("🔍 DEBUG: Winner validation passed")
    
    # Create the table if it doesn't exist with proper privileges
    def create_table():
        try:
            # st.write("🔍 DEBUG: Creating table if not exists")
            
            # Get current role for debugging
            current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
            # st.write(f"🔍 DEBUG: Current role: {current_role}")
            
            # Create table with explicit ownership
            session.sql("""
                CREATE TABLE IF NOT EXISTS NFL_PLAYOFF_CONTEST.PROD.NFL_BRACKET_ENTRIES (
                    participant_name VARCHAR,
                    participant_email VARCHAR,
                    edit_key VARCHAR,
                    tie_breaker_points NUMBER,
                    wildcard1_team_1 VARCHAR,
                    wildcard1_team_2 VARCHAR,
                    wildcard1_winner VARCHAR,
                    wildcard2_team_1 VARCHAR,
                    wildcard2_team_2 VARCHAR,
                    wildcard2_winner VARCHAR,
                    wildcard3_team_1 VARCHAR,
                    wildcard3_team_2 VARCHAR,
                    wildcard3_winner VARCHAR,
                    wildcard4_team_1 VARCHAR,
                    wildcard4_team_2 VARCHAR,
                    wildcard4_winner VARCHAR,
                    wildcard5_team_1 VARCHAR,
                    wildcard5_team_2 VARCHAR,
                    wildcard5_winner VARCHAR,
                    wildcard6_team_1 VARCHAR,
                    wildcard6_team_2 VARCHAR,
                    wildcard6_winner VARCHAR,
                    divisional1_team_1 VARCHAR,
                    divisional1_team_2 VARCHAR,
                    divisional1_winner VARCHAR,
                    divisional2_team_1 VARCHAR,
                    divisional2_team_2 VARCHAR,
                    divisional2_winner VARCHAR,
                    divisional3_team_1 VARCHAR,
                    divisional3_team_2 VARCHAR,
                    divisional3_winner VARCHAR,
                    divisional4_team_1 VARCHAR,
                    divisional4_team_2 VARCHAR,
                    divisional4_winner VARCHAR,
                    conference1_team_1 VARCHAR,
                    conference1_team_2 VARCHAR,
                    conference1_winner VARCHAR,
                    conference2_team_1 VARCHAR,
                    conference2_team_2 VARCHAR,
                    conference2_winner VARCHAR,
                    superbowl_team_1 VARCHAR,
                    superbowl_team_2 VARCHAR,
                    superbowl_winner VARCHAR,
                    submitted_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """).collect()
            
            # Grant privileges to current role
            try:
                session.sql(f"""
                    GRANT INSERT, SELECT ON TABLE NFL_PLAYOFF_CONTEST.PROD.NFL_BRACKET_ENTRIES 
                    TO ROLE {current_role}
                """).collect()
                # st.write("🔍 DEBUG: Granted privileges to current role")
            except Exception as grant_error:
                # st.write(f"🔍 DEBUG: Grant failed (may already have privileges): {grant_error}")
                pass
            
            # st.write("🔍 DEBUG: Table creation completed")
        except Exception as e:
            st.error(f"Error creating table: {e}")
            raise

    create_table()

    # Build data dictionary
    # st.write("🔍 DEBUG: Building data dictionary")
    data = {
        'PARTICIPANT_NAME': st.session_state.name,
        'PARTICIPANT_EMAIL': st.session_state.email,
        'EDIT_KEY': st.session_state.edit_key,
        'TIE_BREAKER_POINTS': st.session_state.tiebreaker,
        # Wild Card
        'WILDCARD1_TEAM_1': AFC_TEAMS.get(7),
        'WILDCARD1_TEAM_2': AFC_TEAMS.get(2),
        'WILDCARD1_WINNER': get_winner(AFC_TEAMS.get(7), AFC_TEAMS.get(2), 
                                       st.session_state.afc_wc1_w1, st.session_state.afc_wc1_w2),
        'WILDCARD2_TEAM_1': AFC_TEAMS.get(6),
        'WILDCARD2_TEAM_2': AFC_TEAMS.get(3),
        'WILDCARD2_WINNER': get_winner(AFC_TEAMS.get(6), AFC_TEAMS.get(3), 
                                       st.session_state.afc_wc2_w1, st.session_state.afc_wc2_w2),
        'WILDCARD3_TEAM_1': AFC_TEAMS.get(5),
        'WILDCARD3_TEAM_2': AFC_TEAMS.get(4),
        'WILDCARD3_WINNER': get_winner(AFC_TEAMS.get(5), AFC_TEAMS.get(4), 
                                       st.session_state.afc_wc3_w1, st.session_state.afc_wc3_w2),
        'WILDCARD4_TEAM_1': NFC_TEAMS.get(7),
        'WILDCARD4_TEAM_2': NFC_TEAMS.get(2),
        'WILDCARD4_WINNER': get_winner(NFC_TEAMS.get(7), NFC_TEAMS.get(2), 
                                       st.session_state.nfc_wc1_w1, st.session_state.nfc_wc1_w2),
        'WILDCARD5_TEAM_1': NFC_TEAMS.get(6),
        'WILDCARD5_TEAM_2': NFC_TEAMS.get(3),
        'WILDCARD5_WINNER': get_winner(NFC_TEAMS.get(6), NFC_TEAMS.get(3), 
                                       st.session_state.nfc_wc2_w1, st.session_state.nfc_wc2_w2),
        'WILDCARD6_TEAM_1': NFC_TEAMS.get(5),
        'WILDCARD6_TEAM_2': NFC_TEAMS.get(4),
        'WILDCARD6_WINNER': get_winner(NFC_TEAMS.get(5), NFC_TEAMS.get(4), 
                                       st.session_state.nfc_wc3_w1, st.session_state.nfc_wc3_w2),
        # Divisional
        'DIVISIONAL1_TEAM_1': st.session_state.afc_div1_t1,
        'DIVISIONAL1_TEAM_2': AFC_TEAMS.get(1),
        'DIVISIONAL1_WINNER': get_winner(st.session_state.afc_div1_t1, st.session_state.afc_div1_t2, 
                                        st.session_state.afc_div1_w1, st.session_state.afc_div1_w2),
        'DIVISIONAL2_TEAM_1': st.session_state.afc_div2_t1,
        'DIVISIONAL2_TEAM_2': st.session_state.afc_div2_t2,
        'DIVISIONAL2_WINNER': get_winner(st.session_state.afc_div2_t1, st.session_state.afc_div2_t2, 
                                        st.session_state.afc_div2_w1, st.session_state.afc_div2_w2),
        'DIVISIONAL3_TEAM_1': st.session_state.nfc_div1_t1,
        'DIVISIONAL3_TEAM_2': NFC_TEAMS.get(1),
        'DIVISIONAL3_WINNER': get_winner(st.session_state.nfc_div1_t1, st.session_state.nfc_div1_t2, 
                                        st.session_state.nfc_div1_w1, st.session_state.nfc_div1_w2),
        'DIVISIONAL4_TEAM_1': st.session_state.nfc_div2_t1,
        'DIVISIONAL4_TEAM_2': st.session_state.nfc_div2_t2,
        'DIVISIONAL4_WINNER': get_winner(st.session_state.nfc_div2_t1, st.session_state.nfc_div2_t2, 
                                        st.session_state.nfc_div2_w1, st.session_state.nfc_div2_w2),
        # Conference
        'CONFERENCE1_TEAM_1': st.session_state.afc_conf_t1,
        'CONFERENCE1_TEAM_2': st.session_state.afc_conf_t2,
        'CONFERENCE1_WINNER': get_winner(st.session_state.afc_conf_t1, st.session_state.afc_conf_t2, 
                                        st.session_state.afc_conf_w1, st.session_state.afc_conf_w2),
        'CONFERENCE2_TEAM_1': st.session_state.nfc_conf_t1,
        'CONFERENCE2_TEAM_2': st.session_state.nfc_conf_t2,
        'CONFERENCE2_WINNER': get_winner(st.session_state.nfc_conf_t1, st.session_state.nfc_conf_t2, 
                                        st.session_state.nfc_conf_w1, st.session_state.nfc_conf_w2),
        # Super Bowl
        'SUPERBOWL_TEAM_1': st.session_state.sb_team1,
        'SUPERBOWL_TEAM_2': st.session_state.sb_team2,
        'SUPERBOWL_WINNER': get_winner(st.session_state.sb_team1, st.session_state.sb_team2, 
                                      st.session_state.sb_win1, st.session_state.sb_win2)
    }
    
    # st.write("🔍 DEBUG: Data dictionary created")
    # st.write(f"🔍 DEBUG: Sample data - Name: {data['PARTICIPANT_NAME']}, Email: {data['PARTICIPANT_EMAIL']}")
    
    # Insert into Snowflake using direct SQL instead of write_pandas
    try:
        # st.write("🔍 DEBUG: Preparing SQL MERGE")
        
        # Build column assignments for UPDATE
        update_columns = [k for k in data.keys() if k not in ['PARTICIPANT_EMAIL', 'EDIT_KEY']]
        update_set = ', '.join([f"{col} = source.{col}" for col in update_columns])
        
        # Build column list and values for INSERT
        columns = ', '.join(data.keys())
        source_columns = ', '.join([f"? AS {col}" for col in data.keys()])
        values = list(data.values())
        
        merge_sql = f"""
            MERGE INTO NFL_PLAYOFF_CONTEST.PROD.NFL_BRACKET_ENTRIES AS target
            USING (SELECT {source_columns}) AS source
            ON target.PARTICIPANT_EMAIL = source.PARTICIPANT_EMAIL 
               AND target.EDIT_KEY = source.EDIT_KEY
            WHEN MATCHED THEN
                UPDATE SET 
                    {update_set},
                    SUBMITTED_AT = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN
                INSERT ({columns})
                VALUES ({', '.join([f'source.{col}' for col in data.keys()])})
        """
        
        # st.write("🔍 DEBUG: Executing MERGE")
        # st.code(merge_sql[:200] + "...")
        
        session.sql(merge_sql, params=values).collect()
        
        # st.write("🔍 DEBUG: Merge completed")
        st.success(f"✅ Bracket submitted successfully for {st.session_state.name}!")
        st.info("🔑 Save your Edit Key to modify this entry later.")
        st.balloons()
    except Exception as e:
        st.error(f"Error submitting bracket: {e}")
        # st.write(f"🔍 DEBUG: Exception type: {type(e)}")
        # st.write(f"🔍 DEBUG: Exception details: {str(e)}")
        # import traceback
        # st.code(traceback.format_exc())

