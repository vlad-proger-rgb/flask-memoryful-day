import openai
import urllib3
import requests

from settings import OPENAI_API_KEY

# from custom_loggers import GPTLogger

CLIENT = openai.OpenAI(
    api_key = OPENAI_API_KEY,
    timeout=30
)

def get_completion(prompt, model="gpt-3.5-turbo"):
    """Get a response to a give prompt"""
    messages = [{"role": "user", "content": prompt}]
    try:
        response = CLIENT.chat.completions.create(
            model = model,
            messages = messages,
            temperature = 0
        )
        # GPTLogger.debug(f"GPT answer: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        # GPTLogger.error(f"Requst to OpenAI error: {e}.\nClass:{e.__class__}", exc_info=True)
        return f"Error happend during the requst to OpenAI: {e}. Try /start"



def get_completion_from_messages(messages, model="gpt-3.5-turbo"):
    """Get a response to a give prompt"""

    try:
        response = CLIENT.chat.completions.create(
            model = model,
            messages = messages,
            temperature = 0
        )
        # GPTLogger.debug(f"GPT answer: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        # GPTLogger.error(f"Requst to OpenAI error: {e}.\nClass:{e.__class__}", exc_info=True)
        return f"Error happend during the requst to OpenAI: {e}"
    except openai.APITimeoutError as e:
        # GPTLogger.error(f"Requst to OpenAI error: {e}.\nClass:{e.__class__}", exc_info=True)
        return f"Error happend during the requst to OpenAI: {e}. Try /start"
    except urllib3.exceptions.ReadTimeoutError as rte:
        # GPTLogger.error(f"Requst to OpenAI error: {rte}.\nClass:{rte.__class__}", exc_info=True)
        return f"Error happend during the requst to OpenAI: {rte}. Try /start"
    except requests.exceptions.ReadTimeout as rt:
        # GPTLogger.error(f"Requst to OpenAI error: {rt}.\nClass:{rt.__class__}", exc_info=True)
        return f"Error happend during the requst to OpenAI: {rt}. Try /start"