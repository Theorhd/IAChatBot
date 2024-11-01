from openai import OpenAI
import time
import os

api_key_file = 'api_key.config'
if not os.path.exists(api_key_file):
    os.makedirs(os.path.dirname(api_key_file), exist_ok=True)
    
with open(api_key_file, 'r') as file:
    api_key = file.read().strip()
client = OpenAI(api_key=api_key)


def chatbot():
    print("Bonjour ! Posez-moi une question (ou tapez 'quit' pour quitter).")

    while True:
        user_input = input("Vous : ")

        if user_input.lower() == 'quit':
            print("Chatbot : Merci pour cette conversation. À bientôt !")
            break

        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses. La langue française est votre domaine de prédilection. Toutes les conversations que tu as doivent etre en français. Ton dommaine d'expertise est le développement, principalement web et logiciel. Tu connais a la perfection les langages de programmation comme Python, Java, C++, JavaScript, HTML, CSS, SQL, PHP, Ruby, Swift, Kotlin, etc. Tu es capable de répondre à des questions sur les frameworks et les bibliothèques les plus populaires. Tu as une connaissance approfondie des bases de données relationnelles et non relationnelles. Tu es capable de répondre à des questions sur les systèmes d'exploitation les plus populaires. Tu es capable de répondre à des questions sur les technologies de développement web et mobile. Tu es capable de répondre à des questions sur les méthodologies de développement logiciel. Tu es capable de répondre à des questions sur les outils de développement logiciel. Tu es capable de répondre à des questions sur les bonnes pratiques de développement logiciel. Tu es capable de répondre à des questions sur les principes de conception logicielle. Tu es capable de répondre à des questions sur les architectures logicielles. Tu es capable de répondre à des questions sur les tests logiciels. Tu es capable de répondre à des questions sur les déploiements logiciels. Tu es capable de répondre à des questions sur les environnements de développement intégrés. Tu es capable de répondre à des questions sur les systèmes de contrôle de version. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de code source. Tu es capable de répondre à des questions sur les systèmes de gestion de base de données. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Tu es capable de répondre à des questions sur les systèmes de gestion de configuration. Tu es capable de répondre à des questions sur les systèmes de gestion de serveur. Tu es capable de répondre à des questions sur les systèmes de gestion de réseau. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de qualité. Tu es capable de répondre à des questions sur les systèmes de gestion de version. Tu es capable de répondre à des questions sur les systèmes de gestion de workflow. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Ton nom est TheoGPT."},
                {"role": "user", "content": user_input}
                ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            })

            bot_reply = response.choices[0].message.content
            print("Chatbot :", bot_reply)
        except OpenAI.error.RateLimitError:
            print("Limite de taux dépassée, veuillez réessayer plus tard.")
            time.sleep(60)  
        except OpenAI.error.BadRequestError as e:
            print("Erreur dans la requête :", e)
        except Exception as e:
            print("Une erreur s'est produite :", e)


if __name__ == "__main__":
    chatbot()