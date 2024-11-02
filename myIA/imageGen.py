from openai import OpenAI
import os

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

    def ask_dall_e(self, prompt):
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
            return "Limite de taux dépassée, veuillez réessayer plus tard."
        except OpenAI.error.BadRequestError as e:
            return "Erreur dans la requête : " + str(e)
        except OpenAI.error.UnauthorizedError:
            return "Erreur d'authentification. Veuillez vérifier votre clé API."
