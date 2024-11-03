@echo off

echo OPENAI_API_KEY= > api_key.config
echo GOOGLE_CLOUD_API_KEY= >> api_key.config
echo Fichier 'api_key.config' créé avec succès.

echo Installation des paquets...
pip install setuptools
pip install --upgrade wheel
pip install -r requirements.txt

echo Installation terminée.
echo Entrez vos clés API OpenAI et Google Cloud dans le fichier api_key.config pour utiliser le programme.
echo Pour lancer le programme, exécutez le fichier start.bat.
pause
