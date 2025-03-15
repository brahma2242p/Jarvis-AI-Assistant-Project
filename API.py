import pyttsx3
import google.generativeai as genai
import speech_recognition as sr
import os

# Securely load API key
API_KEY ="AIzaSyDXRKib2L9cxVn4dF3wyOF2ZmeHoe76bak"  # Set this in your environment variables
if not API_KEY:
    raise ValueError("API key is missing! Set the GEMINI_API_KEY environment variable.")

try:
    # Configure Google Gemini AI
    genai.configure(api_key=API_KEY)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="hi",
    )
    chat_session = model.start_chat(history=[
        {"role": "user", "parts": ["hello"]},
        {"role": "model", "parts": ["Hello there! How can I help you today?"]}
    ])
except Exception as e:
    print(f"Error initializing AI model: {e}")
    exit(1)

# Initialize speech engine
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing text-to-speech engine: {e}")
    exit(1)

def recognize_speech_from_mic(duration=7):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        print("Adjusting for ambient noise... Please wait.")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for speech...")
            audio = recognizer.listen(source, timeout=duration)

        print("Recognizing speech...")
        transcription = recognizer.recognize_google(audio)
        print("You said:", transcription)

        # Get AI response
        try:
            response = chat_session.send_message(transcription)
            print("AI:", response.text)
        except Exception as e:
            print(f"Error in AI response generation: {e}")
            return

        # Speak response
        try:
            engine.stop()  # Stop previous speech if any
            engine.say(response.text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech output: {e}")
    
    except sr.WaitTimeoutError:
        print("Speech timeout: No speech detected.")
    except sr.RequestError as e:
        print(f"Speech recognition API unavailable: {e}")
    except sr.UnknownValueError:
        print("Could not understand the speech.")
    except Exception as e:
        print(f"Unexpected error during speech recognition: {e}")

if __name__ == " __main__ ":
    recognize_speech_from_mic()
