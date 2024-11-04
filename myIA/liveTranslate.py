import requests
from myIA.s2t import SpeechToText
from myIA.t2s import TextToSpeech
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

class Translate:
    def __init__(self, api_key):
        self.api_key = api_key

    def translate_text(self, text: str, target_lang: str) -> str:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': text,
            'target': target_lang,
            'key': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()['data']['translations'][0]['translatedText']
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erreur {response.status_code} lors de la traduction: {e}")
            return None
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la traduction: {e}")
            return None
        finally:
            logging.info("Demande de traduction de texte.")

class LiveTranslate:
    @staticmethod
    def start():
        logging.info("Démarrage de la traduction vocale en temps réel.")
        api_key_file = 'api_key.config'
        if not os.path.exists(api_key_file):
            os.makedirs(os.path.dirname(api_key_file), exist_ok=True)

        with open(api_key_file, 'r') as file:
            for line in file:
                if line.startswith("GOOGLE_CLOUD_API_KEY"):
                    api_key = line.split('=')[1].strip()
                    break

        langue_target = input("Dans quelle langue voulez-vous traduire le texte ? (ex: en pour anglais) : ").strip().lower()
        logging.info(f"Langue cible de traduction : {langue_target}")
        while True:
            texte = SpeechToText().speech_to_text()
            if texte is None:
                print("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
                continue

            print("Texte capturé :", texte)
            logging.info(f"Texte capturé : {texte}")
            texte_traduit = Translate(api_key=api_key).translate_text(texte, langue_target)
            if texte_traduit is not None:
                print("Traduction :", texte_traduit)
                logging.info(f"Traduction : {texte_traduit}")
                TextToSpeech().text_to_speech(texte_traduit, lang=langue_target)
            else:
                print("Impossible de traduire le texte.")
                logging.error("Impossible de traduire le texte.")

            choix = input("Voulez-vous traduire un autre texte ? (oui/non) : ").strip().lower()
            if choix != 'oui':
                print("Fin de la traduction.")
                logging.info("Fin de la traduction.")
                break
