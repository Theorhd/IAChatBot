from openai import OpenAI
import os

api_key_file = 'api_key.config'

current = os.path.dirname(__file__)
parent = os.path.dirname(current)
api_key_file = os.path.join(parent, api_key_file)

with open(api_key_file, 'r') as file:
    api_key = file.read().strip()
    
client = OpenAI(api_key=api_key)

def askDall_E(prompt):
    try:
        DallE_response = client.images.generate(
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