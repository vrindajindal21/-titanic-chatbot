import streamlit as st
import requests
import os
from PIL import Image
import io
import base64
import time

st.set_page_config(
    page_title="Titanic AI Explorer",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Luxury Nautical Light CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap');

    :root {
        --primary: #1e3a8a;
        --secondary: #d4af37;
        --bg-main: #f8fafc;
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-main: #1e293b;
        --text-sub: #64748b;
        --accent-soft: rgba(212, 175, 55, 0.1);
    }

    /* Elegant Light Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--text-main);
    }

    /* Smooth Entry Animations */
    @keyframes slideReveal {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Typography */
    .main-header {
        font-family: 'Playfair Display', serif;
        background: linear-gradient(to right, #1e3a8a, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
        animation: slideReveal 0.8s ease-out;
    }

    .subtitle {
        font-family: 'Outfit', sans-serif;
        text-align: center;
        color: var(--text-sub);
        font-size: 1.1rem;
        font-weight: 500;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 3.5rem;
        animation: slideReveal 1s ease-out;
    }

    /* Premium Light Glass Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 0 15px 35px rgba(30, 58, 138, 0.05);
        margin-bottom: 2rem;
        animation: slideReveal 1.2s ease-out;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(30, 58, 138, 0.08);
        border-color: var(--secondary);
    }

    /* Polished Stats Ribbon */
    .stats-container {
        display: flex;
        justify-content: space-around;
        gap: 2rem;
        margin-bottom: 4rem;
        padding: 0 5%;
    }

    .stat-box {
        background: white;
        padding: 1.75rem;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        flex: 1;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        border-color: var(--secondary);
        transform: translateY(-3px);
    }

    .stat-val {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        color: var(--primary);
    }

    .stat-label {
        color: var(--text-sub);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Modern Chat Bubbles */
    .chat-bubble {
        padding: 1.25rem 1.75rem;
        border-radius: 24px;
        max-width: 80%;
        margin-bottom: 1.5rem;
        font-family: 'Outfit', sans-serif;
        line-height: 1.6;
        animation: slideReveal 0.5s ease-out;
    }

    .user-bubble {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
    }

    .bot-bubble {
        background: #ffffff;
        color: var(--text-main);
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
    }

    /* Premium Buttons */
    .stButton>button {
        background: #ffffff !important;
        color: var(--primary) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        box-shadow: 0 2px 50px rgba(0, 0, 0, 0.02) !important;
    }

    .stButton>button:hover {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
        transform: translateY(-2px) !important;
    }

    /* Sidebar - Luxury Slate */
    section[data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Force visibility for sidebar content */
    section[data-testid="stSidebar"] .stMarkdown h3, 
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stExpander p {
        color: #f8fafc !important;
    }

    .sidebar-header {
        font-family: 'Playfair Display', serif;
        color: var(--secondary);
        font-size: 1.65rem;
        margin-bottom: 2rem;
        text-align: center;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding-bottom: 1rem;
    }
    
    /* FAQ Expander Visibility */
    section[data-testid="stSidebar"] .styled-expander {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: var(--secondary) !important;
        color: #0f172a !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    
    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
</style>



""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown('<div class="sidebar-header">🚢 Voyage Insights</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid var(--secondary); border-radius: 12px; padding: 12px; margin-bottom: 20px;">
        <p style="color: #d4af37; font-size: 0.85rem; margin: 0;"><strong>System Status:</strong> <span style="color: #4ade80;">● Online</span></p>
        <p style="color: #94a3b8; font-size: 0.75rem; margin: 5px 0 0 0;">Dataset: train.csv (891 rows)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Feature Explorer")
    if st.button("📊 Passenger Demographics", use_container_width=True):
        st.session_state.feature_trigger = "tell me everything about the ages"
    if st.button("🔗 Survival Correlations", use_container_width=True):
        st.session_state.feature_trigger = "show me all correlations"
    if st.button("💰 Fare & Class Analysis", use_container_width=True):
        st.session_state.feature_trigger = "average fares by class"
    if st.button("🚢 Cabin Deck Mapping", use_container_width=True):
        st.session_state.feature_trigger = "survival rates by cabin deck"
    
    st.markdown("---")
    st.markdown("### 💡 FAQ")
    with st.expander("How accurate is this?"):
        st.write("Using the official 891-passenger training set. Calculations are 100% deterministic based on this data.")
    
    if st.button("🗑️ Clear Archive", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.7;">
        <p style="font-size: 0.7rem; color: #94a3b8; margin: 0;">Developed by</p>
        <p style="font-size: 0.9rem; color: white; font-weight: 600; margin: 0;">Vrinda Jindal</p>
        <p style="font-size: 0.6rem; color: #d4af37; margin-top: 5px;">VERSION 3.0 • PREMIUM RELEASE</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
main_col, side_col = st.columns([3.2, 1])

with main_col:
    st.markdown('<h1 class="main-header">RMS TITANIC</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Official Voyage Ledger & Data Insights</p>', unsafe_allow_html=True)

    # Stats Ribbon
    st.markdown("""
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-val">891</div>
            <div class="stat-label">Manifest</div>
        </div>
        <div class="stat-box" style="border-bottom: 3px solid var(--secondary);">
            <div class="stat-val" style="color: var(--secondary);">38.4%</div>
            <div class="stat-label">Survival</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">12</div>
            <div class="stat-label">Dimensions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat Container
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_placeholder = st.container()

    with chat_placeholder:
        if not st.session_state.messages:
            st.markdown("""
            <div class="glass-card" style="text-align: center; border-left: 5px solid var(--secondary); background: linear-gradient(to right, #ffffff, #f8fafc);">
                <div style="font-size: 3.5rem; margin-bottom: 15px;">⚓</div>
                <h2 style="color: var(--primary); font-family: 'Outfit', sans-serif; font-weight: 800; letter-spacing: -0.02em; font-size: 2.2rem;">Begin Archive Analysis</h2>
                <p style="color: var(--text-sub); max-width: 75%; margin: 10px auto 25px; line-height: 1.6; font-size: 1.05rem;">
                    Access the complete 1912 passenger manifest. Query our AI engine to cross-reference demographics, survival statistics, and historical records.
                </p>
                <div style="display: flex; justify-content: center; gap: 25px; padding: 15px; background: #f1f5f9; border-radius: 15px; border: 1px solid #e2e8f0;">
                    <div style="text-align: center;"><div style="color: var(--primary); font-weight: 700;">891</div><div style="font-size: 0.65rem; color: var(--text-sub); font-weight: 600;">PASSENGERS</div></div>
                    <div style="text-align: center;"><div style="color: var(--secondary); font-weight: 700;">READY</div><div style="font-size: 0.65rem; color: var(--text-sub); font-weight: 600;">DATABASE</div></div>
                    <div style="text-align: center;"><div style="color: #059669; font-weight: 700;">ACTIVE</div><div style="font-size: 0.65rem; color: var(--text-sub); font-weight: 600;">AI ENGINE</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        for i, msg in enumerate(st.session_state.messages):
            role_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            avatar = "👤" if msg["role"] == "user" else "🤖"
            
            # Clean content to prevent HTML breaking
            display_content = msg['content'].replace('\n', '<br>')
            
            st.markdown(f"""
            <div class="chat-bubble {role_class}">
                <div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 5px;">{avatar} {msg['role'].upper()}</div>
                {display_content}
            </div>
            """, unsafe_allow_html=True)
            
            if msg.get("image"):
                try:
                    image_data = base64.b64decode(msg["image"].split(",")[1])
                    st.image(Image.open(io.BytesIO(image_data)), use_container_width=True)
                except:
                    st.error("Could not render visualization archive.")

    # Input Section
    st.markdown("---")
    
    # Suggestions
    st.markdown("**Try asking:**")
    cols = st.columns(3)
    suggestions = [
        "What was the survival rate of first class?",
        "Show me the age distribution",
        "Who was the oldest passenger?"
    ]
    
    selected_query = None
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"sug_{i}", use_container_width=True):
            selected_query = suggestion

    # Input Bar
    with st.container():
        with st.form("chat_input_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input("Message the manifestation...", placeholder="e.g., How many children were on board?", label_visibility="collapsed")
            with col2:
                send_btn = st.form_submit_button("⚓ Send", use_container_width=True)

    # Determine final query from text input, suggestions, or sidebar features
    final_query = None
    if selected_query:
        final_query = selected_query
    elif send_btn and user_input:
        final_query = user_input
    elif "feature_trigger" in st.session_state and st.session_state.feature_trigger:
        final_query = st.session_state.feature_trigger
        st.session_state.feature_trigger = None # Clear after use

    if final_query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": final_query})
        
        # UI interaction
        with st.spinner("🚢 Navigating the data archives..."):
            try:
                # Prioritize Streamlit Secrets, then Env Vars, then Local Fallback
                backend_url = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
                response = requests.post(f"{backend_url}/ask", json={"question": final_query})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": data["answer"], 
                        "image": data.get("image")
                    })
                    st.rerun()
                else:
                    st.error("Telegraph interrupted. Backend unreachable.")
            except Exception as e:
                st.error(f"Collision detected: {str(e)}")

with side_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Metrics Hub")
    st.metric("Total Records", "891", delta="Full Set")
    st.metric("Searchable Names", "891", delta="100%")
    st.metric("Visualizations", "15+", delta="Available")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card" style="background: #1e3a8a; color: white;">', unsafe_allow_html=True)
    st.markdown("### 💡 Pro Tip")
    st.write("You can search for specific people! Try 'Who is Jack Fortune?' or 'Search for passenger 303'.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; color: #94a3b8; font-size: 0.8rem;">
    RMS Titanic AI Explorer &copy; 2026 | Built for Historical Research
</div>
""", unsafe_allow_html=True)
