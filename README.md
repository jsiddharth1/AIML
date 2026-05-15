# 🌱 Student Mental Health Companion

A modern, empathetic AI-powered mental health chatbot built with **Streamlit** and **Hugging Face's LLaMA-3.1-8B-Instruct** model. This application serves as a supportive, private companion specifically tailored for university students. It combines an advanced conversational AI with interactive wellness tools to help users manage stress, track their moods, and reframe negative thoughts.

---

## 🌟 Features

- **💬 AI Chat Assistant:** A warm, empathetic conversational agent that validates feelings and suggests wellness tools. Powered by Meta's LLaMA 3.1 model via Hugging Face.
- **🚨 Crisis Detection:** Automatically detects high-risk keywords and provides immediate access to mental health helpline numbers.
- **🛠️ Interactive Wellness Tools:**
  - **🧘 Visual Breathing Exercise:** An animated visual guide to help users regulate their breathing and calm their nervous system.
  - **🧠 CBT Thought Reframing:** Uses AI to identify cognitive distortions in negative thoughts and helps users reframe them into healthier, balanced perspectives.
  - **🎧 Relaxing Media:** Curated suggestions for Lo-Fi relaxing music and lighthearted comedy videos.
  - **📊 Mood Tracker & Analytics:** Allows users to log their mood and visualizes their emotional trends using interactive `Plotly` pie charts.
- **📝 Private Reflection Journal:** A secure space for users to write down their thoughts and track daily entries within the session.
- **🎨 Premium UI/UX:** Features a custom modern aesthetic with rounded corners, a smooth color palette, responsive CSS, and a clean layout to ensure a calming user experience.

---

## 🛠️ Tech Stack

- **Frontend / Full-stack Framework:** [Streamlit](https://streamlit.io/)
- **Programming Language:** Python
- **Large Language Model (LLM):** `meta-llama/Llama-3.1-8B-Instruct`
- **LLM Integration:** `openai` Python SDK (routed to Hugging Face serverless endpoints)
- **Data Visualization:** `pandas`, `plotly`
- **Secrets Management:** Streamlit Secrets (`secrets.toml`)

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd "Health chatbot"
```

### 2. Install Dependencies
Make sure you have Python installed. Then, run:
```bash
pip install -r requirements.txt
```

### 3. Setup API Keys
You will need a Hugging Face Access Token to run the AI model. 
1. Create an account on [Hugging Face](https://huggingface.co/).
2. Generate an Access Token from your settings.
3. In the project directory, create a `.streamlit/secrets.toml` file and add your token:
```toml
HF_TOKEN = "your_hugging_face_token_here"
```

### 4. Run the Application
You can run the full-featured UI by executing:
```bash
streamlit run mental_health_chatbot_ui.py
```
Alternatively, if you want to test the basic terminal-style version, you can run `streamlit run mental_health_ai.py`.

---

## 🛡️ Disclaimer
This project is an AI companion meant for educational and supportive purposes. It is **not** a licensed therapist or a substitute for professional medical advice. If you or someone you know is in crisis, please seek immediate professional help.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).