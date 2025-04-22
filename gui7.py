import streamlit as st
import os
import webbrowser
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import re
import random
from streamlit_option_menu import option_menu
from requests_html import HTMLSession
import base64

# --- Text-to-Speech ---
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# --- Speech-to-Text ---
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎙️ Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        st.success("✅ Processing...")
        return recognizer.recognize_google(audio)
    except:
        return None


# --- Assistant Logic ---
def assistant_action(data):
    user_data = data.lower()
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "I'm reading a book on anti-gravity. It's impossible to put down!"
    ]

    if "what is your name" in user_data:
        reply = "My name is Alice."
    elif "who are you" in user_data:
        reply = "I am your cheerful virtual assistant!"
    elif "hello" in user_data or "hi" in user_data:
        reply = "Hello there! 😊 How can I assist you today?"
    elif "good morning" in user_data:
        reply = "Good morning! Wishing you a productive day ahead!"
    elif "good afternoon" in user_data:
        reply = "Good afternoon! What can I help you with?"
    elif "shutdown" in user_data:
        reply = "Alright, shutting down. See you soon!"
    elif "play music" in user_data:
        webbrowser.open("https://spotify.com")
        reply = "Spotify is all set! Enjoy your tunes 🎶"
    elif "youtube" in user_data:
        webbrowser.open("https://youtube.com")
        reply = "YouTube is ready for you!"
    elif "chatgpt" in user_data:
        webbrowser.open("http://chatgpt.com")
        reply = "Opening ChatGPT for you!"
    elif "google" in user_data:
        webbrowser.open("https://google.com")
        reply = "Google is at your service!"
    elif "time now" in user_data:
        now = datetime.now()
        reply = f"The current time is {now.strftime('%H:%M:%S')}"
    elif "joke" in user_data:
        reply = random.choice(jokes)
    else:
        reply = "Hmm, I didn't catch that. Can you please repeat?"

    text_to_speech(reply)
    return reply

# --- Streamlit Setup ---
st.set_page_config(page_title="✨ Virtual Assistant ✨", layout="wide")
st.sidebar.image("https://media.giphy.com/media/3o7TKxohkk8v3dPsAw/giphy.gif", width=150)
st.sidebar.markdown(f"🕒 **{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}**")

# --- Menu ---
menu = ["Home", "Assistance", "About"]
with st.sidebar:
    choice = option_menu("Categories", menu, icons=["house", "mic", "info-circle"], menu_icon="cast", default_index=0)

# --- Chat History ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Pages ---
if choice == "Home":
    st.title("🤖 Welcome to Alice - Your Virtual Assistant")
    st.markdown("""
        ## 👋 Hello There!
        Meet **Alice**, your always-ready AI assistant. Ask her anything!

        ### 🧠 Features:
        - Speech & Text commands
        - Weather forecast with icons
        - Web browsing assistant
        - Jokes & fun responses

        👉 Head to the **Assistance** tab to start talking with Alice!
    """)

elif choice == "Assistance":
    st.title("🧠 Talk to Alice")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍️ Type a message")
        user_input = st.text_input("You:", placeholder="Type here and press enter...")
        if st.button("Send") and user_input:
            response = assistant_action(user_input)
            st.session_state.history.append((user_input, response))

    with col2:
        st.subheader("🎤 Speak to Alice")
        if st.button("Speak Now"):
            spoken_text = speech_to_text()
            if spoken_text:
                st.success(f"You said: {spoken_text}")
                response = assistant_action(spoken_text)
                st.session_state.history.append((spoken_text, response))
            else:
                st.warning("Could not understand your speech. Try again!")

    st.divider()
    st.subheader("📝 Conversation History")
    for user, bot in st.session_state.history:
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Alice:** {bot}")

elif choice == "About":
    st.title("📘 About This App")
    st.markdown("""
        **Virtual Assistant Alice** is a fun, interactive AI helper built using:
        - 🐍 Python
        - 🎙 Speech Recognition
        - 🔊 Text-to-Speech
        - 🌐 Streamlit for Web UI

        Created with ❤️ by pepakayala. Alice is designed to make your digital tasks easier & more enjoyable!
    """)

    st.subheader("🔗 Useful Links")
    st.markdown("[🌍 Google](https://google.com)")
    st.markdown("[🎵 Spotify](https://spotify.com)")
    st.markdown("[📺 YouTube](https://youtube.com)")

