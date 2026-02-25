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

# Ultra-Premium CSS Overhaul
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:ital,wght@0,700;1,700&family=Outfit:wght@300;400;600&display=swap');

    :root {
        --primary: #0f172a;
        --accent: #d4af37;
        --accent-glow: rgba(212, 175, 55, 0.4);
        --bg-main: #fcfcfd;
        --card-bg: rgba(255, 255, 255, 0.9);
    }

    /* General Body Styling */
    .stApp {
        background: radial-gradient(circle at top right, #f8fafc, #eff6ff);
        font-family: 'Outfit', sans-serif;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Header Styling */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-style: italic;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 4.2rem;
        margin-top: -2rem;
        letter-spacing: -1px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 300;
    }

    /* Stats Cards with Neumorphism */
    .premium-stat {
        background: white;
        padding: 1.5rem;
        border-radius: 24px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 20px 20px 60px #d1d9e6, -20px -20px 60px #ffffff;
        transition: transform 0.3s ease;
    }
    .premium-stat:hover {
        transform: translateY(-5px);
    }
    .premium-stat-val {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #1e293b;
        display: block;
    }
    .premium-stat-label {
        font-size: 0.75rem;
        color: #d4af37;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Chat Area Enhancements */
    .chat-bubble {
        padding: 1.2rem 1.8rem;
        border-radius: 24px;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        font-size: 1.05rem;
        max-width: 80%;
        animation: fadeIn 0.4s ease-out both;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-bubble {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #f1f5f9;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        box-shadow: 0 10px 15px -3px rgba(30, 41, 59, 0.2);
    }

    .bot-bubble {
        background: white;
        color: #1e293b;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* Sidebar Logo-style Header */
    .sidebar-brand {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--accent);
    }

    /* Image Styling */
    .stImage img {
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Hide default Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar UI
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2 style="font-family: 'Playfair Display'; color: #d4af37; margin:0;">TITANIC</h2>
        <small style="color: #94a3b8; letter-spacing: 3px;">RESEARCH LABS</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏛️ Data Archives")
    if st.button("📊 Demographics Panel", use_container_width=True):
        st.session_state.feature_trigger = "tell me everything about the ages"
    if st.button("🔗 Survival Intelligence", use_container_width=True):
        st.session_state.feature_trigger = "show me all correlations"
    if st.button("💰 Economic Analysis", use_container_width=True):
        st.session_state.feature_trigger = "average fares by class"
    if st.button("⚓ Deck Archeology", use_container_width=True):
        st.session_state.feature_trigger = "survival rates by cabin deck"

    st.markdown("---")
    st.markdown("### � Status")
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem;">
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; border: 1px solid #334155;">
            <small style="color: #64748b;">MANIFEST</small><br>
            <b style="color: white;">891 Records</b>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; border: 1px solid #334155;">
            <small style="color: #64748b;">INTEGRITY</small><br>
            <b style="color: #10b981;">100%</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("� Reset Navigation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(f"Curated by Vrinda Jindal")
    st.caption("Intelligence Core v3.0 • Premium")

# Main Dashboard
hero_col, center_col, info_col = st.columns([1, 4, 1])

with center_col:
    st.markdown('<h1 class="main-header">Maritime Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Exploring the final voyage through algorithmic archeology</p>', unsafe_allow_html=True)

    # Stats Ribbon
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="premium-stat"><span class="premium-stat-label">Manifest</span><span class="premium-stat-val">891</span></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="premium-stat"><span class="premium-stat-label">Survival</span><span class="premium-stat-val">38%</span></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="premium-stat"><span class="premium-stat-label">Dimensions</span><span class="premium-stat-val">12</span></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="premium-stat"><span class="premium-stat-label">Deck Level</span><span class="premium-stat-val">8</span></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Chat Container
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_placeholder = st.container()

    with chat_placeholder:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 30px; border: 1px dashed #cbd5e1; margin-bottom: 2rem;">
                <h3 style="color: #0f172a; font-family: 'Playfair Display'; font-style: italic;">At Your Service, Explorer</h3>
                <p style="color: #64748b; max-width: 500px; margin: 0 auto;">Inquire about passenger fates, economic disparities, or structural patterns of the RMS Titanic project.</p>
            </div>
            """, unsafe_allow_html=True)
        
        for i, msg in enumerate(st.session_state.messages):
            role_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            avatar = "👤" if msg["role"] == "user" else "⚙️"
            display_content = msg['content'].replace('\n', '<br>')
            
            st.markdown(f"""
            <div class="chat-bubble {role_class}">
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.6; margin-bottom: 8px;">{avatar} {msg['role'].upper()}</div>
                {display_content}
            </div>
            """, unsafe_allow_html=True)
            
            if msg.get("image"):
                try:
                    image_data = base64.b64decode(msg["image"].split(",")[1])
                    st.image(Image.open(io.BytesIO(image_data)))
                except:
                    st.error("Visualization trace lost.")

    # Interaction Space
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Suggestions and Input
    st.markdown("<div style='text-align: center; margin-bottom: 15px;'><small style='color:#94a3b8;'>COMMAND SHORTCUTS</small></div>", unsafe_allow_html=True)
    cols = st.columns([1,1,1,1,1])
    s_list = ["Survival", "Ages", "Oldest", "Search", "Missing"]
    q_list = ["survival rate by class", "age distribution chart", "who was the oldest passenger", "search for passenger 303", "show me missing data"]
    
    selected_query = None
    for idx, s in enumerate(s_list):
        if cols[idx].button(s, key=f"s_{idx}", use_container_width=True):
            selected_query = q_list[idx]

    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Enter inquiry...", placeholder="e.g. Visualize the fare distribution", label_visibility="collapsed")
    with col2:
        send_btn = st.button("🚀 EXECUTE", type="primary", use_container_width=True)

    # Process Input Logic
    final_query = None
    if selected_query:
        final_query = selected_query
    elif send_btn and user_input:
        final_query = user_input
    elif "feature_trigger" in st.session_state and st.session_state.feature_trigger:
        final_query = st.session_state.feature_trigger
        st.session_state.feature_trigger = None

    if final_query:
        st.session_state.messages.append({"role": "user", "content": final_query})
        with st.spinner("Processing Maritime Logic..."):
            try:
                response = requests.post("http://127.0.0.1:8000/ask", json={"question": final_query})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.messages.append({"role": "assistant", "content": data["answer"], "image": data.get("image")})
                    st.rerun()
                else:
                    st.error("System Desynchronized.")
            except Exception as e:
                st.error(f"Logic Fault: {str(e)}")

# Vertical Accents
with hero_col:
    st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='writing-mode: vertical-rl; text-orientation: mixed; color: #cbd5e1; font-size: 3rem; font-family: Montserrat; letter-spacing: 15px; opacity: 0.3;'>V O Y A G E</p>", unsafe_allow_html=True)

with info_col:
    st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='writing-mode: vertical-rl; text-orientation: mixed; color: #cbd5e1; font-size: 3rem; font-family: Montserrat; letter-spacing: 15px; opacity: 0.3;'>D A T A</p>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; color: #94a3b8; font-size: 0.8rem;">
    RMS Titanic Maritime Intelligence &copy; 2026 | Historical Data Explorer
</div>
""", unsafe_allow_html=True)
