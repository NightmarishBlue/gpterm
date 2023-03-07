from sys import stdin
import json

import requests

message_history = [
    # {"role": "system", "content": """

    # """}
]

while True:
    user_message = input(">>> ").strip()
    if user_message == '':
        break

    message_history.append({"role": "user", "content": user_message})
    request = requests.post(
        url="https://chatgpt-api.shn.hk/v1/",
        #headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": message_history
        }
    )

    if (code := request.status_code) == 200:
        response_object = json.loads(request.content)
        message = response_object['choices'][0]['message']['content'].strip()
        message_history.append({"role": "assistant", "content": message})
        print(message)
    else:
        print(f'Failed with error code {code}:')
        print(request.content.strip().decode('utf-8'))
        break