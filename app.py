import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile

# Initialize translator
translator = Translator()

# Streamlit App
st.title("Voice-to-Voice Language Translator")

# Dropdowns for language selection
st.sidebar.header("Select Languages")
source_lang = st.sidebar.selectbox(
    "Source Language", ["English", "Hindi", "Spanish", "German", "Korean"]
)
target_lang = st.sidebar.selectbox(
    "Target Language", ["English", "Hindi", "Spanish", "German", "Korean"]
)

# Language codes for Google Translator
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "German": "de",
    "Korean": "ko",
}

source_lang_code = language_codes[source_lang]
target_lang_code = language_codes[target_lang]

# Capture and translate voice
st.header("Translate Your Speech")
if st.button("Record and Translate"):
    try:
        # Record the user's voice
        st.info("Listening... Please speak into your microphone.")
        recog = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = recog.listen(source)

        # Recognize speech using Google Speech Recognition
        st.success("Processing your speech...")
        input_text = recog.recognize_google(audio_data, language=source_lang_code)
        st.write(f"Recognized Text: {input_text}")

        # Translate the recognized text
        translated = translator.translate(
            input_text, src=source_lang_code, dest=target_lang_code
        )
        translated_text = translated.text
        st.write(f"Translated Text: {translated_text}")

        # Convert translated text to speech
        tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio_file.name)
        st.audio(temp_audio_file.name, format="audio/mp3")

    except sr.UnknownValueError:
        st.error("Sorry, I could not understand your speech. Please try again.")
    except sr.RequestError as e:
        st.error(f"Could not request results from the speech recognition service; {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# App instructions
st.sidebar.subheader("How to Use")
st.sidebar.text(
    """
1. Select source and target languages.
2. Click "Record and Translate."
3. Speak into your microphone.
4. View the recognized and translated text.
5. Listen to the translated speech output.
"""
)
