# gpterm
Messing with ChatGPT's API. Currently, basically ChatGPT in the terminal, but bad.

## Requirements
* Python. Version 3, I think.
* The `python-dotenv` package, optionally.

### How to use
1. Set the `API_KEY` variable to your OpenAI API key, either on the commandline or in the .env file if you have `python-dotenv`. If you don't have one, get one for free [here](https://platform.openai.com/account/api-keys).
2. Optionally, set the `SYSTEM_PROMPT` variable to change ChatGPT's behaviour.
3. Run `gpterm.py` and enjoy the results.
