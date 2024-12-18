from openai import OpenAI
from myIA.help import Help
from myIA.imageGen import ImageGen
from myIA.vision import ImageAnalyzer
from myIA.t2s import TextToSpeech 
from myIA.s2t import LiveConv
from myIA.liveTranslate import LiveTranslate
from myIA.memory import Memory
from myIA.weather import Weather
from login.login import UserManager
import time
import os
import sys
import itertools
import threading
import json
from rich.console import Console
from rich.markdown import Markdown

api_key_file = 'api_key.config'
if not os.path.exists(api_key_file):
    os.makedirs(os.path.dirname(api_key_file), exist_ok=True)

with open(api_key_file, 'r') as file:
    for line in file:
        if line.startswith("OPENAI_API_KEY"):
            api_key = line.split('=')[1].strip()
            break
          
client = OpenAI(api_key=api_key)

class Chatbot:
    def __init__(self):
        self.memory = Memory()
        self.messages = self.memory.get("messages") or [
            {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses. La langue française est votre domaine de prédilection. Toutes les conversations que tu as doivent etre en français. Ton dommaine d'expertise est le développement, principalement web et logiciel. Tu connais a la perfection les langages de programmation comme Python, Java, C++, JavaScript, HTML, CSS, SQL, PHP, Ruby, Swift, Kotlin, etc. Tu es capable de répondre à des questions sur les frameworks et les bibliothèques les plus populaires. Tu as une connaissance approfondie des bases de données relationnelles et non relationnelles. Tu es capable de répondre à des questions sur les systèmes d'exploitation les plus populaires. Tu es capable de répondre à des questions sur les technologies de développement web et mobile. Tu es capable de répondre à des questions sur les méthodologies de développement logiciel. Tu es capable de répondre à des questions sur les outils de développement logiciel. Tu es capable de répondre à des questions sur les bonnes pratiques de développement logiciel. Tu es capable de répondre à des questions sur les principes de conception logicielle. Tu es capable de répondre à des questions sur les architectures logicielles. Tu es capable de répondre à des questions sur les tests logiciels. Tu es capable de répondre à des questions sur les déploiements logiciels. Tu es capable de répondre à des questions sur les environnements de développement intégrés. Tu es capable de répondre à des questions sur les systèmes de contrôle de version. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de code source. Tu es capable de répondre à des questions sur les systèmes de gestion de base de données. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Tu es capable de répondre à des questions sur les systèmes de gestion de configuration. Tu es capable de répondre à des questions sur les systèmes de gestion de serveur. Tu es capable de répondre à des questions sur les systèmes de gestion de réseau. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de qualité. Tu es capable de répondre à des questions sur les systèmes de gestion de version. Tu es capable de répondre à des questions sur les systèmes de gestion de workflow. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Toutes tes réponses doivent correspondre en terme de syntaxe a celle des fichiers .md (Markdown). Ton nom est TheoGPT."}
        ]
        self.tts = TextToSpeech()
        self.image_analyzer = ImageAnalyzer()
        self.weather = Weather()
        self.user_manager = UserManager()
        self.console = Console()
        self.stop_loading_event = threading.Event()

    def add_message(self, role, content):
        """Ajoute un message et le sauvegarde dans la mémoire JSON"""
        if role not in ["user", "assistant", "system"]:
            print("Le rôle doit être 'user', 'assistant' ou 'system'.")
            return None
        self.messages.append({"role": role, "content": content})
        self.memory.add("messages", self.messages)
        print(f"L'information : '{content}' a été ajouté avec succès. Avce le rôle : '{role}'.")

    def load_session(self, session_name):
        """Charge une session sauvegardée dans la mémoire JSON"""
        session_path = os.path.join('sessions', f"{session_name}.json")
        if os.path.exists(session_path):
            with open(session_path, 'r') as file:
                self.messages = self.memory.get("messages") + json.load(file)
                self.memory.load_json_in_conversation(session_path)
                print(f"""
Session '{session_name}' chargée avec succès.
                      """)
                self.memory.display_session_content(session_name)
        else:
            print(f"Session '{session_name}' non trouvée.")

    def start(self):
        self.user_manager.connection_menu()
        print("Bonjour ! Posez-moi une question (ou tapez 'quit' pour quitter).")
        if (self.memory.display_sessions_history()):
            print('')
            print(self.memory.display_sessions_history())
            print("Pour charger une session, tapez '--loadSession nom_de_la_session'.")
            print('')
        while True:
            user_input = input("Vous : ")

            if user_input.lower() == 'quit':
                print("Chatbot : Merci pour cette conversation. À bientôt !")
                break

            elif user_input.startswith('--help'):
                Help().display()

            elif user_input.startswith("--imageGen"):
                user_input = user_input.replace("--imageGen", "").strip()
                dalle_response = ImageGen().ask_dall_e(user_input)
                print("Chatbot : Voici l'image générée : " + dalle_response)

            elif user_input.startswith("--imageAnalyze"):
                user_input = user_input.replace("--imageAnalyze", "").strip()
                image_url = user_input
                image_analyze_response = self.image_analyzer.image_analyze(image_url) 
                print("Chatbot : ", image_analyze_response)

            elif user_input.startswith("--t2s"):
                user_input = user_input.replace("--t2s", "").strip()
                self.tts.chat_t2s(user_input) 

            elif user_input.startswith("--liveConv"):
                LiveConv().start()

            elif user_input.startswith("--liveTranslate"):
                LiveTranslate().start()
                
            elif user_input.startswith("--addInfo"):
                user_input = user_input.replace("--addInfo", "").strip()
                key, value = user_input.split(" ", 1)
                Chatbot().add_message(key, value)
                
            elif self.weather.user_askMeteo(user_input):
                city = self.weather.get_city_in_user_input(user_input)
                if city:
                    city_insee = self.weather.get_insee(city)
                    self.weather.display_weather(city_insee)
                else:
                    print("Chatbot : Je ne connais pas cette ville.")
            
            elif user_input.startswith("--saveSession"):
                user_input = user_input.replace("--saveSession", "").strip()
                self.memory.save_session(user_input)
                print("Chatbot : La session a été sauvegardée avec succès.")

            elif user_input.startswith("--loadSession"):
                user_input = user_input.replace("--loadSession", "").strip()
                self.load_session(user_input)

            elif user_input.startswith("--createSession"):
                self.memory.create_other_session()
                self.messages = self.memory.get("messages")

            elif user_input.startswith("--deleteSession"):
                user_input = user_input.replace("--deleteSession", "").strip()
                check = self.memory.delete_session(user_input)
                if (check):
                    print("Chatbot : La session a été supprimée avec succès.")
                else:
                    print("Chatbot : La session n'existe pas.")

            else:
                self.get_response(user_input)

    def loader(self):
        spin = itertools.cycle(['| ', '/ ', '- ', '\\ '])
        while not self.stop_loading_event.is_set():
            sys.stdout.write(f'\rLoading {next(spin)}')
            sys.stdout.flush()
            time.sleep(0.1)

    def get_response(self, user_input):
        self.stop_loading_event.clear()
        loader_thread = threading.Thread(target=self.loader)
        loader_thread.start()
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages + [{"role": "user", "content": user_input}],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.stop_loading_event.set()
            loader_thread.join()

            bot_reply = response.choices[0].message.content
            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "assistant", "content": bot_reply})
            self.memory.add_message_to_conversation_session("user", user_input)
            self.memory.add_message_to_conversation_session("assistant", bot_reply)
            md = Markdown(bot_reply)
            self.console.print("Chatbot :", md)

        except OpenAI.error.RateLimitError:
            print("Limite de taux dépassée, veuillez réessayer plus tard.")
            time.sleep(60)
        except OpenAI.error.BadRequestError as e:
            print("Erreur dans la requête :", e)
        except Exception as e:
            print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    Chatbot().start()
