from openai import OpenAI
from myIA.help import Help
from myIA.imageGen import ImageGen
from myIA.vision import ImageAnalyzer
from myIA.t2s import TextToSpeech 
from myIA.s2t import LiveConv
from myIA.liveTranslate import LiveTranslate
import time
import os

api_key_file = 'api_key.config'
if not os.path.exists(api_key_file):
    os.makedirs(os.path.dirname(api_key_file), exist_ok=True)

with open(api_key_file, 'r') as file:
    for line in file:
        if line.startswith("OPENAI_API_KEY"):
            api_key = line.split('=')[1].strip()
            break

client = OpenAI(api_key=api_key)

class Chatbot:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses. La langue française est votre domaine de prédilection. ..."}
        ]
        self.tts = TextToSpeech()
        self.image_analyzer = ImageAnalyzer() 
    
    def start(self):
        print("Bonjour ! Posez-moi une question (ou tapez 'quit' pour quitter).")
        while True:
            user_input = input("Vous : ")

            if user_input.lower() == 'quit':
                print("Chatbot : Merci pour cette conversation. À bientôt !")
                break

            elif user_input.startswith('--help'):
                Help().display()

            elif user_input.startswith("--imageGen"):
                user_input = user_input.replace("--imageGen", "").strip()
                dalle_response = ImageGen().ask_dall_e(user_input)
                print("Chatbot : Voici l'image générée : " + dalle_response)

            elif user_input.startswith("--imageAnalyze"):
                user_input = user_input.replace("--imageAnalyze", "").strip()
                image_url = user_input
                image_analyze_response = self.image_analyzer.image_analyze(image_url) 
                print("Chatbot : ", image_analyze_response)

            elif user_input.startswith("--t2s"):
                user_input = user_input.replace("--t2s", "").strip()
                self.tts.chat_t2s(user_input) 

            elif user_input.startswith("--liveConv"):
                LiveConv().start()

            elif user_input.startswith("--liveTranslate"):
                LiveTranslate().start()

            else:
                self.get_response(user_input)

    def get_response(self, user_input):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.messages + [{"role": "user", "content": user_input}],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                })

            self.messages.append({"role": "user", "content": user_input})
            bot_reply = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": bot_reply})
            print("Chatbot :", bot_reply)

            if len(self.messages) > 20:
                self.messages = self.messages[-20:]

        except OpenAI.error.RateLimitError:
            print("Limite de taux dépassée, veuillez réessayer plus tard.")
            time.sleep(60)
        except OpenAI.error.BadRequestError as e:
            print("Erreur dans la requête :", e)
        except Exception as e:
            print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    Chatbot().start()
