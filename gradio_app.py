import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()
from query_image import encode_image, analyze_image
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from voice_of_the_pt import transcribe_audio

prompt="""
Act a  a healthcare professional. If A patient has come to you with a 
medical concern and ask a query along with an image ask query regarding her 
medical condition .You should act in the 
best interest of the patient and provide the best possible advice tailor 
according to her medical condition specifically. 

"""
def process_inputs(audio_file, image_file):
    # Debugging: Print the audio file path and check if the file exists
    print(f"Audio file path: {audio_file}")
    if not os.path.exists(audio_file):
        return "Error: Audio file not found.", "Please try again.", None

    # Transcribe audio
    speech_of_the_pt = transcribe_audio(audiopath=audio_file)
    if speech_of_the_pt is None:
        return "Error: Could not transcribe audio.", "Please try again.", None
    print(f"Transcribed Text: {speech_of_the_pt}")  # Debugging

    # Handle image file
    if image_file:
        encoded_image = encode_image(image_file)
        print(f"Image Encoded Successfully: {encoded_image is not None}")  # Debugging
        doctor_response = analyze_image(query=prompt+speech_of_the_pt, model="llama-3.2-90b-vision-preview", encoded_image=encoded_image)
    else:
        doctor_response = "If no image file is provided, only the audio file is processed."
    
    print(f"Doctor's Response: {doctor_response}")  # Debugging

    # Convert doctor's response to speech
    output_filepath = os.path.abspath("final_audio.mp3")
    print(f"Output file path: {output_filepath}")  # Debugging
    doctor_voice = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=output_filepath)
    print(f"Doctor's Voice File: {doctor_voice}")  # Debugging

    # Verify the audio file was created
    if os.path.exists(output_filepath):
        print("Audio file created successfully.")
    else:
        print("Error: Audio file not created.")

    return audio_path, doctor_response, doctor_voice

interface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final_audio.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)
interface.launch(server_name="0.0.0.0", server_port=7860,share=True, debug=True)