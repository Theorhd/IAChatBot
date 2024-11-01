import speech_recognition as sr
from myIA.t2s import chat_t2s

recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous avez dit : " + text)
        except sr.UnknownValueError:
            print("Impossible de comprendre l'audio")
        except sr.RequestError as e:
            print("Erreur avec le service Google Speech Recognition ; {0}".format(e))

def liveConv():
    while True:
        text = speech_to_text()
        chat_t2s(text)
