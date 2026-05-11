import streamlit as st
from openai import OpenAI

# --- PAGE SETUP ---
st.set_page_config(page_title="Mental Health Companion", page_icon="🌱")
st.title("🌱 Student Mental Health Companion")
st.caption("A supportive chatbot powered by Hugging Face models using the OpenAI library.")
st.warning("**Disclaimer:** I am an AI, not a licensed therapist. If you are in a crisis, please reach out to university counseling services or a professional.")

# --- API KEY & CLIENT SETUP ---
# Replace this string with your actual Hugging Face token (starts with hf_)
hf_token = "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"

# Initialize the OpenAI client to point at Hugging Face's servers
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token
)

# Updated to a widely supported, highly empathetic model
HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# --- SESSION STATE & MEMORY ---
if "messages" not in st.session_state:
    # The system message secretly tells the AI how to behave
    st.session_state.messages = [
        {
            "role": "system", 
            "content": (
                "You are a warm, empathetic, and supportive mental health companion for university students. "
                "Validate their feelings, provide a brief comforting message, and offer one actionable relaxation tip "
                "(e.g., breathing exercises, grounding techniques). Keep your response concise, conversational, and natural. "
                "Do not pretend to be a real doctor."
            )
        }
    ]

# --- DISPLAY CHAT HISTORY ---
# Skip displaying the hidden system prompt
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT & RESPONSE ---
if prompt := st.chat_input("How are you feeling today?"):
    
    # 1. Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Save user message to memory
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Generate response from Hugging Face via OpenAI client
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Making the API call
            response = client.chat.completions.create(
                model=HF_MODEL,
                messages=st.session_state.messages,
                max_tokens=250, # Keep responses from getting too long
                temperature=0.7 # 0.7 gives a nice balance of creativity and focus
            )
            
            # Extract text response
            assistant_response = response.choices[0].message.content
            
            # Display response
            message_placeholder.markdown(assistant_response)
            
            # 4. Save assistant response to memory
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            st.error(f"An error occurred with the Hugging Face API: {e}")