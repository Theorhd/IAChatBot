# TheoGPT Chatbot

**TheoGPT** est un chatbot en Python qui utilise l'API OpenAI pour fournir des réponses en français aux questions des utilisateurs sur divers domaines techniques, en se spécialisant dans les technologies de développement logiciel et web. Ce projet intègre également des fonctionnalités d'analyse d'images, de génération d'images avec DALL-E, de synthèse vocale (TTS), de traduction en direct et de conversation vocale en temps réel.

## Fonctionnalités

- **Réponses sur le développement logiciel et web** : TheoGPT est capable de répondre aux questions concernant de nombreux langages de programmation (Python, JavaScript, Java, etc.), les frameworks populaires, les bases de données, les systèmes d'exploitation, les bonnes pratiques de développement, les tests logiciels et plus encore.
- **Génération d'images avec DALL-E** : Commande : `--imageGen + {prompt}` : pour générer des images basées sur des descriptions.
- **Analyse d'images** : Commande : `--imageAnalyze + {url vers une image}` : pour analyser des images et fournir des informations.
- **Synthèse vocale** : Commande : `--t2s + {prompt}` : pour que le texte sortie par TheoGPT soit en audio.
- **Conversation en temps réel (Speech-to-Text to Text-to-Speech)** : Commande : `--liveConv` : pour activer une conversation vocale.
- **Traduction en direct** : Commande : `--liveTranslate` : pour activer une traduction en temps réel par le micro.
- **Ajout d'information a TheoGPT** : Commande : `--addinfo {role} {content}` pour ajouter une information dans la mémoire de TheoGPT de façon permanante.
- **Sessions** : Vous pouvez sauvegarder des sessions de tchat avec la commande : `--saveSession {nom_de_la_session}` et la charger dans une autre session avec : `--loadSession {nom_de_la_session}`, crée une nouvelles sessions avec : `--createSession`. Et supprimé une session avec `--deleteSession {nom_de_la_session}`.
- **Météo** : Demandez au ChatBot de vous donné la météo pour une ville. Exemple : Quelle temps a Toulouse ?

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Theorhd/IAChatBot.git
    ```

2. Installation du programme :
    ```text
    1 - Lancer le fichier installer.bat pour installer les dépendances.
    2 - Ajoutez vos clés API dans le fichier api_key.config.
    3 - Lancer le programme avec start.bat.
    ```
    ```bash
    !! Important !!
    Si un problème survient lors de l'installation de `installer.bat`, effectuez les commandes suivantes dans PowerShell :
    pip cache purge
    ```

## Utilisation

Lancez le chatbot en exécutant le fichier start.bat :

```bash
start.bat
```
