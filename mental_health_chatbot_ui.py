import streamlit as st
from openai import OpenAI
import time
import random
import pandas as pd
import plotly.express as px

# ---------------- PAGE SETUP & UI DESIGN ----------------
st.set_page_config(page_title="Mental Health Companion", page_icon="🌱", layout="centered")

# Theme Toggle
with st.sidebar:
    st.header("⚙️ Configuration")
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

# Inject Custom Premium CSS (Dynamic based on theme)
if dark_mode:
    bg_color = "#121212"
    secondary_bg = "#1E1E1E"
    text_color = "#E0E0E0"
    border_color = "#333333"
    card_shadow = "rgba(0,0,0,0.5)"
    circle_gradient = "linear-gradient(135deg, #1E88E5, #4CAF50)"
else:
    bg_color = "#F7FAF7"
    secondary_bg = "#E8F0E8"
    text_color = "#2C3E2D"
    border_color = "#d1e0d1"
    card_shadow = "rgba(0,0,0,0.03)"
    circle_gradient = "linear-gradient(135deg, #4CAF50, #81C784)"

css = f"""
<style>
    .stApp {{
        background-color: {bg_color} !important;
    }}
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label {{
        color: {text_color} !important;
    }}
    div[data-testid="stSidebar"] {{
        background-color: {secondary_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    .breathing-circle {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: {circle_gradient} !important;
        margin: 40px auto;
        animation: breathe 10s infinite ease-in-out;
        box-shadow: 0 10px 20px {card_shadow} !important;
    }}
    @keyframes breathe {{
        0% {{ transform: scale(0.8); opacity: 0.8; }}
        40% {{ transform: scale(1.3); opacity: 1; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
        100% {{ transform: scale(0.8); opacity: 0.8; }}
    }}
    .feature-card {{
        background: {secondary_bg} !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px {card_shadow} !important;
        margin-bottom: 20px;
        border: 1px solid {border_color} !important;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("🌱 Student Mental Health Companion")
st.caption("A premium, supportive AI chatbot for student mental well-being")

st.info("⚠️ **Note:** I am an AI companion, not a licensed therapist. If you're in crisis, please seek professional help.")

# ---------------- API SETUP ----------------
try:
    hf_token = st.secrets.get("HF_TOKEN")
except Exception:
    hf_token = None

with st.sidebar:
    if not hf_token:
        hf_token = st.text_input("HuggingFace API Token", type="password", help="Get your token from https://huggingface.co/settings/tokens")
    else:
        st.success("✅ API Key loaded securely from secrets!")

if hf_token:
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=hf_token
    )
else:
    client = None

HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"system",
            "content":
            "You are a warm, empathetic mental health companion for university students. "
            "Always be highly supportive, validate their feelings, and occasionally suggest using the app's built-in wellness tools (like the visual breathing exercise, music therapy, or the CBT Reframing tool)."
        }
    ]

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# ---------------- FEATURES ----------------

def breathing_exercise():
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🧘 Visual Breathing Exercise")
    st.markdown(f"<p style='text-align:center;'>Follow the expanding and contracting circle. Breathe in as it grows, hold, and breathe out as it shrinks.</p>", unsafe_allow_html=True)
    st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def suggest_music():
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🎧 Relaxing Lo-Fi Music")
    music_links = ["https://youtu.be/5qap5aO4i9A", "https://youtu.be/jfKfPfyJRdk"]
    st.video(random.choice(music_links))
    st.markdown('</div>', unsafe_allow_html=True)

def suggest_comedy():
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("😂 A Little Laughter")
    comedy_links = [
        "https://www.youtube.com/watch?v=4Xo3Fq7GGWk",
        "https://www.youtube.com/watch?v=R8v7TwlYCt0",
        "https://www.youtube.com/watch?v=VvPaEsuz-tY"
    ]
    st.video(random.choice(comedy_links))
    st.markdown('</div>', unsafe_allow_html=True)

def mood_tracker():
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📊 Mood Analytics")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        mood = st.selectbox("How are you feeling right now?", ["Happy", "Calm", "Stressed", "Sad", "Angry"])
    with col2:
        st.write("")
        st.write("")
        if st.button("Save Mood", use_container_width=True):
            st.session_state.mood_history.append(mood)
            st.success("Mood saved! 🌟")

    if len(st.session_state.mood_history) > 0:
        df = pd.DataFrame(st.session_state.mood_history, columns=["Mood"])
        chart_data = df.value_counts().reset_index()
        chart_data.columns = ["Mood", "Count"]
        
        color_map = {"Happy": "#FFD700", "Calm": "#4CAF50", "Stressed": "#FF9800", "Sad": "#2196F3", "Angry": "#F44336"}
        
        fig = px.pie(chart_data, values='Count', names='Mood', color='Mood', color_discrete_map=color_map, hole=0.5)
        # Fix plotly background for dark mode
        fig.update_layout(margin=dict(t=20, b=20, l=0, r=0), showlegend=False, 
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(color=text_color))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def cbt_reframing():
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🧠 CBT Thought Reframing")
    st.write("Write down a negative thought you're having, and the AI will help you reframe it into a more balanced perspective.")
    
    negative_thought = st.text_area("Your negative thought:", height=100)
    if st.button("Reframe Thought", type="primary"):
        if negative_thought and client:
            with st.spinner("Analyzing your thought..."):
                prompt = f"Act as a CBT therapist. The user has this negative thought: '{negative_thought}'. Identify any cognitive distortions and provide a healthier, balanced reframed thought. Keep it under 3 sentences."
                try:
                    response = client.chat.completions.create(
                        model=HF_MODEL,
                        messages=[{"role":"system", "content":prompt}],
                        max_tokens=200,
                        temperature=0.7
                    )
                    reply = response.choices[0].message.content
                    st.success("Reframed Perspective:")
                    st.write(reply)
                except Exception as e:
                    st.error("Error connecting to AI.")
        elif not client:
            st.warning("Please configure your API key in the sidebar.")
    st.markdown('</div>', unsafe_allow_html=True)

def crisis_detection(text):
    keywords = ["suicide", "kill myself", "want to die", "end my life"]
    for k in keywords:
        if k in text.lower():
            st.error(
            """
            🚨 **You are not alone.**

            Please reach out to someone immediately.
            
            **India Mental Health Helpline:** 📞 9152987821
            """
            )

# ---------------- MAIN LAYOUT ----------------

tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🛠️ Wellness Tools", "📝 Daily Journal"])

with tab1:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            avatar = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    if prompt := st.chat_input("How are you feeling today?"):
        crisis_detection(prompt)

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            try:
                if not client:
                    st.error("Please enter your HuggingFace API Token in the sidebar to continue.")
                    st.stop()

                response = client.chat.completions.create(
                    model=HF_MODEL,
                    messages=st.session_state.messages,
                    max_tokens=250,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                placeholder.markdown(reply)
                st.session_state.messages.append({"role":"assistant","content":reply})

            except Exception as e:
                st.error(f"API Error: {e}")

        # Smart Triggers
        if any(word in prompt.lower() for word in ["stress", "anxious", "panic", "overwhelmed"]):
            st.info("💡 I noticed you might be stressed. Check out the **Wellness Tools** tab for a calming CBT Reframing exercise!")
        if any(word in prompt.lower() for word in ["sad", "depressed", "down"]):
            st.info("💡 I noticed you might be feeling down. Check out the **Wellness Tools** tab for some relaxing music or comedy.")

with tab2:
    # Selective Tool Rendering
    st.write("### Choose a Tool")
    selected_tool = st.radio("Select Tool", 
                             ["🧘 Breathing Exercise", "🧠 CBT Reframing", "🎧 Relaxing Music", "😂 Comedy", "📊 Mood Tracker"], 
                             horizontal=True, label_visibility="collapsed")
    
    st.divider()
    
    if selected_tool == "🧘 Breathing Exercise":
        breathing_exercise()
    elif selected_tool == "🧠 CBT Reframing":
        cbt_reframing()
    elif selected_tool == "🎧 Relaxing Music":
        suggest_music()
    elif selected_tool == "😂 Comedy":
        suggest_comedy()
    elif selected_tool == "📊 Mood Tracker":
        mood_tracker()

with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📝 Private Reflection Journal")
    st.write("Writing down your thoughts can help reduce stress and clarify your feelings.")
    
    journal_entry = st.text_area("What's on your mind today?", height=150)
    if st.button("Save Entry", type="primary"):
        if journal_entry:
            st.session_state.journal_entries.append({"date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "text": journal_entry})
            st.success("Journal entry saved securely for this session.")
        else:
            st.warning("Please write something before saving.")
            
    if st.session_state.journal_entries:
        st.divider()
        st.subheader("Past Entries")
        for entry in reversed(st.session_state.journal_entries):
            st.markdown(f"**{entry['date']}**")
            st.info(entry['text'])
    st.markdown('</div>', unsafe_allow_html=True)