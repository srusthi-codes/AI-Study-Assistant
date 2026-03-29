import streamlit as st
import requests
import time

# Page config
st.set_page_config(page_title="AI Study Assistant", layout="wide")

# Custom UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .stButton button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Assistant 🚀")

# 🔑 ADD YOUR API KEY HERE
api_key = "sk_izJaToCxSn4ZVaSxw2xPAwjYU03fqXQifhHpd9vkSzg"

# 📄 File upload
uploaded_file = st.file_uploader("📄 Upload notes (txt file)", type=["txt"])

text_input = ""

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully!")

# ✍️ Manual input
user_input = st.text_area("✍️ Or enter your notes manually:", value=text_input, height=200)

# ⚠️ Input check
if user_input.strip() == "":
    st.warning("Please enter or upload notes first!")

# 🔘 Buttons
col1, col2, col3 = st.columns(3)

summary_btn = col1.button("📄 Summary")
points_btn = col2.button("🔑 Key Points")
quiz_btn = col3.button("❓ Quiz")

# 🔥 API function with retry (FINAL FIX)
def call_api(prompt):
    url = "https://api.oxlo.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-v3_2",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    for i in range(3):  # retry 3 times
        with st.spinner(f"Generating... (attempt {i+1}) ⏳"):
            response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        time.sleep(2)  # wait before retry

    return "⚠️ API is busy. Please try again in a few seconds."

# 🚀 Actions
if summary_btn and user_input.strip() != "":
    output = call_api(f"Summarize this text:\n{user_input}")
    st.subheader("📄 Summary")
    st.write(output)

if points_btn and user_input.strip() != "":
    output = call_api(f"Give key points from this text:\n{user_input}")
    st.subheader("🔑 Key Points")
    st.write(output)

if quiz_btn and user_input.strip() != "":
    output = call_api(f"Generate 3 quiz questions from this text:\n{user_input}")
    st.subheader("❓ Quiz Questions")
    st.write(output)