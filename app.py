import streamlit as st
import random
import string
from datetime import datetime
import statistics

# Page config
st.set_page_config(
    page_title="Nubs x Claude",
    page_icon="✦",
    layout="centered"
)

# Complete design system with proper Streamlit overrides
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Base styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* App background */
    .stApp {
        background-color: #F8F7F4;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 420px;
    }

    /* Tighten all element spacing */
    .element-container {
        margin-bottom: 0.4rem !important;
    }

    .stMarkdown {
        margin-bottom: 0 !important;
    }

    /* All text should be dark by default */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #4A4A4A !important;
    }

    /* Title */
    h1 {
        font-weight: 600 !important;
        font-size: 1.6rem !important;
        color: #3D3D3D !important;
        text-align: center;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }

    /* Buttons - centered container */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    /* All buttons - base style */
    .stButton > button {
        background-color: #8BA888 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        height: 40px !important;
        max-width: 280px !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #7A9A77 !important;
        border: none !important;
    }

    .stButton > button:active {
        background-color: #6B8B68 !important;
    }

    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: #ECEAE5 !important;
        color: #4A4A4A !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #E0DED9 !important;
    }

    /* Vote buttons in columns - fill their column */
    [data-testid="column"] .stButton > button {
        max-width: none !important;
        width: 100% !important;
        padding: 8px 6px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        height: 38px !important;
    }

    /* Text inputs - comprehensive fix */
    .stTextInput {
        max-width: 280px !important;
        margin: 0 auto !important;
    }

    /* Remove ALL borders from wrapper elements */
    .stTextInput > div,
    .stTextInput > div > div,
    .stTextInput [data-baseweb="input"],
    .stTextInput [data-baseweb="base-input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Style only the actual input */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #3D3D3D !important;
        border: 1.5px solid #D8D6D1 !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        height: 40px !important;
        box-sizing: border-box !important;
        width: 100% !important;
    }

    .stTextInput input::placeholder {
        color: #A8A8A8 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        border-color: #A8B8A6 !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Input labels - centered */
    .stTextInput > label {
        color: #7A7A7A !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-align: center !important;
        display: block !important;
        margin-bottom: 6px !important;
    }

    .stTextInput > label p {
        text-align: center !important;
    }

    /* Select boxes */
    .stSelectbox {
        max-width: 280px !important;
        margin: 0 auto !important;
    }

    .stSelectbox > div > div {
        background-color: white !important;
        border: 1.5px solid #D8D6D1 !important;
        border-radius: 10px !important;
    }

    .stSelectbox > div > div > div {
        color: #3D3D3D !important;
    }

    .stSelectbox > label {
        color: #7A7A7A !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-align: center !important;
        display: block !important;
    }

    /* Session code display */
    .session-code {
        background: linear-gradient(135deg, #C8BFD6 0%, #B5C9D3 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        letter-spacing: 3px;
        margin: 10px auto;
        max-width: 200px;
    }

    /* Participant badges */
    .participant-list {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        justify-content: center;
        margin: 8px 0;
    }

    .user-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 5px 10px;
        border-radius: 16px;
        font-weight: 500;
        font-size: 13px;
    }

    .user-badge.voted {
        background-color: #E5EDE4;
        color: #5C7A59;
    }

    .user-badge.waiting {
        background-color: #ECEAE5;
        color: #8C8C8C;
    }

    .user-badge.observer {
        background-color: #E5ECF0;
        color: #5C7A8A;
    }

    /* Stats cards */
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 12px 8px;
        text-align: center;
        border: 1px solid #ECEAE5;
    }

    .stat-value {
        font-size: 22px;
        font-weight: 600;
        color: #3D3D3D;
        margin-bottom: 2px;
    }

    .stat-label {
        font-size: 10px;
        color: #8C8C8C;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Consensus colors */
    .consensus-high { color: #6B8F68; }
    .consensus-medium { color: #C4A55A; }
    .consensus-low { color: #C4877A; }

    /* Vote results */
    .vote-result {
        display: inline-block;
        background: white;
        padding: 5px 10px;
        border-radius: 8px;
        margin: 2px;
        font-size: 13px;
        border: 1px solid #ECEAE5;
    }

    .vote-result-name {
        color: #8C8C8C;
    }

    .vote-result-value {
        color: #3D3D3D;
        font-weight: 600;
        margin-left: 4px;
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: #E8E6E1;
        margin: 14px 0;
    }

    /* Section headers */
    .section-header {
        font-size: 11px;
        font-weight: 600;
        color: #8C8C8C !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        text-align: center;
    }

    /* Tagline */
    .tagline {
        color: #9C9C9C !important;
        font-size: 14px;
        text-align: center;
        margin-bottom: 16px;
    }

    /* Centered text */
    .centered {
        text-align: center;
    }

    /* Helper text */
    .helper-text {
        color: #9C9C9C !important;
        font-size: 12px;
        text-align: center;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Fix column gaps */
    [data-testid="column"] {
        padding: 0 4px;
    }

    /* Reduce spacing around elements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'sessions' not in st.session_state:
    st.session_state.sessions = {}

if 'current_session' not in st.session_state:
    st.session_state.current_session = None

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

if 'is_observer' not in st.session_state:
    st.session_state.is_observer = None

if 'last_username' not in st.session_state:
    st.session_state.last_username = ""

# Voting options
VOTE_OPTIONS = ["0.5", "1", "2", "3", "5", "8", "13", "?"]

def generate_session_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_session():
    code = generate_session_code()
    st.session_state.sessions[code] = {
        'users': {},
        'votes': {},
        'created_at': datetime.now(),
        'votes_revealed': False
    }
    return code

def join_session(code, username, is_observer):
    if code in st.session_state.sessions:
        st.session_state.sessions[code]['users'][username] = {
            'is_observer': is_observer,
            'joined_at': datetime.now()
        }
        st.session_state.current_session = code
        st.session_state.user_name = username
        st.session_state.is_observer = is_observer
        st.session_state.last_username = username
        return True
    return False

def cast_vote(session_code, username, vote):
    if session_code in st.session_state.sessions:
        st.session_state.sessions[session_code]['votes'][username] = vote

def clear_votes(session_code):
    if session_code in st.session_state.sessions:
        st.session_state.sessions[session_code]['votes'] = {}
        st.session_state.sessions[session_code]['votes_revealed'] = False

def kick_user(session_code, username):
    if session_code in st.session_state.sessions:
        session = st.session_state.sessions[session_code]
        if username in session['users']:
            del session['users'][username]
        if username in session['votes']:
            del session['votes'][username]

def all_voters_voted(session_code):
    if session_code not in st.session_state.sessions:
        return False
    session = st.session_state.sessions[session_code]
    voters = [u for u, data in session['users'].items() if not data['is_observer']]
    if not voters:
        return False
    return all(voter in session['votes'] for voter in voters)

def calculate_stats(votes):
    if not votes:
        return None
    numeric_votes = [float(v) for v in votes.values() if v != "?"]
    if not numeric_votes:
        return {'most_common': "?", 'average': None, 'consensus': "—"}

    vote_counts = {}
    for vote in votes.values():
        vote_counts[vote] = vote_counts.get(vote, 0) + 1
    most_common = max(vote_counts.items(), key=lambda x: x[1])
    avg = statistics.mean(numeric_votes)

    if len(numeric_votes) > 1:
        stdev = statistics.stdev(numeric_votes)
        if stdev <= 1:
            consensus, consensus_class = "High", "consensus-high"
        elif stdev <= 2:
            consensus, consensus_class = "Medium", "consensus-medium"
        else:
            consensus, consensus_class = "Low", "consensus-low"
    else:
        consensus, consensus_class = "—", "consensus-medium"

    return {
        'most_common': most_common[0],
        'most_common_count': most_common[1],
        'average': round(avg, 1),
        'consensus': consensus,
        'consensus_class': consensus_class
    }

# ========== MAIN APP ==========

st.markdown("<h1>✦ Nubs x Claude</h1>", unsafe_allow_html=True)

if st.session_state.current_session is None:
    # HOME SCREEN
    st.markdown("<p class='tagline'>Estimate together, align faster</p>", unsafe_allow_html=True)

    if st.button("Create New Session", use_container_width=True):
        code = create_session()
        st.session_state.temp_session_code = code
        st.rerun()

    st.markdown("<p class='section-header'>Or join existing</p>", unsafe_allow_html=True)

    join_code = st.text_input("Session Code", max_chars=6, placeholder="ABC123").upper()

    if join_code or 'temp_session_code' in st.session_state:
        code_to_join = join_code if join_code else st.session_state.get('temp_session_code', '')

        if 'temp_session_code' in st.session_state and not join_code:
            st.markdown(f"<div class='session-code'>{code_to_join}</div>", unsafe_allow_html=True)
            st.markdown("<p class='helper-text'>Share this code with your team</p>", unsafe_allow_html=True)

        username = st.text_input("Your Name", value=st.session_state.last_username, placeholder="Enter your name", key="join_username")

        if st.button("Join as Voter", use_container_width=True, type="primary"):
            if username:
                if join_session(code_to_join, username, False):
                    if 'temp_session_code' in st.session_state:
                        del st.session_state.temp_session_code
                    st.rerun()
                else:
                    st.error("Session not found")
            else:
                st.warning("Please enter your name")

        if st.button("Join as Observer", use_container_width=True, type="secondary"):
            if username:
                if join_session(code_to_join, username, True):
                    if 'temp_session_code' in st.session_state:
                        del st.session_state.temp_session_code
                    st.rerun()
                else:
                    st.error("Session not found")
            else:
                st.warning("Please enter your name")

else:
    # SESSION SCREEN
    session = st.session_state.sessions[st.session_state.current_session]

    st.markdown(f"<div class='session-code'>{st.session_state.current_session}</div>", unsafe_allow_html=True)

    all_voted = all_voters_voted(st.session_state.current_session)
    votes_revealed = session['votes_revealed'] or all_voted

    # Voting buttons (voters only)
    if not st.session_state.is_observer:
        st.markdown("<p class='section-header'>Your Estimate</p>", unsafe_allow_html=True)
        current_vote = session['votes'].get(st.session_state.user_name)

        cols = st.columns(4)
        for idx, option in enumerate(VOTE_OPTIONS):
            with cols[idx % 4]:
                is_selected = current_vote == option
                btn_type = "primary" if is_selected else "secondary"
                if st.button(option, key=f"vote_{option}", use_container_width=True, type=btn_type):
                    cast_vote(st.session_state.current_session, st.session_state.user_name, option)
                    st.rerun()

    st.markdown("---")

    # Participants
    st.markdown("<p class='section-header'>Participants</p>", unsafe_allow_html=True)

    voters = {u: d for u, d in session['users'].items() if not d['is_observer']}
    observers = {u: d for u, d in session['users'].items() if d['is_observer']}

    if voters:
        badges = "<div class='participant-list'>"
        for user in voters:
            voted = user in session['votes']
            cls = "voted" if voted else "waiting"
            icon = "✓" if voted else "···"
            badges += f"<span class='user-badge {cls}'>{user} {icon}</span>"
        badges += "</div>"
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.markdown("<p class='helper-text'>No voters yet</p>", unsafe_allow_html=True)

    if observers:
        obs_badges = "<div class='participant-list'>"
        for user in observers:
            obs_badges += f"<span class='user-badge observer'>{user} 👁</span>"
        obs_badges += "</div>"
        st.markdown(obs_badges, unsafe_allow_html=True)

    # Auto-reveal
    if all_voted and not session['votes_revealed']:
        session['votes_revealed'] = True
        st.balloons()

    # Results
    if votes_revealed and session['votes']:
        st.markdown("---")
        st.markdown("<p class='section-header'>Results</p>", unsafe_allow_html=True)

        vote_html = "<div class='centered'>"
        for user, vote in session['votes'].items():
            vote_html += f"<span class='vote-result'><span class='vote-result-name'>{user}</span><span class='vote-result-value'>{vote}</span></span>"
        vote_html += "</div>"
        st.markdown(vote_html, unsafe_allow_html=True)

        stats = calculate_stats(session['votes'])
        if stats:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='stats-card'><div class='stat-value'>{stats['most_common']}</div><div class='stat-label'>Most Common</div></div>", unsafe_allow_html=True)
            with c2:
                avg = stats['average'] if stats['average'] else "—"
                st.markdown(f"<div class='stats-card'><div class='stat-value'>{avg}</div><div class='stat-label'>Average</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='stats-card'><div class='stat-value {stats['consensus_class']}'>{stats['consensus']}</div><div class='stat-label'>Consensus</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Observer controls
    if st.session_state.is_observer:
        st.markdown("<p class='section-header'>Controls</p>", unsafe_allow_html=True)
        if st.button("Clear Votes", use_container_width=True):
            clear_votes(st.session_state.current_session)
            st.rerun()

        users_to_kick = [u for u in session['users'] if u != st.session_state.user_name]
        if users_to_kick:
            user_to_kick = st.selectbox("Remove participant", users_to_kick)
            if st.button("Remove", use_container_width=True, type="secondary"):
                kick_user(st.session_state.current_session, user_to_kick)
                st.rerun()

    # Leave button
    if st.button("Leave Session", use_container_width=True, type="secondary"):
        st.session_state.current_session = None
        st.session_state.user_name = None
        st.session_state.is_observer = None
        st.rerun()
