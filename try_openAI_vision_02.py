
from dotenv import load_dotenv
import os
import base64
import requests
import prompt_01
import mimetypes
from PIL import Image
from pillow_heif import register_heif_opener
import logging


logging.basicConfig(level=logging.DEBUG)

# need to register HEIF opener once at the start for opening HEIC images
register_heif_opener()

load_dotenv()
api_key = os.getenv("api_key")


# Function to encode the image
# Base64 is an encoding method that converts binary data into a text string.
# OpenAI API can only passed a string 
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# 1.API Request
# when the user input == image
def ask_openAI_category_image(input_img):

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
 
  # In the case of image passed
  payload = {
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": prompt_01.prompt_system},
      {
        "role": "user",
        "content": [{
            "type": "text",
            "text": "Which case of category does the following content belong to?"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{input_img}"}}]
      }
    ],
    "max_tokens": 300
  }
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  response_content = response.json()['choices'][0]['message']['content'] # only 'content' will be returned
  logging.debug("ask_openAI_category_image() API response status code: %s", response.status_code)
  logging.debug("ask_openAI_category_image() API response content: %s", response_content)
  return response_content


# 1.API Request
# when the user input == text
def ask_openAI_category_text(input_text):

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  # In the case of text passed
  payload = {
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": prompt_01.prompt_system},
      {
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"Input content is {input_text}. Which case of category does the content belong to?"},
          ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  return response.json()['choices'][0]['message']['content'] # only 'content' will be returned 


# 1.API Request                
def determine_and_ask_openAI(user_input):
    if isinstance(user_input, str):
        # Check if the input string is a valid file path
        if os.path.isfile(user_input):
            logging.debug("input data is an image")
            mime_type, _ = mimetypes.guess_type(user_input) # returned value is tuple e.g. ('image/jpeg', None). The second returned value is not used. 
            if mime_type and mime_type.startswith('image'):
                # It's an image file
                # Check the image-format
                if user_input.lower().endswith(".heic"):
                    temp_img = Image.open(user_input)
                    logging.debug("input data was a HEIC data")
                    # Change the file extension to .jpeg
                    file_root, _ = os.path.splitext(os.path.basename(user_input)) # returned value example: IMG_9989 .HEIC
                    new_jpeg_image = os.path.join("Project/img/jpg", file_root + ".jpeg")
                    logging.debug("filename extension changed to jpeg")

                    temp_img.save(new_jpeg_image, "JPEG")
                    logging.debug(f"image saved at: {new_jpeg_image}")
                    
                    base64_image = encode_image(new_jpeg_image)
                return ask_openAI_category_image(base64_image)

            else:
                # It's a text string, not a file path
                return ask_openAI_category_text(user_input)
        else:
            # It's a text string
            return ask_openAI_category_text(user_input)
    else:
        return "Invalid input type. Please provide a string representing either text or an image file path."

# 2. API Request in the case of "Case 01"
def second_API_request_case_01(user_input):
   
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  # In the case of text passed
  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"please return to the user input{user_input}a positiv feedback. The feedback should be encouraging and praising"},
          ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  #logging.debug("second_API_request_case_01:", response.json())['choices'][0]['message']['content'] # Man bekommt logging error

  return response.json()['choices'][0]['message']['content']


    
# 2. API Request in the case of "Case 02"
# if user_input is text
def case2_text(input_text): # Target: you only want to get the information about "item, category, cost" back in form of dictionary

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  # In the case of text passed
  payload = {
    "model": "gpt-4-0613",
    "messages": [
      {
        "role": "user",
        "content": f"The input content is related to money expenses. Please just return the expense items, categories and their costs in the following key-value form: {{\"expense_item\": expense_item, \"category\": category, \"cost\": cost}}"
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  return response.json()['choices'][0]['message']['content']

# 2. API Request in the case of "Case 02"
# if user_input is image
def case2_image(input_img):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
 
    # In the case of image passed
    payload = {
      "model": "gpt-4o",
      "messages": [
              {
        "role": "user",
        "content": [{
            "type": "text",
            "text": "The input content is related to the money expenses. Please just return 'items','categories' and 'costs' in form of dictionary."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{input_img}"}}]
      }
      ],
      "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #print("case2_image:", response.json())
    logging.debug("case2_image:", response.json()['choices'][0]['message']['content'])
    return response.json()['choices'][0]['message']['content']

# 2.API Request in the case of Case 02
def second_API_request_case_02(user_input):
    if isinstance(user_input, str):
        # Check if the input string is a valid file path
        if os.path.isfile(user_input):
          
            mime_type, _ = mimetypes.guess_type(user_input) 
            if mime_type and mime_type.startswith('image'):
                # It's an image file
                # Check the image-format
                if user_input.lower().endswith(".heic"):
                    temp_img = Image.open(user_input)

                    # Change the file extension to .jpeg
                    file_root, _ = os.path.splitext(os.path.basename(user_input)) 
                    new_jpeg_image = os.path.join("Project/img/jpg", file_root + ".jpeg")
                    
                    base64_image = encode_image(new_jpeg_image)
                return case2_image(base64_image)

            else:
                # It's a text string, not a file path
                return case2_text(user_input)
        else:
            # It's a text string
            return case2_text(user_input)
    else:
        return "Invalid input type. Please provide a string representing either text or an image file path."