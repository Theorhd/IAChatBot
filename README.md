# TheoGPT Chatbot

**TheoGPT** est un chatbot en Python qui utilise l'API OpenAI pour fournir des réponses en français aux questions des utilisateurs sur divers domaines techniques, en se spécialisant dans les technologies de développement logiciel et web. Ce projet intègre également des fonctionnalités d'analyse d'images, de génération d'images avec DALL-E, de synthèse vocale (TTS), de traduction en direct et de conversation vocale en temps réel.

## Fonctionnalités

- **Réponses sur le développement logiciel et web** : TheoGPT est capable de répondre aux questions concernant de nombreux langages de programmation (Python, JavaScript, Java, etc.), les frameworks populaires, les bases de données, les systèmes d'exploitation, les bonnes pratiques de développement, les tests logiciels et plus encore.
- **Génération d'images avec DALL-E** : Commande : `--imageGen + {prompt}` : pour générer des images basées sur des descriptions.
- **Analyse d'images** : Commande : `--imageAnalyze + {url vers une image}` : pour analyser des images et fournir des informations.
- **Synthèse vocale** : Commande : `--t2s + {prompt}` : pour générer une sortie audio à partir de texte.
- **Conversation en temps réel (Speech-to-Text to Text-to-Speech)** : Commande : `--liveConv` : pour activer une conversation vocale.
- **Traduction en direct** : Commande : `--liveTranslate` : pour activer une traduction en temps réel par le micro.

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Theorhd/IAChatBot.git
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Créez un fichier de configuration de clé API nommé `api_key.config` et ajoutez votre clé OpenAI et GoogleCloudTranslate :
    ```text
    OPENAI_API_KEY=your_api_key_here
    GOOGLE_CLOUD_API_KEY=your_api_key_here
    ```

## Utilisation

Lancez le chatbot en exécutant le fichier principal :

```bash
python app.py
```