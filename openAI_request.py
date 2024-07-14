from dotenv import load_dotenv
import os
import base64
import requests


# convert Heic into Jpg necessary: https://convertio.co/de/download/d522cc2edda5b67f8492297daa2f64e516b06b/

load_dotenv()
api_key = os.getenv("api_key")


# Function to encode the image
# Base64 ist ein Kodierungsverfahren, das binäre Daten in einen Textstring umwandelt.
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "Project/img/jpg/IMG_9991.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [{
          "type": "text",
          "text": "Was steht auf dem Bild? "},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])