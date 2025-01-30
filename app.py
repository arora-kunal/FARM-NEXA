import streamlit as st
import openai
from moviepy.editor import AudioFileClip
import tempfile
import os

# Set up your OpenAI API key
openai.api_key = "Your OpenAI API Key"

# Multilingual Description
description_english = "Welcome to the AI Agricultural Assistant!\n" \
                      "This app is here to offer valuable support and guidance to farmers around the world. " \
                      "It can help with everything from crop diseases and weed control to plantation and other farming queries, " \
                      "all while focusing on improving productivity and promoting sustainable practices. " \
                      "Feel free to ask any farming-related questions, and the assistant will do its best to provide helpful advice and information."

description_hindi = "कृषि सहायक में आपका स्वागत है!\n" \
                    "यह ऐप दुनिया भर के किसानों को समर्थन और मार्गदर्शन प्रदान करने के लिए है। " \
                    "यह किसानों को फसल के रोगों और खरपतवार नियंत्रण से लेकर बागवानी और अन्य खेती संबंधित सवालों में मदद कर सकता है, " \
                    "साथ ही उत्पादकता को बढ़ाने और सतत अभिवृद्धि को प्रोत्साहित करने पर ध्यान केंद्रित करता है। " \
                    "खेती से संबंधित किसी भी प्रश्न को पूछने के लिए स्वतंत्र महसूस करें, और सहायक सलाह और जानकारी प्रदान करने के लिए अपनी पूरी कोशिश करेगा।"

description_multilingual = f"{description_english}\n\n{description_hindi}"

# Instruction Message
instruction_message = {
    "role": "system",
    "content": "You are only a farming and agricultural themed assistant bot. Do not answer any question about any place or any other thing except farming and agriculture-themed questions. If a user asks queries other than farming and agriculture theme, then deny in a polite manner."
}

messages = [instruction_message]

# Streamlit app layout
st.title("🌱 AI Agricultural Assistant")
st.write(description_multilingual)

def get_assistant_response(messages, temperature=0.8):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"]

def text_interaction(user_input):
    messages.append({"role": "user", "content": user_input})
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
    return response

def audio_interaction(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
        audio_clip = AudioFileClip(audio_file.name)
        audio_clip.write_audiofile(tmp_mp3.name)
        
    with open(tmp_mp3.name, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file).text
        messages.append({"role": "user", "content": transcript})
        response = get_assistant_response(messages)
        messages.append({"role": "assistant", "content": response})
    os.remove(tmp_mp3.name)  # Cleanup temp file
    return transcript, response

# Text input handling
st.write("## Ask Your Farming Question:")
user_text = st.text_input("Enter your question here:")

if user_text:
    with st.spinner("Fetching response..."):
        response_text = text_interaction(user_text)
    st.write("### Assistant's Response:")
    st.write(response_text)

# Audio file handling
st.write("## Or Upload an Audio Question:")
uploaded_file = st.file_uploader("Upload a .ogg audio file", type="ogg")

if uploaded_file:
    with st.spinner("Processing audio..."):
        transcript, response_text = audio_interaction(uploaded_file)
    st.write("### Transcription of Your Question:")
    st.write(transcript)
    st.write("### Assistant's Response:")
    st.write(response_text)