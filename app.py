import streamlit as st
import random
import string
from datetime import datetime
import statistics

# Page config
st.set_page_config(
    page_title="Pointing Poker",
    page_icon="✦",
    layout="centered"
)

# Apple-inspired design system
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background-color: #FAFAFA;
        max-width: 600px;
        margin: 0 auto;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 540px;
    }

    h1 {
        font-weight: 600;
        font-size: 1.75rem;
        color: #1D1D1F;
        text-align: center;
        letter-spacing: -0.02em;
    }

    h2, h3 {
        font-weight: 600;
        color: #1D1D1F;
        letter-spacing: -0.01em;
    }

    .stButton>button {
        background-color: #007AFF;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        font-size: 15px;
        letter-spacing: -0.01em;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 122, 255, 0.2);
    }

    .stButton>button:hover {
        background-color: #0066D6;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.25);
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    .stButton>button[kind="secondary"] {
        background-color: #F5F5F7;
        color: #1D1D1F;
        box-shadow: none;
    }

    .stButton>button[kind="secondary"]:hover {
        background-color: #E8E8ED;
    }

    /* Session code display */
    .session-code {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 16px;
        font-size: 20px;
        font-weight: 600;
        text-align: center;
        letter-spacing: 4px;
        margin: 24px auto;
        max-width: 280px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }

    /* Participant badges */
    .participant-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin: 16px 0;
    }

    .user-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 14px;
        letter-spacing: -0.01em;
    }

    .user-badge.voted {
        background-color: #E8F5E9;
        color: #2E7D32;
    }

    .user-badge.waiting {
        background-color: #F5F5F7;
        color: #86868B;
    }

    .user-badge.observer {
        background-color: #E3F2FD;
        color: #1565C0;
    }

    /* Stats card */
    .stats-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        margin: 20px 0;
        text-align: center;
    }

    .stat-value {
        font-size: 32px;
        font-weight: 600;
        color: #1D1D1F;
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: 13px;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Consensus indicators */
    .consensus-high {
        color: #34C759;
        font-weight: 600;
    }

    .consensus-medium {
        color: #FF9500;
        font-weight: 600;
    }

    .consensus-low {
        color: #FF3B30;
        font-weight: 600;
    }

    /* Vote results */
    .vote-result {
        display: inline-block;
        background: #F5F5F7;
        padding: 8px 16px;
        border-radius: 10px;
        margin: 4px;
        font-size: 14px;
    }

    .vote-result-name {
        color: #86868B;
    }

    .vote-result-value {
        color: #1D1D1F;
        font-weight: 600;
        margin-left: 6px;
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: #E5E5EA;
        margin: 32px 0;
    }

    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #E5E5EA;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.2s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #007AFF;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }

    /* Section headers */
    .section-header {
        font-size: 13px;
        font-weight: 600;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        text-align: center;
    }

    /* Center content */
    .centered {
        text-align: center;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Subtle animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeIn 0.3s ease-out;
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
    """Generate a random 6-character session code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_session():
    """Create a new session"""
    code = generate_session_code()
    st.session_state.sessions[code] = {
        'users': {},
        'votes': {},
        'created_at': datetime.now(),
        'votes_revealed': False
    }
    return code

def join_session(code, username, is_observer):
    """Join an existing session"""
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
    """Cast or update a vote"""
    if session_code in st.session_state.sessions:
        st.session_state.sessions[session_code]['votes'][username] = vote

def clear_votes(session_code):
    """Clear all votes for a new round"""
    if session_code in st.session_state.sessions:
        st.session_state.sessions[session_code]['votes'] = {}
        st.session_state.sessions[session_code]['votes_revealed'] = False

def kick_user(session_code, username):
    """Remove a user from the session"""
    if session_code in st.session_state.sessions:
        session = st.session_state.sessions[session_code]
        if username in session['users']:
            del session['users'][username]
        if username in session['votes']:
            del session['votes'][username]

def all_voters_voted(session_code):
    """Check if all voters have cast their votes"""
    if session_code not in st.session_state.sessions:
        return False

    session = st.session_state.sessions[session_code]
    voters = [u for u, data in session['users'].items() if not data['is_observer']]

    if not voters:
        return False

    return all(voter in session['votes'] for voter in voters)

def calculate_stats(votes):
    """Calculate voting statistics"""
    if not votes:
        return None

    # Filter out "?" votes for numerical calculations
    numeric_votes = [float(v) for v in votes.values() if v != "?"]

    if not numeric_votes:
        return {
            'most_common': "?",
            'average': None,
            'consensus': "No numerical votes"
        }

    # Most common vote
    vote_counts = {}
    for vote in votes.values():
        vote_counts[vote] = vote_counts.get(vote, 0) + 1
    most_common = max(vote_counts.items(), key=lambda x: x[1])

    # Average
    avg = statistics.mean(numeric_votes)

    # Consensus indicator (based on standard deviation)
    if len(numeric_votes) > 1:
        stdev = statistics.stdev(numeric_votes)
        if stdev <= 1:
            consensus = "High"
            consensus_class = "consensus-high"
        elif stdev <= 2:
            consensus = "Medium"
            consensus_class = "consensus-medium"
        else:
            consensus = "Low"
            consensus_class = "consensus-low"
    else:
        consensus = "—"
        consensus_class = "consensus-medium"

    return {
        'most_common': most_common[0],
        'most_common_count': most_common[1],
        'average': round(avg, 1),
        'consensus': consensus,
        'consensus_class': consensus_class
    }

# Main app logic
st.markdown("<h1>✦ Pointing Poker</h1>", unsafe_allow_html=True)

# If not in a session, show join/create options
if st.session_state.current_session is None:
    st.markdown("<p class='centered' style='color: #86868B; margin-bottom: 32px;'>Estimate together, align faster</p>", unsafe_allow_html=True)

    # Create session button
    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    if st.button("Create New Session", use_container_width=True):
        code = create_session()
        st.session_state.temp_session_code = code
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Join existing session
    st.markdown("<p class='section-header'>Or join existing</p>", unsafe_allow_html=True)
    join_code = st.text_input("Session code", max_chars=6, placeholder="Enter 6-digit code", label_visibility="collapsed").upper()

    # Show join form if we have a code
    if join_code or 'temp_session_code' in st.session_state:
        code_to_join = join_code if join_code else st.session_state.get('temp_session_code', '')

        if 'temp_session_code' in st.session_state and not join_code:
            st.markdown(f"<div class='session-code'>{code_to_join}</div>", unsafe_allow_html=True)
            st.markdown("<p class='centered' style='color: #86868B; font-size: 14px;'>Share this code with your team</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        default_name = st.session_state.last_username if st.session_state.last_username else ""
        username = st.text_input("Your name", value=default_name, placeholder="Enter your name", key="join_username")

        st.markdown("<br>", unsafe_allow_html=True)

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

        if st.button("Join as Observer", use_container_width=True):
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
    # In a session
    session = st.session_state.sessions[st.session_state.current_session]

    # Session code display
    st.markdown(f"<div class='session-code'>{st.session_state.current_session}</div>", unsafe_allow_html=True)

    # Check if all voters have voted
    all_voted = all_voters_voted(st.session_state.current_session)
    votes_revealed = session['votes_revealed'] or all_voted

    # Voting interface (only for voters)
    if not st.session_state.is_observer:
        st.markdown("<p class='section-header'>Your estimate</p>", unsafe_allow_html=True)

        current_vote = session['votes'].get(st.session_state.user_name)

        # Create a clean grid of vote buttons
        cols = st.columns(4)
        for idx, option in enumerate(VOTE_OPTIONS):
            with cols[idx % 4]:
                is_selected = current_vote == option
                button_type = "primary" if is_selected else "secondary"
                if st.button(option, key=f"vote_{option}", use_container_width=True, type=button_type):
                    cast_vote(st.session_state.current_session, st.session_state.user_name, option)
                    st.rerun()

    st.markdown("---")

    # Show current voting status
    st.markdown("<p class='section-header'>Participants</p>", unsafe_allow_html=True)

    voters = {u: data for u, data in session['users'].items() if not data['is_observer']}
    observers = {u: data for u, data in session['users'].items() if data['is_observer']}

    # Display voters
    voter_badges = "<div class='participant-list'>"
    for username in voters:
        has_voted = username in session['votes']
        badge_class = "voted" if has_voted else "waiting"
        status = "✓" if has_voted else "···"
        voter_badges += f"<span class='user-badge {badge_class}'>{username} {status}</span>"
    voter_badges += "</div>"

    if voters:
        st.markdown(voter_badges, unsafe_allow_html=True)
    else:
        st.markdown("<p class='centered' style='color: #86868B;'>No voters yet</p>", unsafe_allow_html=True)

    # Display observers
    if observers:
        observer_badges = "<div class='participant-list'>"
        for username in observers:
            observer_badges += f"<span class='user-badge observer'>{username} 👁</span>"
        observer_badges += "</div>"
        st.markdown(observer_badges, unsafe_allow_html=True)

    # Reveal votes if all have voted
    if all_voted and not session['votes_revealed']:
        session['votes_revealed'] = True
        st.balloons()

    # Show results if votes are revealed
    if votes_revealed and session['votes']:
        st.markdown("---")
        st.markdown("<p class='section-header'>Results</p>", unsafe_allow_html=True)

        # Display all votes in a clean format
        vote_display = "<div class='centered'>"
        for username, vote in session['votes'].items():
            vote_display += f"<span class='vote-result'><span class='vote-result-name'>{username}</span><span class='vote-result-value'>{vote}</span></span>"
        vote_display += "</div>"
        st.markdown(vote_display, unsafe_allow_html=True)

        # Calculate and display statistics
        stats = calculate_stats(session['votes'])
        if stats:
            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                    <div class='stats-card'>
                        <div class='stat-value'>{stats['most_common']}</div>
                        <div class='stat-label'>Most Common</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                avg_display = stats['average'] if stats['average'] else "—"
                st.markdown(f"""
                    <div class='stats-card'>
                        <div class='stat-value'>{avg_display}</div>
                        <div class='stat-label'>Average</div>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div class='stats-card'>
                        <div class='stat-value {stats['consensus_class']}'>{stats['consensus']}</div>
                        <div class='stat-label'>Consensus</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Controls section
    if st.session_state.is_observer:
        st.markdown("<p class='section-header'>Controls</p>", unsafe_allow_html=True)

        if st.button("Clear Votes", use_container_width=True):
            clear_votes(st.session_state.current_session)
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        users_to_kick = [u for u in session['users'].keys() if u != st.session_state.user_name]
        if users_to_kick:
            user_to_kick = st.selectbox("Remove participant", users_to_kick, label_visibility="collapsed")
            if st.button("Remove", use_container_width=True):
                kick_user(st.session_state.current_session, user_to_kick)
                st.rerun()

    # Leave session
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Leave Session", use_container_width=True):
        st.session_state.current_session = None
        st.session_state.user_name = None
        st.session_state.is_observer = None
        st.rerun()
