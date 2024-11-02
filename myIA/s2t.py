import speech_recognition as sr
from myIA.t2s import TextToSpeech

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Parlez maintenant...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                print("Vous avez dit : " + text)
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print("Erreur avec le service Google Speech Recognition ; {0}".format(e))

class LiveConv:
    @staticmethod
    def start():
        speech_to_text = SpeechToText()
        tts = TextToSpeech() 
        print("Début de la conversation. Dites 'quitter' pour terminer la conversation.")
        while True:
            text = speech_to_text.speech_to_text()
            if text is None:
                print("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
                continue
            elif text.lower() == 'quitter':
                print("Fin de la conversation.")
                break
            else:
                response = tts.chat_t2s(text) 
