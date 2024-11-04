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

class ImageGen:
    def __init__(self):
        api_key_file = 'api_key.config'
        current = os.path.dirname(__file__)
        parent = os.path.dirname(current)
        api_key_file = os.path.join(parent, api_key_file)

        with open(api_key_file, 'r') as file:
            for line in file:
                if line.startswith("OPENAI_API_KEY"):
                    api_key = line.split('=')[1].strip()
                    break
                
        self.client = OpenAI(api_key=api_key)
        logging.info("Initialisation de l'IA de génération d'images.")

    def ask_dall_e(self, prompt):
        prompt = self.optimize_prompt(prompt)
        try:
            DallE_response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return DallE_response.data[0].url
        except Exception as e:
            return str(e)
        except OpenAI.error.RateLimitError:
            logging.error("Limite de taux dépassée, veuillez réessayer plus tard.")
            return "Limite de taux dépassée, veuillez réessayer plus tard."
        except OpenAI.error.BadRequestError as e:
            logging.error("Erreur dans la requête : " + str(e))
            return "Erreur dans la requête : " + str(e)
        except OpenAI.error.UnauthorizedError:
            logging.error("Erreur d'authentification. Veuillez vérifier votre clé API.")
            return "Erreur d'authentification. Veuillez vérifier votre clé API."
        finally:
            logging.info("Demande de génération d'image Dall-E.")
        
    def optimize_prompt(self, prompt):
        optimize_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Crée un prompt optimisé pour l'ia génératrice Dall-E, le prompt doit etre en anglais et bien décrire l'image souhaité, à partir du prompt suivant : " + prompt}],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        logging.info("Optimisation du prompt pour l'IA Dall-E.")
        return optimize_response.choices[0].message.content