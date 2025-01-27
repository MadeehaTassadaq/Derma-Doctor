import os
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

# Function to encode an image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

# Route: Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        image_file = request.files["image"]
        
        # Save uploaded image temporarily
        
        image_path = os.path.join("uploads", image_file.filename)
        image_file.save(image_path)
        
        # Encode the image
        encoded_image = encode_image(image_path)
        
        # Call Groq API
        try:
            messages = [{
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
                messages=messages,
                model="llama-3.2-90b-vision-preview"
            )
            result = response.choices[0].message.content
        except Exception as e:
            result = f"Error: {e}"
        
        return render_template("index.html", result=result)
# Handle GET request
    return render_template("index.html", result=None)
    

# Run the app
if __name__ == "__main__":
    app.run(debug=True)