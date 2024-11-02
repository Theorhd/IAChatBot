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
        prompt = self.optimize_prompt(prompt)
        print("Prompt optimisé pour Dall-E :", prompt)
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
        return optimize_response.choices[0].message.content