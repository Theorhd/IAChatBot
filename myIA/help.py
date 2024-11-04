import logging
import os

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

class Help:
    @staticmethod
    def display():
        help_text = """
Commandes disponibles pour TheoGPT:

1. Général:
   - Tapez votre question directement pour recevoir une réponse.

2. Commandes spéciales:
   --imageGen <description>     : Génère une image en fonction de la description donnée.
   --imageAnalyze <url_image>   : Analyse l'image située à l'URL fournie.
   --t2s <texte>                : Convertit le texte de sortie de TheoGPT en audio (Text-to-Speech).
   --liveConv                   : Lance une conversation vocale en continu (Speech-to-Text et Text-to-Speech).
   --liveTranslate              : Traduction vocale en temps réel vers une langue spécifiée.
   --addInfo <role> <info>      : Ajoute une information à la mémoire de TheoGPT de façon permanante.

3. Quitter:
   - Tapez "quit" pour quitter la conversation.

Exemple d'utilisation:
- Pour générer une image, tapez: --imageGen Un chat mignon avec un chapeau
- Pour analyser une image, tapez: --imageAnalyze http://exemple.com/monimage.jpg
        """
        print(help_text)
        logging.info("Affichage de l'aide.")
