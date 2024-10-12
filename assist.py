import os
from dotenv import load_dotenv
import requests

import google.generativeai as genai
import os

# Carrega as variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)

