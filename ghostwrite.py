from sys import stdin, exit
import json

import requests

# Read in the prompt.
user_input = stdin.read().strip()
if user_input == '':
    exit(1)

# Grab a rough draft to refine later.
draft = ""
request = requests.post(
    url="https://chatgpt-api.shn.hk/v1/",
    #headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}]
    }
)
if (code := request.status_code) == 200:
    response_object = json.loads(request.content)
    draft = response_object['choices'][0]['message']['content'].strip()
    print(draft, end="\n\n\n\n")
else:
    print(f'Failed with error code {code}:')
    print(request.content.strip().decode('utf-8'))
    exit(1)

# Go through a set of prompts to refine this, adding them to the output and a message history.
steps = [
    """I'm going to give you some information before asking you to write an article. You will use this information to produce your output.
When it comes to writing content, two factors are crucial, "perplexity" and "burstiness." Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with great burstiness, for example, with some longer or complex sentences alongside shorter sentences. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness.
Using these concepts, rewrite this article with a high degree of perplexity and burstiness:""",
    """Rewrite this article changing 50% of nouns and verbs for similar ones and rewrite verb usages to add natural sounding variations in complexity but retain the same tense and overall meaning.:"""
]
message_history = []

for prompt in steps:
    message_history.append({"role": "user", "content": f'{prompt}\n\n{draft}'})
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
        draft = message
        print(message, end="\n\n\n\n")
    else:
        print(f'Failed with error code {code}:')
        print(request.content.strip().decode('utf-8'))
        exit(1)