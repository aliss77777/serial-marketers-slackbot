# General libraries
import re
import string
import os
import openai
import logging
from dotenv import load_dotenv
import tiktoken

load_dotenv()

openai.api_key = os.environ["OPENAPI_KEY"]
slack_key = os.environ["SLACK_BOT_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
chat_gpt_model = 'gpt-3.5-turbo-0301'
max_tokens = 3200
encoding = tiktoken.encoding_for_model(chat_gpt_model)

# Slack and Flask libraries
from slack_sdk import WebClient
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# getting one week's worth on conversation history: used in the conversation history summary section
import time
import datetime as DT
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)
week_ago_unix = time.mktime(week_ago.timetuple())

# WebClient instantiates a client that can call API methods such as bot_ID and conversation history
client = WebClient(token=slack_key)
bot_user_id = client.auth_test()
bot_user_id = bot_user_id['user_id']

# creating regex pattern for channel mention in direct mentiod
summarization_request_regex = re.compile('<@U\w{10}> <#C\w{8}|\w{1,}>') # e.g. 'C04T04MPAJV'
#  'text': '<@U04U6BU020K> <#CBH4YNBFF|lounge>'
completion_request_regex = re.compile('<@U\w{10}> .*')
# '<@U04QXFF5W9W> can you tell me'
channel_name_regex = re.compile('C\w{8}') # e.g. 'CBH4YNBFF'

# using bolt as message responder per guidance from Slack on how to avoid duplicate messages
# https://github.com/slackapi/python-slack-sdk/issues/1164
bolt_app = App(
    token=slack_key,
    signing_secret=slack_signing_secret)


@bolt_app.event("message")
def handle_message_events(body, say, logger):
    logger.info(body)
    #print(body)
    # handling DM's directed at the bot
    if body['event']['channel_type'] == 'im' and body['event']['text'] == 'hi':
         say('testing DM method')  # my user ID U04Q13P1GJJ

    # handling channel summary request
    elif body['event']['channel_type'] == 'im' and summarization_request_regex.match(body['event']['text']) != None:
        completion_type = 'summarize'
        channel_id = channel_name_regex.findall(body['event']['text'])[0]
        say('Request received, please stand by')
        #say('channel ' + channel_id + ' summary goes here')  # my user ID U04Q13P1GJJ
        conversation_history = client.conversations_history(channel=channel_id, oldest=week_ago_unix)["messages"]
        # print(conversation_history)
        messages = [message["text"] for message in conversation_history if
                    "text" in message and "bot_id" not in message]
        messages = [message["text"] for message in conversation_history if
                    "text" in message and message["user"] != bot_user_id]
        length_of_messages = 'here are how many messages I found: ' + str(len(messages))
        say(length_of_messages)

        # creating one big message from all the conversations
        text_for_prompt = "\n".join(messages)
        char_length = 'I found this many characters in the message history ' + str(len(text_for_prompt))
        say(char_length)
        if len(text_for_prompt) > 12000:
            say('This is a big summary request. Please be patient :)')
        say(completion_request_handler(text_for_prompt, max_tokens, encoding, completion_type))

    # handling general completion prompt
    elif body['event']['channel_type'] == 'im' and completion_request_regex.match(body['event']['text']) != None:
        completion_type = 'respond'
        text_for_completion_prompt = body['event']['text']
        text_for_completion_prompt = text_for_completion_prompt.replace(bot_user_id, '')
        say('One second, processing your request ')
        say(completion_request_handler(text_for_completion_prompt, max_tokens, encoding, completion_type))

    return print(body)

