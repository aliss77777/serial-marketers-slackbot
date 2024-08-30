
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient

# Import helper functions
from helpers import (
    handle_summary_request,
    handle_completion_request,
    update_home_tab
)

# Load environment variables
load_dotenv()
slack_key = os.environ["SLACK_BOT_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Slack client setup
client = WebClient(token=slack_key)
bot_user_id = client.auth_test()["user_id"]

# Slack Bolt app setup
bolt_app = App(token=slack_key, signing_secret=slack_signing_secret)

@bolt_app.event("message")
def handle_message_events(body, say):
    """
    Handles incoming messages directed at the bot.
    
    Args:
        body (dict): The payload containing event data from Slack.
        say (function): Function to send a message back to the Slack channel.
    """
    logger.info(body)
    
    channel_type = body['event']['channel_type']
    text = body['event']['text']
    
    if channel_type == 'im' and text == 'hi':
        say('Testing DM method')
    
    elif channel_type == 'im' and summarization_request_regex.match(text):
        handle_summary_request(body, say, client, bot_user_id)
    
    elif channel_type == 'im' and completion_request_regex.match(text):
        handle_completion_request(body, say, bot_user_id)

@bolt_app.event("app_home_opened")
def app_home_opened_event(client, event):
    """
    Updates the app home tab when opened.
    
    Args:
        client (WebClient): Slack WebClient instance to publish view updates.
        event (dict): The event data containing user information.
    """
    update_home_tab(client, event)

# Flask app setup
app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Handles Slack events forwarded to this endpoint by Slack's Events API.
    
    Returns:
        Response: The HTTP response returned to Slack.
    """
    return handler.handle(request)

@app.route('/', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint to verify the service is running.
    
    Returns:
        str: A simple 'OK' message.
    """
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
