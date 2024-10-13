import google.generativeai as genai
import os
import re
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

history = [
    {"role": "user", "parts": ["Olá"]},
    {"role": "model", "parts": ["Prazer, o que gostaria de saber?"]}
]

historyExecute = [
    {"role": "user", "parts": ["Quando eu pedir o código eu quero somente o código pronto sem mais nem menos. Exemplo: código para desligar o PC, você vai me responder apenas shutdown /s /t 1, lembrando que tudo pelo terminal do Windows, não Linux"]},
    {"role": "model", "parts": ["Certo, qual código deseja saber?"]}
]

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    with sr.Microphone() as source:
        print("Diga algo ('sair' para sair) (execute para códigos):")
        audio = recognizer.listen(source)
        try:
            inpresp = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {inpresp}")

            if inpresp.lower() == "sair":
                break
            elif inpresp.lower() == "execute":
                speak("Qual código deseja?")
                audio = recognizer.listen(source)
                executeOrder = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {executeOrder}")

                historyExecute.append({"role": "user", "parts": [executeOrder]})
                response = model.generate_content(historyExecute)
                historyExecute.append({"role": "model", "parts": [response.text]})
                clean_response = re.sub(r'```(.*?)```', r'\1', response.text, flags=re.DOTALL)

                try:
                    print("Código executado foi:", clean_response)
                    os.system(clean_response)
                except Exception as e:
                    print("Ocorreu um erro:", e)
            else:
                try:
                    history.append({"role": "user", "parts": [inpresp]})
                    response = model.generate_content(history)
                    history.append({"role": "model", "parts": [response.text]})
                    print(response.text)
                    speak(response.text)
                except Exception as e:
                    print("Ocorreu um erro:", e)
        except sr.UnknownValueError:
            print("Não entendi o que você disse")
        except sr.RequestError as e:
            print(f"Erro ao solicitar resultados do Google Speech Recognition; {e}")
