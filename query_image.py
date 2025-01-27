#Step1: Setup GROQ API key
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#Step2: Convert image to required format
import base64
# Function to encode an image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image
def analyze_image(query, model, encoded_image):
    # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
        
