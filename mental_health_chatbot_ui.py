import streamlit as st
from openai import OpenAI
import time
import random
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Mental Health Companion", page_icon="🌱", layout="centered")

st.title("🌱 Student Mental Health Companion")
st.caption("A supportive AI chatbot for student mental well-being")

st.warning("⚠️ I am an AI companion, not a licensed therapist.")

# ---------------- API SETUP ----------------
with st.sidebar:
    st.header("⚙️ Configuration")
    hf_token = st.text_input("HuggingFace API Token", value="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", type="password", help="Get your token from https://huggingface.co/settings/tokens")

if hf_token:
    client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token
)

HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"system",
            "content":
            "You are a warm mental health companion for university students. "
            "Be empathetic, supportive and suggest simple coping strategies."
        }
    ]

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# ---------------- BREATHING EXERCISE ----------------

def breathing_exercise():

    st.subheader("🧘 Breathing Exercise")

    phases = [
        ("Inhale deeply",4),
        ("Hold breath",4),
        ("Exhale slowly",6)
    ]

    progress = st.progress(0)

    for text,sec in phases:

        for i in range(sec):

            st.write(text)
            progress.progress((i+1)/sec)
            time.sleep(1)

    st.success("Great job! You completed the breathing exercise.")

# ---------------- MUSIC THERAPY ----------------

def suggest_music():

    st.subheader("🎧 Try relaxing music")

    music_links = [
        "https://youtu.be/5qap5aO4i9A",
        "https://youtu.be/jfKfPfyJRdk"
    ]

    st.video(random.choice(music_links))

# ---------------- COMEDY SUGGESTION ----------------

def suggest_comedy():

    st.subheader("😂 A little laughter might help")

    comedy_links = [
        "https://www.youtube.com/watch?v=4Xo3Fq7GGWk",
        "https://www.youtube.com/watch?v=R8v7TwlYCt0",
        "https://www.youtube.com/watch?v=VvPaEsuz-tY"
    ]

    st.video(random.choice(comedy_links))
    for link in comedy_links:
        st.markdown(f"👉 Watch here: {link}")

# ---------------- MOOD TRACKER ----------------

def mood_tracker():

    st.subheader("📊 Mood Tracker")

    mood = st.selectbox(
        "How are you feeling today?",
        ["Happy","Calm","Stressed","Sad","Angry"]
    )

    if st.button("Save Mood"):
        st.session_state.mood_history.append(mood)
        st.success("Mood saved!")

    if len(st.session_state.mood_history) > 0:

        df = pd.DataFrame(st.session_state.mood_history, columns=["Mood"])

        chart = df.value_counts().reset_index()
        chart.columns = ["Mood","Count"]

        st.bar_chart(chart.set_index("Mood"))

# ---------------- CRISIS DETECTION ----------------

def crisis_detection(text):

    keywords = [
        "suicide",
        "kill myself",
        "want to die",
        "end my life"
    ]

    for k in keywords:

        if k in text.lower():

            st.error(
            """
            🚨 You are not alone.

            Please reach out to someone immediately.

            India Mental Health Helpline  
            📞 9152987821
            """
            )

# ---------------- CHAT HISTORY ----------------

for msg in st.session_state.messages:

    if msg["role"] != "system":

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------

if prompt := st.chat_input("How are you feeling today?"):

    crisis_detection(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:

            response = client.chat.completions.create(
                model=HF_MODEL,
                messages=st.session_state.messages,
                max_tokens=250,
                temperature=0.7
            )

            reply = response.choices[0].message.content

            placeholder.markdown(reply)

            st.session_state.messages.append(
                {"role":"assistant","content":reply}
            )

        except Exception as e:

            st.error(f"API Error: {e}")

    # -------- TRIGGER FEATURES --------

    if "stress" in prompt or "anxious" in prompt:

        breathing_exercise()

    if "sad" in prompt or "depressed" in prompt:

        suggest_music()
        suggest_comedy()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("Wellness Tools")

    if st.button("🧘 Breathing Exercise"):
        breathing_exercise()

    if st.button("🎧 Relaxing Music"):
        suggest_music()

    if st.button("😂 Watch Comedy"):
        suggest_comedy()

    mood_tracker()
