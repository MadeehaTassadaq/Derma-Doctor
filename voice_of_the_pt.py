from dotenv import load_dotenv
load_dotenv()
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#def record_audio(file_path,time_out,phrase_time_limit):
#     # Initialize the recognizer
#     recognizer = sr.Recognizer()
#     # Record audio
#     logging.info("starting recording ...")
    
#     with sr.Microphone() as source:
#         audio = recognizer.adjust_for_ambient_noise(source, duration=1)
#         audio_data = recognizer.listen(source, timeout=time_out, phrase_time_limit=phrase_time_limit)
#         audio=audio_data.get_wav_data(audio)
#         AudioSegment.from_wav(BytesIO(audio)).export(file_path, format="mp3",bitrate="128k")
#     logging.info(f"Audio saved to {file_path}")
    
#     audiopath=file_path
#     return audiopath

    
    

# audiopath= "voice_of_the-pt.mp3"
# record_audio(audiopath,3,60)
#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"

def transcribe_audio(audiopath):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        logging.info("Transcribing audio...")
        print(f"Audio file path: {audiopath}") # Debugging
        with open(audiopath, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=(os.path.basename(audiopath), audio_file.read()),
                model=stt_model,
                language="en"
            )
        return response.text
    except FileNotFoundError:
        logging.error(f"File not found: {audiopath}")
        return None
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return None
    
    
audiopath = "voice_of_the-pt.mp3"

# Transcribe the audio
transcription = transcribe_audio(audiopath)
print(transcription)