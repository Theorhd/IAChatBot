from openai import OpenAI
from myIA.imageGen import askDall_E
from myIA.vision import imageAnalyze
from myIA.t2s import chat_t2s
from myIA.s2t import liveConv
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

    messages = [
        {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses. La langue française est votre domaine de prédilection. Toutes les conversations que tu as doivent etre en français. Ton dommaine d'expertise est le développement, principalement web et logiciel. Tu connais a la perfection les langages de programmation comme Python, Java, C++, JavaScript, HTML, CSS, SQL, PHP, Ruby, Swift, Kotlin, etc. Tu es capable de répondre à des questions sur les frameworks et les bibliothèques les plus populaires. Tu as une connaissance approfondie des bases de données relationnelles et non relationnelles. Tu es capable de répondre à des questions sur les systèmes d'exploitation les plus populaires. Tu es capable de répondre à des questions sur les technologies de développement web et mobile. Tu es capable de répondre à des questions sur les méthodologies de développement logiciel. Tu es capable de répondre à des questions sur les outils de développement logiciel. Tu es capable de répondre à des questions sur les bonnes pratiques de développement logiciel. Tu es capable de répondre à des questions sur les principes de conception logicielle. Tu es capable de répondre à des questions sur les architectures logicielles. Tu es capable de répondre à des questions sur les tests logiciels. Tu es capable de répondre à des questions sur les déploiements logiciels. Tu es capable de répondre à des questions sur les environnements de développement intégrés. Tu es capable de répondre à des questions sur les systèmes de contrôle de version. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de code source. Tu es capable de répondre à des questions sur les systèmes de gestion de base de données. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Tu es capable de répondre à des questions sur les systèmes de gestion de configuration. Tu es capable de répondre à des questions sur les systèmes de gestion de serveur. Tu es capable de répondre à des questions sur les systèmes de gestion de réseau. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de qualité. Tu es capable de répondre à des questions sur les systèmes de gestion de version. Tu es capable de répondre à des questions sur les systèmes de gestion de workflow. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Ton nom est TheoGPT."}
    ]

    while True:
        user_input = input("Vous : ")

        if user_input.lower() == 'quit':
            print("Chatbot : Merci pour cette conversation. À bientôt !")
            break
        
        if user_input.startswith("--imageGen"):
            user_input = user_input.replace("--imageGen", "")
            dalle_response = askDall_E(user_input)
            print("Chatbot : Voici l'image générée : " + dalle_response)

        elif user_input.startswith("--imageAnalyze"):
            user_input = user_input.replace("--imageAnalyze", "")
            image_url = user_input.strip()
            imageAnalyze_response = imageAnalyze(image_url)
            print("Chatbot : ", imageAnalyze_response)
            
        elif user_input.startswith("--t2s"):
            user_input = user_input.replace("--t2s", "")
            chat_t2s(user_input)

        elif user_input.startswith("--liveConv"):
            liveConv()
            
        else:
            try:
                response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages + [
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

                messages.append({"role": "user", "content": user_input})
                bot_reply = response.choices[0].message.content
                messages.append({"role": "assistant", "content": bot_reply})
                print("Chatbot :", bot_reply)
                
                if len(messages) > 20:
                    messages = messages[-20:]
                
            except OpenAI.error.RateLimitError:
                print("Limite de taux dépassée, veuillez réessayer plus tard.")
                time.sleep(60)  
            except OpenAI.error.BadRequestError as e:
                print("Erreur dans la requête :", e)
            except Exception as e:
                print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    chatbot()