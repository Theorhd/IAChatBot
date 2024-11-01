import gtts
from playsound import playsound
import os
import time
import tempfile
from openai import OpenAI
from mutagen.mp3 import MP3

def text_to_speech(text, lang='fr'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        mp3_filename = temp_file.name

    tts = gtts.gTTS(text, lang=lang)
    tts.save(mp3_filename)

    try:
        audio = MP3(mp3_filename)
        duration = audio.info.length
        playsound(mp3_filename)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")
    finally:
        time.sleep(duration)
        os.remove(mp3_filename)

def chat_t2s(user_input):
    parent = os.path.dirname(os.path.dirname(__file__))
    api_key_file = os.path.join(parent, 'api_key.config')
    
    with open(api_key_file, 'r') as file:
        for line in file:
            if line.startswith("OPENAI_API_KEY"):
                api_key = line.split('=')[1].strip()
                break
            api_key = api_key

    messages = [
        {"role": "system", "content": "Vous êtes un chatbot. Spécialisé dans les questions-réponses... (contenu ici)"}
    ]

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages + [{"role": "user", "content": user_input}],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"}
        )

        bot_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_reply})
        print("Chatbot :", bot_reply)
        text_to_speech(bot_reply)

        if len(messages) > 20:
            messages = messages[-20:]
                
    except OpenAI.error.RateLimitError:
        print("Limite de taux dépassée, veuillez réessayer plus tard.")
        time.sleep(60)
    except OpenAI.error.BadRequestError as e:
        print("Erreur dans la requête :", e)
    except Exception as e:
        print("Une erreur s'est produite :", e)
