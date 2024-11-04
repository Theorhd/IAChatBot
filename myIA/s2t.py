import speech_recognition as sr
from myIA.t2s import TextToSpeech
from myIA.weather import Weather
import os
import logging

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chemin_log = os.path.join(parent, "logs", "theogpt.log")
if not os.path.exists(os.path.dirname(chemin_log)):
    os.makedirs(os.path.dirname(chemin_log), exist_ok=True)
logging.basicConfig(
    filename=(chemin_log),
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    datefmt="%d/%m/%Y - %H:%M:%S",
    encoding='utf-8'
)

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1
        logging.info("Initialisation de la reconnaissance vocale.")

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Parlez maintenant...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                print("Vous avez dit : " + text)
                logging.info("Reconnaissance vocale : " + text)
                return text
            except sr.UnknownValueError:
                logging.error("Speech Recognition n'a pas pu comprendre l'audio.")
                return None
            except sr.RequestError as e:
                logging.error("Erreur avec le service Google Speech Recognition ; {0}".format(e))
                print("Erreur avec le service Google Speech Recognition ; {0}".format(e))

class LiveConv:
    @staticmethod
    def start():
        speech_to_text = SpeechToText()
        tts = TextToSpeech() 
        print("Début de la conversation. Dites 'quitter' pour terminer la conversation.")
        logging.info("Démarrage de la conversation vocale en continu.")
        while True:
            text = speech_to_text.speech_to_text()
            if text is None:
                print("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
                logging.warning("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
                continue
            elif text.lower() == 'quitter':
                print("Fin de la conversation.")
                logging.info("Fin de la conversation.")
                break
            
            elif Weather().user_askMeteo(text):
                city = Weather().get_city_in_user_input(text)
                if city:
                    city_insee = Weather().get_insee(city)
                    response = Weather().display_weather(city_insee)
                    tts.text_to_speech(response, lang="fr")
                else:
                    print("Chatbot : Je ne connais pas cette ville.")
            else:
                tts.chat_t2s(text)