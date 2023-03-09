#from sys import stdin
from json import loads
from time import sleep
#from re import search
from os import getenv
import requests

api_key = getenv('API_KEY')
if not api_key:
    raise Exception("Missing API Key. Provide it as an environment variable.")
system_prompt = getenv('SYSTEM_PROMPT') or ""

message_history = [
    {"role": "system", "content": f"""
        {system_prompt}
    """}
]


while True:
    user_message = input(">>> ").strip()
    if user_message == '':
        break

    message_history.append({"role": "user", "content": user_message})
    for i in range(5):
    #tries = 1
    #while True:
        request = requests.post(
            url="https://api.openai.com/v1/chat/completions", #"https://chatgpt-api.shn.hk/v1/",
            #headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": message_history
            }
        )

        if (code := request.status_code) == 200:
            response_object = loads(request.content)
            message = response_object['choices'][0]['message']['content'].strip()
            message_history.append({"role": "assistant", "content": message})
            print(message)
            break
        elif i == 4:
            print(f'Failed with error code {code}:')
            print(request.content.strip().decode('utf-8'))
            #if input('Do you want to discard the message or go back?')
            print('Previous message discarded. Sorry, you\'ll have to type it in again.')
            message_history.pop()
        #else:
            
            #reqs = search(b'Current:\s*(\S+)', request.content)
            # if tries == 1:
            #     print(f'Failed with error code {code}, tried 1 time')
            # else:
            #     print('\033[F\033[K', end='\r')
            #     print(f'Failed with error code {code}, tried {tries} time(s)')
            #print(request.content.strip().decode('utf-8'))
            #if input('Do you want to discard the message or go back?')
        #tries += 1
        sleep(0.5)
        # elif i == 4:
        #     print(f'Failed with error code {code}:')
        #     print(request.content.strip().decode('utf-8'))
        #     #if input('Do you want to discard the message or go back?')
        #     print('Previous message discarded. Sorry, you\'ll have to type it in again.')
        #     message_history.pop()