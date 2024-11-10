import os
import json
import logging
from rich.console import Console
from rich.markdown import Markdown

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

data_json = os.path.join(parent, 'chatbot_data.json')
if os.path.dirname(data_json) and not os.path.exists(os.path.dirname(data_json)):
    os.makedirs(os.path.dirname(data_json), exist_ok=True)

class Memory:
    def __init__(self):
        self.data = {}
        self.load()
        self.conversation = []
        self.console = Console()
        logging.info("Initialisation de la mémoire du chatbot.")

    def load(self):
        if os.path.exists(data_json):
            with open(data_json, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        logging.info("Chargement de la mémoire du chatbot.")

    def save(self):
        with open(data_json, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)
        logging.info("Sauvegarde de la mémoire du chatbot.")

    def add(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        messages = self.data.get(key)
        if isinstance(messages, list) and all(isinstance(msg, dict) and "role" in msg and "content" in msg for msg in messages):
            logging.info(f"Récupération des messages de la mémoire du chatbot.")
            return messages
        logging.info(f"Récupération de la mémoire du chatbot.")
        return [
            {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses. La langue française est votre domaine de prédilection. Toutes les conversations que tu as doivent etre en français. Ton dommaine d'expertise est le développement, principalement web et logiciel. Tu connais a la perfection les langages de programmation comme Python, Java, C++, JavaScript, HTML, CSS, SQL, PHP, Ruby, Swift, Kotlin, etc. Tu es capable de répondre à des questions sur les frameworks et les bibliothèques les plus populaires. Tu as une connaissance approfondie des bases de données relationnelles et non relationnelles. Tu es capable de répondre à des questions sur les systèmes d'exploitation les plus populaires. Tu es capable de répondre à des questions sur les technologies de développement web et mobile. Tu es capable de répondre à des questions sur les méthodologies de développement logiciel. Tu es capable de répondre à des questions sur les outils de développement logiciel. Tu es capable de répondre à des questions sur les bonnes pratiques de développement logiciel. Tu es capable de répondre à des questions sur les principes de conception logicielle. Tu es capable de répondre à des questions sur les architectures logicielles. Tu es capable de répondre à des questions sur les tests logiciels. Tu es capable de répondre à des questions sur les déploiements logiciels. Tu es capable de répondre à des questions sur les environnements de développement intégrés. Tu es capable de répondre à des questions sur les systèmes de contrôle de version. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de code source. Tu es capable de répondre à des questions sur les systèmes de gestion de base de données. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Tu es capable de répondre à des questions sur les systèmes de gestion de configuration. Tu es capable de répondre à des questions sur les systèmes de gestion de serveur. Tu es capable de répondre à des questions sur les systèmes de gestion de réseau. Tu es capable de répondre à des questions sur les systèmes de gestion de projet. Tu es capable de répondre à des questions sur les systèmes de gestion de qualité. Tu es capable de répondre à des questions sur les systèmes de gestion de version. Tu es capable de répondre à des questions sur les systèmes de gestion de workflow. Tu es capable de répondre à des questions sur les systèmes de gestion de contenu. Ton nom est TheoGPT."}
        ]

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save()
            logging.info(f"Suppression de la clé '{key}' de la mémoire du chatbot.")
    
    def add_message_to_conversation_session(self, role, content):
        """Ajoute un message et le sauvegarde dans la mémoire JSON"""
        if role not in ["user", "assistant", "system"]:
            logging.error("Le rôle doit être 'user', 'assistant' ou 'system'.")
            return None
        self.conversation.append({"role": role, "content": content})
        return True
    
    def save_session(self, name):
        session_dir = os.path.join(parent, "sessions")
        if not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)
        session_path = os.path.join(session_dir, f"{name}.json")
        with open(session_path, 'w', encoding='utf-8') as file:
            json.dump(self.conversation, file, indent=4)
        logging.info(f"Sauvegarde de la session de conversation '{name}'.")
    
    def delete_session(self, name):
        session_path = os.path.join(parent, "sessions", f"{name}.json")
        if os.path.exists(session_path):
            os.remove(session_path)
            logging.info(f"Suppression de la session de conversation '{name}'.")
            return True
        logging.error(f"La session de conversation '{name}' n'existe pas.")
        return False

    def create_other_session(self):
        self.conversation = []
        print("""Création d'une nouvelle session de conversation.
              """)
        logging.info("Création d'une nouvelle session de conversation.")

    def load_json_in_conversation(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.conversation = json.load(file)

    def display_sessions_history(self):
        sessions_dir = os.path.join(parent, "sessions")
        if os.path.exists(sessions_dir):
            sessions = os.listdir(sessions_dir)
            if sessions:
                return [os.path.splitext(session)[0] for session in sessions]
        return False
    
    def display_session_content(self, session_name):
        session_path = os.path.join(parent, "sessions", f"{session_name}.json")
        if os.path.exists(session_path):
            with open(session_path, 'r', encoding='utf-8') as file:
                conversation = json.load(file)
                for message in conversation:
                    role_display = "Vous" if message['role'] == "user" else "Chatbot"
                    texte = f"""{role_display} : {message['content']}
                          """
                    md = Markdown(texte)
                    self.console.print(md)
                    print(" ")
                return True
        return False