# handling bot app home views just for logging info
@bolt_app.event("app_home_opened")
def update_home_tab(client, event, logger):
    logger.info(event)
    client.views_publish(
        user_id=event['user'],
        view={
            "type":"home",
            "callback_id":"home_view",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": '''*Welcome to the ChatGPT slack integration:tada: Go to the messages tab to interact.
                            To use, open a direct message with the bot and do the following:
                            1. To get a ChatGPT response, @mention the bot and write out your query.
                            2. To do a channel summarization requestion, @mention the bot and the also #channel
                                By default up to 7 days worth of messages will be retrieved.
                                Make sure you add the bot to the channel first otherwise it won't work.  
                                '''
                    }
                }],
        }
    )

# summarizing mentions in a channel
# @bolt_app.event("app_mention")
# def gpt_completion(body, say, logger):
#     # basic summary of whatever's contained in the chat request
#     logger.info(body)
#     #print(body)
#
#     # get # of conversions in the channel
#     channel_id = (body['event']['channel'])
#     conversation_history = client.conversations_history(channel=channel_id, oldest=week_ago_unix)["messages"]
#     #print(conversation_history)
#     messages = [message["text"] for message in conversation_history if "text" in message and "bot_id" not in message]
#     messages = [message["text"] for message in conversation_history if
#                 "text" in message and message["user"] != bot_user_id]
#     length_of_messages = 'here are how many messages I found: ' + str(len(messages))
#     say(length_of_messages)
#     # client.chat_postMessage(channel=channel_id, text=length_of_messages)
#
#     # creating one big message from all the conversations
#     text_for_prompt = "\n".join(messages)
#     char_length = 'I found this many characters in the message history ' + str(len(text_for_prompt))
#     say(char_length)
#     if len(text_for_prompt) > 12000:
#         say('This is a big summary request. Please be patient :)')
#     # say('original text\n')
#     # say(text_for_prompt)
#     # say('====================================')
#     # say('ChatGPT response to summary request')
#     say(completion_request_handler(text_for_prompt, max_tokens, encoding))


app = Flask(__name__)

handler = SlackRequestHandler(bolt_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@app.route('/', methods=['GET'])
def healthcheck():
    return 'OK'

logger = logging.getLogger(__name__)


def completion_request_handler(text_for_prompt, max_tokens, encoding, completion_type):
    completion_type = completion_type
    prompt_tokens = encoding.encode(text_for_prompt)
    if len(prompt_tokens) < max_tokens:
        return get_summary_chatgpt(text_for_prompt, completion_type)
    else:
        responses = []
        return recursive_completion(prompt_tokens, max_tokens, encoding, responses, )


def get_summary_chatgpt(text_for_prompt, completion_type):
    completion_type = completion_type
    response = openai.ChatCompletion.create(
        model=chat_gpt_model,
        messages=[
            {"role": "system", "content": '''You are an assistant in Slack that provides content completion
                                                        and content summarization upon user request.'''},
            {"role": "user", "content": 'Please ' + completion_type + ''' the following messages with a rich level of detail 
                                            and be as clear as possible: ''' + "###\n" + text_for_prompt},
        ]
    )
    print(response)
    return response.choices[0].message['content']

def recursive_completion(prompt_tokens, max_tokens, encoding, responses, completion_type):
    completion_type = completion_type
    i = 0
    while len(prompt_tokens) > 0:
        print('prompt token length is ' + str(len(prompt_tokens)))
        # gets the 'head' tokens of the token bunch
        chunk = encoding.decode(prompt_tokens[:min(max_tokens, len(prompt_tokens))])
        print('now on chunk number: ' + str(i))
        i += 1
        responses.append(get_summary_chatgpt(chunk, completion_type))
        # slices off the 'head' and continues through
        prompt_tokens = prompt_tokens[min(max_tokens, len(prompt_tokens)):len(prompt_tokens)]
        print('prompt token length is ' + str(len(prompt_tokens)))
        if len(prompt_tokens) < max_tokens:
            print('completing recursive function')
            responses.append(get_summary_chatgpt(encoding.decode(prompt_tokens), completion_type))
            prompt_tokens = prompt_tokens[len(prompt_tokens):len(prompt_tokens)]
            print('prompt token length is ' + str(len(prompt_tokens)))
            break
    return '\n'.join(responses)




if __name__ == '__main__':
    app.run(debug=True)
