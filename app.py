import streamlit as st
import random
import string
import statistics
from supabase import create_client

# Page config
st.set_page_config(
    page_title="Nubs x Claude",
    page_icon="✦",
    layout="centered"
)

# Initialize Supabase client
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

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
        padding: 0.25rem 1rem 1rem 1rem !important;
        margin-top: -1rem !important;
        max-width: 420px;
    }

    /* Kill the top margin on first element */
    .block-container > div:first-child,
    .stMarkdown:first-child,
    [data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Tighter consistent spacing */
    [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }

    /* Columns should have minimal gap */
    [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
        margin-bottom: 0 !important;
    }

    /* All text should be dark by default */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #4A4A4A !important;
    }

    /* Title */
    h1 {
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        color: #3D3D3D !important;
        text-align: center;
        letter-spacing: -0.02em;
        margin: 0 0 0.25rem 0 !important;
    }

    /* Buttons - centered container */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    /* All buttons - base style (primary) */
    .stButton > button {
        background-color: #4A6B4D !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        height: 42px !important;
        max-width: 280px !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #3D5A40 !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
        border: none !important;
    }

    .stButton > button:active {
        background-color: #324A34 !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    /* Secondary buttons - soft sage with charcoal text */
    .stButton > button[kind="secondary"] {
        background-color: #E9EEE9 !important;
        color: #444444 !important;
        -webkit-text-fill-color: #444444 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #DCE3DC !important;
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
    }

    /* Vote buttons in columns - fill their column */
    [data-testid="column"] .stButton > button {
        max-width: none !important;
        width: 100% !important;
        padding: 8px 6px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        height: 38px !important;
        -webkit-text-fill-color: inherit !important;
    }

    [data-testid="column"] .stButton > button[kind="secondary"] {
        -webkit-text-fill-color: #444444 !important;
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
        color: #2D2D2D !important;
        -webkit-text-fill-color: #2D2D2D !important;
    }

    /* Style only the actual input - all states */
    .stTextInput input,
    .stTextInput input:focus,
    .stTextInput input:active,
    .stTextInput input:hover {
        background-color: #FFFFFF !important;
        color: #2D2D2D !important;
        border: 1.5px solid #D8D6D1 !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        height: 42px !important;
        box-sizing: border-box !important;
        width: 100% !important;
        -webkit-text-fill-color: #2D2D2D !important;
        caret-color: #2D2D2D !important;
    }

    .stTextInput input::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        border-color: #4A6B4D !important;
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
        margin-bottom: 4px !important;
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
        background: #E8EDE8;
        color: #3D4A3D;
        padding: 10px 18px;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 600;
        text-align: center;
        letter-spacing: 3px;
        margin: 6px auto 14px auto;
        max-width: 140px;
    }

    /* Participant badges */
    .participant-list {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        justify-content: center;
        margin: 2px 0 0 0;
    }

    .user-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 5px 10px;
        border-radius: 14px;
        font-weight: 500;
        font-size: 13px;
    }

    .user-badge.voted {
        background-color: #E5EDE4;
        color: #3D5A3D;
    }

    .user-badge.waiting {
        background-color: #ECEAE5;
        color: #666666;
    }

    .user-badge.observer {
        background-color: #E5ECF0;
        color: #3D5A6A;
    }

    /* Stats cards */
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 10px 8px;
        text-align: center;
        border: 1px solid #ECEAE5;
        margin-top: 6px;
    }

    .stat-value {
        font-size: 20px;
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

    /* Consensus colors - accessible on white */
    .consensus-high { color: #3D6B3A; }
    .consensus-medium { color: #8B7332; }
    .consensus-low { color: #A65D50; }

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
        margin-left: 5px;
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: #E8E6E1;
        margin: 12px 0;
    }

    /* Section headers */
    .section-header {
        font-size: 11px;
        font-weight: 600;
        color: #8C8C8C !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 6px 0;
        text-align: center;
    }

    /* Tagline */
    .tagline {
        color: #9C9C9C !important;
        font-size: 13px;
        text-align: center;
        margin: 0 0 10px 0;
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
        margin: 2px 0;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Nuclear option for top padding */
    .stApp > header {
        height: 0 !important;
        min-height: 0 !important;
    }

    section[data-testid="stSidebar"] + div {
        padding-top: 0 !important;
    }

    .appview-container {
        padding-top: 0 !important;
    }

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

# ========== SUPABASE FUNCTIONS ==========

def generate_session_code():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

def create_session():
    """Create a new session in Supabase"""
    code = generate_session_code()
    # Make sure code is unique
    existing = supabase.table('sessions').select('code').eq('code', code).execute()
    while existing.data:
        code = generate_session_code()
        existing = supabase.table('sessions').select('code').eq('code', code).execute()

    supabase.table('sessions').insert({'code': code, 'votes_revealed': False}).execute()
    return code

def session_exists(code):
    """Check if a session exists"""
    result = supabase.table('sessions').select('code').eq('code', code).execute()
    return len(result.data) > 0

def join_session(code, username, is_observer):
    """Add user to a session"""
    if not session_exists(code):
        return False

    # Upsert user (in case they're rejoining)
    supabase.table('session_users').upsert({
        'session_code': code,
        'username': username,
        'is_observer': is_observer
    }, on_conflict='session_code,username').execute()

    st.session_state.current_session = code
    st.session_state.user_name = username
    st.session_state.is_observer = is_observer
    st.session_state.last_username = username

    # Set URL params for persistence across refresh
    st.query_params['session'] = code
    st.query_params['user'] = username
    if is_observer:
        st.query_params['observer'] = 'true'
    return True

def get_session_data(code):
    """Fetch all data for a session"""
    # Get users
    users_result = supabase.table('session_users').select('*').eq('session_code', code).execute()
    users = {u['username']: {'is_observer': u['is_observer']} for u in users_result.data}

    # Get votes
    votes_result = supabase.table('votes').select('*').eq('session_code', code).execute()
    votes = {v['username']: v['vote'] for v in votes_result.data}

    # Get session info
    session_result = supabase.table('sessions').select('*').eq('code', code).execute()
    votes_revealed = session_result.data[0]['votes_revealed'] if session_result.data else False

    return {
        'users': users,
        'votes': votes,
        'votes_revealed': votes_revealed
    }

def cast_vote(session_code, username, vote):
    """Record a vote"""
    supabase.table('votes').upsert({
        'session_code': session_code,
        'username': username,
        'vote': vote
    }, on_conflict='session_code,username').execute()

def clear_votes(session_code):
    """Clear all votes for a session"""
    supabase.table('votes').delete().eq('session_code', session_code).execute()
    supabase.table('sessions').update({'votes_revealed': False}).eq('code', session_code).execute()

def reveal_votes(session_code):
    """Set votes as revealed"""
    supabase.table('sessions').update({'votes_revealed': True}).eq('code', session_code).execute()

def kick_user(session_code, username):
    """Remove a user from the session"""
    supabase.table('session_users').delete().eq('session_code', session_code).eq('username', username).execute()
    supabase.table('votes').delete().eq('session_code', session_code).eq('username', username).execute()

def leave_session(session_code, username):
    """Current user leaves the session"""
    supabase.table('session_users').delete().eq('session_code', session_code).eq('username', username).execute()
    supabase.table('votes').delete().eq('session_code', session_code).eq('username', username).execute()

def all_voters_voted(session_data):
    """Check if all voters have voted"""
    voters = [u for u, data in session_data['users'].items() if not data['is_observer']]
    if not voters:
        return False
    return all(voter in session_data['votes'] for voter in voters)

def calculate_stats(votes):
    if not votes:
        return None
    numeric_votes = [float(v) for v in votes.values() if v != "?"]
    if not numeric_votes:
        return {'most_common': "?", 'average': None, 'consensus': "—", 'consensus_class': ""}

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

# Check URL params for session persistence (must be after function definitions)
query_params = st.query_params
if st.session_state.current_session is None and 'session' in query_params and 'user' in query_params:
    code = query_params['session']
    username = query_params['user']
    is_obs = query_params.get('observer', 'false') == 'true'
    if session_exists(code):
        join_session(code, username, is_obs)

# ========== MAIN APP ==========

st.markdown("<h1>✦ Nubs x Claude</h1>", unsafe_allow_html=True)

# Auto-refresh for real-time updates (every 2 seconds when in session)
if st.session_state.current_session:
    st.markdown("""
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 2000);
        </script>
    """, unsafe_allow_html=True)

if st.session_state.current_session is None:
    # HOME SCREEN
    st.markdown("<p class='tagline'>Estimate together, align faster</p>", unsafe_allow_html=True)

    # Check if we just created a session
    if 'temp_session_code' in st.session_state:
        # CREATED SESSION - just need name to join
        code_to_join = st.session_state.temp_session_code
        st.markdown(f"<div class='session-code'>{code_to_join}</div>", unsafe_allow_html=True)
        st.markdown("<p class='helper-text'>Share this code with your team</p>", unsafe_allow_html=True)

        username = st.text_input("Your Name", value=st.session_state.last_username, placeholder="Enter your name", key="join_username")

        if st.button("Join as Voter", use_container_width=True, type="primary"):
            if username:
                if join_session(code_to_join, username, False):
                    del st.session_state.temp_session_code
                    st.rerun()
            else:
                st.warning("Please enter your name")

        if st.button("Join as Observer", use_container_width=True, type="secondary"):
            if username:
                if join_session(code_to_join, username, True):
                    del st.session_state.temp_session_code
                    st.rerun()
            else:
                st.warning("Please enter your name")

        st.markdown("---")
        if st.button("Cancel", use_container_width=True, type="secondary"):
            del st.session_state.temp_session_code
            st.rerun()

    else:
        # LANDING - create or join
        if st.button("Create New Session", use_container_width=True):
            code = create_session()
            st.session_state.temp_session_code = code
            st.rerun()

        st.markdown("<p class='section-header'>Or join existing</p>", unsafe_allow_html=True)

        join_code = st.text_input("Session Code", max_chars=4, placeholder="ABCD").upper()

        if join_code:
            username = st.text_input("Your Name", value=st.session_state.last_username, placeholder="Enter your name", key="join_username")

            if st.button("Join as Voter", use_container_width=True, type="primary"):
                if username:
                    if join_session(join_code, username, False):
                        st.rerun()
                    else:
                        st.error("Session not found")
                else:
                    st.warning("Please enter your name")

            if st.button("Join as Observer", use_container_width=True, type="secondary"):
                if username:
                    if join_session(join_code, username, True):
                        st.rerun()
                    else:
                        st.error("Session not found")
                else:
                    st.warning("Please enter your name")

else:
    # SESSION SCREEN - fetch fresh data from Supabase
    session = get_session_data(st.session_state.current_session)

    st.markdown(f"<div class='session-code'>{st.session_state.current_session}</div>", unsafe_allow_html=True)

    all_voted = all_voters_voted(session)
    votes_revealed = session['votes_revealed'] or all_voted

    # Auto-reveal when all voted
    if all_voted and not session['votes_revealed']:
        reveal_votes(st.session_state.current_session)
        votes_revealed = True

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
        leave_session(st.session_state.current_session, st.session_state.user_name)
        st.session_state.current_session = None
        st.session_state.user_name = None
        st.session_state.is_observer = None
        st.query_params.clear()
        st.rerun()
