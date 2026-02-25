import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="🚢 Titanic Dataset Chatbot",
    page_icon="🚢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    .delete-btn {
        opacity: 0.7;
        transition: opacity 0.2s;
    }
    .delete-btn:hover {
        opacity: 1;
    }
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .stats-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.3);
    }
    .welcome-message {
        text-align: center;
        color: #666;
        padding: 3rem 1rem;
        background: linear-gradient(145deg, #f8f9ff 0%, #e8f4f8 100%);
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px dashed #007bff;
    }
    .welcome-message h3 {
        color: #007bff;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with gradient
st.markdown('<h1 class="main-header">🚢 Titanic Dataset Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">💬 Ask me anything about Titanic passengers! Get instant insights with beautiful visualizations.</p>', unsafe_allow_html=True)

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stats-card">
        <h4>📊 891</h4>
        <small>Passengers</small>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stats-card">
        <h4>📈 12</h4>
        <small>Features</small>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stats-card">
        <h4>🎯 100%</h4>
        <small>Accurate</small>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to add message to history
def add_message(role, content, image=None):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "image": image
    })

# Function to delete message
def delete_message(index):
    if 0 <= index < len(st.session_state.messages):
        del st.session_state.messages[index]

# Chat container with custom styling
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-message">
            <h3>🌟 Welcome to Titanic Chat!</h3>
            <p>I'm your AI assistant for exploring the famous Titanic dataset. Ask me questions like:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>"What percentage of passengers were male?"</li>
                <li>"Show me the age distribution"</li>
                <li>"How many passengers embarked from each port?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                # User message (right aligned with custom styling)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div style="text-align: right; margin: 10px 0;">
                        <div class="user-message">
                            <strong>👤 You:</strong><br>{message['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("❌", key=f"delete_user_{i}", help="Delete message", type="secondary"):
                        delete_message(i)
                        st.rerun()
            else:
                # Bot message (left aligned with custom styling)
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("❌", key=f"delete_bot_{i}", help="Delete message", type="secondary"):
                        delete_message(i)
                        st.rerun()
                with col2:
                    st.markdown(f"""
                    <div class="bot-message">
                        <strong>🤖 Titanic Assistant:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                    if message["image"]:
                        # Add a nice border to images
                        st.markdown("""
                        <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        """, unsafe_allow_html=True)
                        image_data = base64.b64decode(message["image"].split(",")[1])
                        st.image(Image.open(io.BytesIO(image_data)), use_container_width=True, caption="📊 Visualization")
                        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area with custom styling
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    question = st.text_input(
        "💭 Ask your question:",
        key="question_input",
        placeholder="e.g., What was the average ticket fare?",
        label_visibility="collapsed"
    )

with col2:
    ask_clicked = st.button("🚀 Send", use_container_width=True, type="primary")

if ask_clicked and question.strip():
    # Add user message
    add_message("user", question.strip())

    try:
        with st.spinner("🔍 Analyzing Titanic data... Please wait!"):
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question}
            )

        if response.status_code == 200:
            data = response.json()
            # Add bot response
            add_message("assistant", data["answer"], data.get("image"))
            st.success("✅ Response received!")
            st.rerun()
        else:
            st.error(f"❌ Backend error: {response.text}")

    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Clear history button with better styling
if st.session_state.messages:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ 🧹 Clear Entire Conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.success("🧹 Conversation cleared! Fresh start! ✨")
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>Built with ❤️ using FastAPI, Streamlit & Python | Data: Titanic Dataset</small>
</div>
""", unsafe_allow_html=True)