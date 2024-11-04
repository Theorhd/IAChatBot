from openai import OpenAI
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

class ImageAnalyzer:
    parent = os.path.dirname(os.path.dirname(__file__))
    api_key_file = os.path.join(parent, 'api_key.config')
    with open(api_key_file, 'r') as file:
        for line in file:
            if line.startswith("OPENAI_API_KEY"):
                api_key = line.split('=')[1].strip()
                break

    def __init__(self):
        self.client = OpenAI(api_key=self.api_key)
        logging.info("Initialisation de l'IA d'analyse d'images.")

    def image_analyze(self, image_url):
        try:
            imageAnalyze_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Qu'est-ce qu'il y a sur cette image ?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
        except Exception as e:
            logging.error("Erreur inattendue lors de l'analyse d'image : " + str(e))
            return str(e)
        finally:
            logging.info("Demande d'analyse d'image.")
            return imageAnalyze_response.choices[0].message.content
