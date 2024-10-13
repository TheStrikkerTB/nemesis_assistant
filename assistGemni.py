import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# This is the conversation history
history = [
    {"role": "user", "parts": ["Hello"]},
    {"role": "model", "parts": ["Great to meet you. What would you like to know?"]}
]

# Initial conversation history for executing code
historyExecute = [
    {"role": "user", "parts": ["When I ask for the code, I want only the ready-made code, nothing more, nothing less. For example, code to shut down the PC, you will respond with only shutdown /s /t 1, remembering that everything is for the Windows terminal, not Linux"]},
    {"role": "model", "parts": ["Sure, what code would you like to know?"]}
]

# Conversation loop
while True:
    inpresp = str(input("Type what you want \n('exit' to quit) (execute for codes)\n: "))
    if inpresp.lower() == "exit":
        break
    elif inpresp.lower() == "execute":
        executeOrder = input("What code would you like?")
        historyExecute.append({"role": "user", "parts": [executeOrder]})
        response = model.generate_content(historyExecute)
        historyExecute.append({"role": "model", "parts": [response.text]})

        # Remove markdown formatting
        clean_response = re.sub(r'```(.*?)```', r'\1', response.text, flags=re.DOTALL)

        try:
            print("executed code was:", clean_response)
            os.system(clean_response)
        except Exception as e:
            print("An error occurred:", e)
    else:
        try:
            history.append({"role": "user", "parts": [inpresp]})
            response = model.generate_content(history)
            history.append({"role": "model", "parts": [response.text]})
            print(response.text)
        except Exception as e:
            print("An error occurred:", e)
