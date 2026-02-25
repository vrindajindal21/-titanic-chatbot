import streamlit as st
import requests
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

# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --primary: #1e3a8a;
        --secondary: #d4af37;
        --bg-glass: rgba(255, 255, 255, 0.8);
        --bot-bg: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        --user-bg: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    }

    .stApp {
        background-color: #f8fafc;
    }

    .main-header {
        font-family: 'Playfair Display', serif;
        background: linear-gradient(90deg, #1e3a8a, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #475569;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Glassmorphism containers */
    .glass-card {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 1rem;
    }

    /* Professional Chat Bubbles */
    .chat-bubble {
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        max-width: 85%;
        position: relative;
        font-family: 'Inter', sans-serif;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .user-bubble {
        background: var(--user-bg);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .bot-bubble {
        background: var(--bot-bg);
        color: #1e293b;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #e2e8f0;
    }

    .avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        margin-bottom: 5px;
    }

    /* Smooth Transitions */
    .stButton>button {
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: white;
    }

    .sidebar-header {
        font-family: 'Playfair Display', serif;
        color: #d4af37;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Hide default Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stats-container {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        flex: 1;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .stat-val {
        font-weight: 700;
        font-size: 1.5rem;
        color: #1e3a8a;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Suggestions Grid */
    .suggestion-btn {
        background: white;
        border: 1px solid #cbd5e1;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
        margin: 0.2rem;
        display: inline-block;
        transition: all 0.2s;
    }

    .suggestion-btn:hover {
        background: #f1f5f9;
        border-color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown('<div class="sidebar-header">🚢 Voyage Insights</div>', unsafe_allow_html=True)
    st.info("Explore the tragedy and triumph of the RMS Titanic through data-driven AI analysis.")
    
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
    st.caption("Developed by Vrinda Jindal")

# Main Content
main_col, side_col = st.columns([3, 1])

with main_col:
    st.markdown('<h1 class="main-header">RMS Titanic Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">An AI-powered dive into history through the lens of data</p>', unsafe_allow_html=True)

    # Stats Ribbon
    st.markdown("""
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-val">891</div>
            <div class="stat-label">Manifest</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">38.4%</div>
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
            <div class="glass-card" style="text-align: center; border-left: 5px solid #d4af37;">
                <h3>⚓ Welcome Aboard</h3>
                <p>I can help you analyze the passenger manifest, visualize demographics, and uncover patterns. 
                Ask me anything about the manifest or select a suggestion below.</p>
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
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Message the manifestation...", placeholder="e.g., How many children were on board?", label_visibility="collapsed")
        with col2:
            send_btn = st.button("⚓ Send", type="primary", use_container_width=True)

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
                response = requests.post("http://127.0.0.1:8000/ask", json={"question": final_query})
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
