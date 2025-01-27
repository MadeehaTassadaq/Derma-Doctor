import os
from gtts import gTTS
import subprocess
import platform
GROQ_API_KEY=os.environ.get('GROQ_API_KEY')
def speech_to_text(input_text, output_file):
    tts = gTTS(text=input_text, lang='en')
    tts.save(output_file)
    return output_file
#speech_to_text("Hello, I am the Doctor", "gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import os
from elevenlabs.client import ElevenLabs

# Set up ElevenLabs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")

# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     # Initialize the ElevenLabs client
#     client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
#     # Generate audio from text
#     audio = client.generate(
#         text=input_text,
#         voice="Aria",  # Choose a voice
#         model="eleven_turbo_v2"  # Choose a model
#     )
    
#     # Save the audio to a file
#     with open(output_filepath, "wb") as f:
#         for chunk in audio:
#             f.write(chunk)  # Write the audio data to the file
    
#     return f"Audio saved to {output_filepath}"
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
     
    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
import platform
import subprocess
import os
from elevenlabs.client import ElevenLabs

# Set up ElevenLabs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    # Initialize the ElevenLabs client
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # Generate audio from text
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    
    # Save the audio to a file
    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    # Play the audio file
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Use ffplay (from FFmpeg) to play .mp3 files
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath], check=True)
        elif os_name == "Linux":  # Linux
            # Use mpg123 to play .mp3 files
            subprocess.run(['mpg123', output_filepath], check=True)
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
    
    return f"Audio saved to {output_filepath}"


# Example usage
input_text = "Hello, I am the Doctor"
output_filepath = "elevenlabs_testing.mp3"
#result = text_to_speech_with_elevenlabs(input_text=input_text, output_filepath=output_filepath)
#print(result)

