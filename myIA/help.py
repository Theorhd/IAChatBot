def help():
    help_text = """
Commandes disponibles pour TheoGPT:

1. Général:
   - Tapez votre question directement pour recevoir une réponse.

2. Commandes spéciales:
   --imageGen <description>     : Génère une image en fonction de la description donnée.
   --imageAnalyze <url_image>   : Analyse l'image située à l'URL fournie.
   --t2s <texte>                : Convertit le texte donné en audio (Text-to-Speech).
   --liveConv                   : Lance une conversation vocale en continu (Speech-to-Text et Text-to-Speech).
   --liveTranslate              : Traduction vocale en temps réel vers une langue spécifiée.

3. Quitter:
   - Tapez "quit" pour quitter la conversation.

Exemple d'utilisation:
- Pour générer une image, tapez: --imageGen Un chat mignon avec un chapeau
- Pour analyser une image, tapez: --imageAnalyze http://exemple.com/monimage.jpg
    """
    print(help_text)
