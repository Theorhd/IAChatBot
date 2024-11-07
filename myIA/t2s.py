import gtts
from playsound import playsound
import os
import time
import tempfile
from openai import OpenAI
from mutagen.mp3 import MP3
import logging
import threading

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

class TextToSpeech:
    def __init__(self):
        self.api_key = self.load_api_key()
        logging.info("Initialisation de la synthèse vocale.")

    def load_api_key(self):
        parent = os.path.dirname(os.path.dirname(__file__))
        api_key_file = os.path.join(parent, 'api_key.config')
        
        with open(api_key_file, 'r') as file:
            for line in file:
                if line.startswith("OPENAI_API_KEY"):
                    logging.info("Clé API OpenAI trouvée.")
                    return line.split('=')[1].strip()
        logging.error("Clé API OpenAI non trouvée.")
        return None

    def text_to_speech(self, text, lang='fr'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            mp3_filename = temp_file.name

        tts = gtts.gTTS(text, lang=lang)
        tts.save(mp3_filename)
        logging.info("Fichier audio temporaire créé.")
        try:
            audio = MP3(mp3_filename)
            duration = audio.info.length
            playsound(mp3_filename)
            logging.info("Lecture du fichier audio.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier audio : {e}")
            logging.error(f"Erreur lors de la lecture du fichier audio : {e}")
        finally:
            time.sleep(duration)
            os.remove(mp3_filename)
            logging.info("Fichier audio temporaire supprimé.")

    def start_text_to_speech_thread(self, text, lang='fr'):
        thread = threading.Thread(target=self.text_to_speech, args=(text, lang))
        thread.start()

    def chat_t2s(self, user_input):
        messages = [
            {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses... (contenu ici)"}
        ]

        client = OpenAI(api_key=self.api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages + [{"role": "user", "content": user_input}],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "text"}
            )

            bot_reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": bot_reply})
            print("Chatbot :", bot_reply)
            self.text_to_speech(bot_reply)

            if len(messages) > 20:
                messages = messages[-20:]

        except OpenAI.error.RateLimitError:
            logging.error("Limite de taux dépassée, veuillez réessayer plus tard.")
            print("Limite de taux dépassée, veuillez réessayer plus tard.")
            time.sleep(60)
        except OpenAI.error.BadRequestError as e:
            logging.error("Erreur dans la requête : " + str(e))
            print("Erreur dans la requête :", e)
        except Exception as e:
            logging.error("Une erreur s'est produite : " + str(e))
            print("Une erreur s'est produite :", e)
        finally:
            logging.info("Demande de synthèse vocale.")