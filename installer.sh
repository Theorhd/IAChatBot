#!/bin/bash

echo "OPENAI_API_KEY=" > api_key.config
echo "GOOGLE_CLOUD_API_KEY=" >> api_key.config
echo "Fichier 'api_key.config' créé avec succès."

echo "Installation des paquets..."
pip3 install setuptools
pip3 install --upgrade wheel
pip3 install -r requirements.txt

echo "Installation terminée."
echo "Entrez vos clés API OpenAI et Google Cloud dans le fichier api_key.config pour utiliser le programme."
echo "Pour lancer le programme, exécutez le fichier start.sh."
