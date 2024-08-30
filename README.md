# Serial Marketers Slackbot

## Overview

Serial Marketers Slackbot is an integration that connects Slack with ChatGPT, enabling users to interact with the AI directly from their Slack workspace. This project was built to demonstrate how to create a custom integration using Slack's API and OpenAI's GPT model. It was created in Q1 2023 before there was an official integration between Slack and ChatGPT. 

## How to Use

- Add the bot to your workspace
- Add the bot to a channel you want to summarize
- Invoke it via a DM where you give a channel name and it will give you a summary of the most recent weeks messages
- It was built with a early version of GPT3.5Turbo that had a 4000 token limit so it has a built in recursive text splitter function to parse large requests into small ones and summarize as it goes

## Setup and Installation

### Prerequisites

- Python 3.x
- Slack workspace and admin access to install the bot
- OpenAI API key

### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/aliss77777/serial-marketers-slackbot.git
    cd serial-marketers-slackbot
    ```

2. **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**

    Create a `.env` file in the root directory of the project and add your Slack bot token and OpenAI API key:
    ```
    SLACK_BOT_TOKEN=your-slack-bot-token
    OPENAI_API_KEY=your-openai-api-key
    ```

5. **Deploy the bot to a web server (e.g. Heroku) to bring the bot online and invokable in slack**
    
    See this page for instructions: https://slack.dev/bolt-js/deployments/heroku/
    

## Usage

Once the bot is running, you can start interacting with it in your Slack workspace. @mention the bot in a DM to send a message to ChatGPT.

### Example Commands

- DM the bot + mention a channel it will give you a summary of up to 1 weeks messages in that channel e.g.: `@ChatGPTBot2.0 #selfpromo`
- DM the bot + include freeform text to get a ChatGPT completion e.g.: `@ChatGPTBot2.0 I'm planning a dinner party can you suggest a theme and a menu I should prepare for the guests?`
- Note the name of the bot will be different depending on your workspace e.g. `@ChatGPTBot2.0`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any feature requests, bug fixes, or improvements.

## Contact

For questions or suggestions, please reach out to me [Alexander Liss](mailto:aliss77777@gmail.com).

