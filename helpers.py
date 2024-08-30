import os
import time
import datetime as DT
import re
import openai
import tiktoken
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.environ["OPENAPI_KEY"]
CHAT_GPT_MODEL = 'gpt-3.5-turbo-0301'
MAX_TOKENS = 3200
ENCODING = tiktoken.encoding_for_model(CHAT_GPT_MODEL)

# Date calculations for conversation history
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)
week_ago_unix = time.mktime(week_ago.timetuple())

# Regex patterns
summarization_request_regex = re.compile(r'<@U\w{10}> <#C\w{8}|\w{1,}>')
completion_request_regex = re.compile(r'<@U\w{10}> .*')
channel_name_regex = re.compile(r'C\w{8}')

def handle_summary_request(body, say, client, bot_user_id):
    """
    Handles summarization requests for a Slack channel.

    Args:
        body (dict): The payload containing event data from Slack.
        say (function): Function to send a message back to the Slack channel.
        client (WebClient): Slack WebClient instance to fetch conversation history.
        bot_user_id (str): The Slack bot user ID to filter out bot messages.
    """
    say('Request received, please stand by')
    channel_id = channel_name_regex.findall(body['event']['text'])[0]
    conversation_history = client.conversations_history(channel=channel_id, oldest=week_ago_unix)["messages"]
    
    messages = [message["text"] for message in conversation_history if "text" in message and message.get("user") != bot_user_id]
    say(f'Found {len(messages)} messages in the channel.')
    
    text_for_prompt = "\n".join(messages)
    if len(text_for_prompt) > 12000:
        say('This is a big summary request. Please be patient :)')
    
    response = completion_request_handler(text_for_prompt, MAX_TOKENS, ENCODING, 'summarize')
    say(response)

def handle_completion_request(body, say, bot_user_id):
    """
    Handles general completion requests.

    Args:
        body (dict): The payload containing event data from Slack.
        say (function): Function to send a message back to the Slack channel.
        bot_user_id (str): The Slack bot user ID to filter out bot mentions.
    """
    text_for_completion_prompt = body['event']['text'].replace(bot_user_id, '')
    say('One second, processing your request')
    
    response = completion_request_handler(text_for_completion_prompt, MAX_TOKENS, ENCODING, 'respond')
    say(response)

def update_home_tab(client, event):
    """
    Updates the Slack app's home tab when opened.

    Args:
        client (WebClient): Slack WebClient instance to publish view updates.
        event (dict): The event data containing user information.
    """
    client.views_publish(
        user_id=event['user'],
        view={
            "type": "home",
            "callback_id": "home_view",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ("*Welcome to the ChatGPT Slack integration :tada:*\n"
                                 "To use, open a direct message with the bot and follow these steps:\n"
                                 "1. To get a ChatGPT response, @mention the bot and write your query.\n"
                                 "2. To request a channel summary, @mention the bot and include #channel."
                                 "Up to 7 days worth of messages will be retrieved. Ensure the bot is in the channel.")
                    }
                }
            ]
        }
    )

def completion_request_handler(text_for_prompt, max_tokens, encoding, completion_type):
    """
    Handles the completion request for text prompts to be processed by ChatGPT.

    Args:
        text_for_prompt (str): The text to be processed by ChatGPT.
        max_tokens (int): The maximum number of tokens for ChatGPT to process.
        encoding (tiktoken.Encoding): Encoding instance to handle tokenization.
        completion_type (str): The type of completion requested (e.g., 'summarize' or 'respond').

    Returns:
        str: The response from ChatGPT.
    """
    prompt_tokens = encoding.encode(text_for_prompt)
    
    if len(prompt_tokens) < max_tokens:
        return get_summary_chatgpt(text_for_prompt, completion_type)
    else:
        responses = []
        return recursive_completion(prompt_tokens, max_tokens, encoding, responses, completion_type)

def get_summary_chatgpt(text_for_prompt, completion_type):
    """
    Fetches the summary or response from ChatGPT based on the given text prompt.

    Args:
        text_for_prompt (str): The text to be processed by ChatGPT.
        completion_type (str): The type of completion requested (e.g., 'summarize' or 'respond').

    Returns:
        str: The generated content from ChatGPT.
    """
    response = openai.ChatCompletion.create(
        model=CHAT_GPT_MODEL,
        messages=[
            {"role": "system", "content": ("You are an assistant in Slack that provides content completion "
                                           "and content summarization upon user request.")},
            {"role": "user", "content": f'Please {completion_type} the following messages with a rich level of detail and be as clear as possible: ###\n{text_for_prompt}'}
        ]
    )
    return response.choices[0].message['content']

def recursive_completion(prompt_tokens, max_tokens, encoding, responses, completion_type):
    """
    Handles large prompt tokens recursively to fit within the token limit of ChatGPT.

    Args:
        prompt_tokens (list): The list of tokenized prompts to be processed by ChatGPT.
        max_tokens (int): The maximum number of tokens for each chunk to be processed.
        encoding (tiktoken.Encoding): Encoding instance to handle tokenization and decoding.
        responses (list): The list to accumulate responses from ChatGPT.
        completion_type (str): The type of completion requested (e.g., 'summarize' or 'respond').

    Returns:
        str: The combined response from ChatGPT after processing all token chunks.
    """
    while len(prompt_tokens) > 0:
        chunk = encoding.decode(prompt_tokens[:min(max_tokens, len(prompt_tokens))])
        responses.append(get_summary_chatgpt(chunk, completion_type))
        
        prompt_tokens = prompt_tokens[min(max_tokens, len(prompt_tokens)):]
        if len(prompt_tokens) < max_tokens:
            responses.append(get_summary_chatgpt(encoding.decode(prompt_tokens), completion_type))
            break
    
    return '\n'.join(responses)
