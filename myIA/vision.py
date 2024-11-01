from openai import OpenAI
import os

api_key_file = 'api_key.config'

current = os.path.dirname(__file__)
parent = os.path.dirname(current)
api_key_file = os.path.join(parent, api_key_file)

with open(api_key_file, 'r') as file:
    api_key = file.read().strip()
    
client = OpenAI(api_key=api_key)

def imageAnalyze(image_url):
    imageAnalyze_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Qu'est-ce qu'il y a sur cette image ?"},
            {
            "type": "image_url",
            "image_url": {
                "url": image_url,
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    return imageAnalyze_response.choices[0].message.content