import requests
import json
from django.conf import settings


def get_deepseek_response(message):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer {}".format(settings.DEEP_AI_API_KEY),
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
        {
            "role": "user",
            "content": message
        }
        ],
        
    })
    )

    return response.json()