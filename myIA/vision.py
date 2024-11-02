from openai import OpenAI
import os

class ImageAnalyzer:
    parent = os.path.dirname(os.path.dirname(__file__))
    api_key_file = os.path.join(parent, 'api_key.config')
    with open(api_key_file, 'r') as file:
        for line in file:
            if line.startswith("OPENAI_API_KEY"):
                api_key = line.split('=')[1].strip()
                break

    def __init__(self):
        self.client = OpenAI(api_key=self.api_key)

    def image_analyze(self, image_url):
        imageAnalyze_response = self.client.chat.completions.create(
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
