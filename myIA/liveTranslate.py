import requests
from myIA.s2t import speech_to_text
from myIA.t2s import text_to_speech
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Translate:
    def __init__(self, api_key):
        self.api_key = api_key

    def translate_text(self, text: str, target_lang: str) -> str:
        """Utilise l'API Google Translate via une requête HTTP pour traduire le texte.

        Args:
            text (str): Texte à traduire
            target_lang (str): Langue dans laquelle traduire le texte d'entrée

        Returns:
            str: Texte traduit
        """
        url = "https://translation.googleapis.com/language/translate/v2"

        params = {
            'q': text,
            'target': target_lang,
            'key': self.api_key
        }

        translations = []
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() 
            translation = response.json()['data']['translations'][0]['translatedText']
            translations.append(translation)
        except requests.exceptions.HTTPError as e:
            logging.warning(f"Erreur {response.status_code} lors de la traduction: {e}")
        except Exception as e:
            logging.warning(f"Erreur inattendue lors de la traduction: {e}")
        finally:
            pass

        return translation


def liveTranslate():

    api_key_file = 'api_key.config'
    if not os.path.exists(api_key_file):
        os.makedirs(os.path.dirname(api_key_file), exist_ok=True)
    
    with open(api_key_file, 'r') as file:
        for line in file:
            if line.startswith("GOOGLE_CLOUD_API_KEY"):
                api_key = line.split('=')[1].strip()
                break
    api_key = api_key


    langue_target = input("Dans quelle langue voulez-vous traduire le texte ? (ex: en pour anglais) : ").strip().lower()
    while True:
        texte = speech_to_text()
        if texte is None:
            print("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
            continue

        print("Texte capturé :", texte)
        texte_traduit = Translate(api_key=api_key).translate_text(texte, langue_target)
        if texte_traduit is not None:
            print("Traduction :", texte_traduit)
            text_to_speech(texte_traduit, lang=langue_target)
        else:
            print("Impossible de traduire le texte.")
        
        choix = input("Voulez-vous traduire un autre texte ? (oui/non) : ").strip().lower()
        if choix != 'oui':
            print("Fin de la traduction.")
            break

