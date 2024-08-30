# Serial Marketers Slackbot

## Overview

Serial Marketers Slackbot is an integration that connects Slack with ChatGPT, enabling users to interact with the AI directly from their Slack workspace. This project was built to demonstrate how to create a custom integration using Slack's API and OpenAI's GPT model. It was created in Q1 2023 before there was an official integration between Slack and ChatGPT. 

## How to Use

- Add the bot to your workspace
- Add the bot to a channel
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

5. **Run the Bot**
    ```bash
    python bot.py
    ```

## Usage

Once the bot is running, you can start interacting with it in your Slack workspace. Simply mention the bot or use a designated trigger word to send a message to ChatGPT.

### Example Commands

- `@serial-marketers-bot tell me a joke`
- `@serial-marketers-bot summarize the latest news`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any feature requests, bug fixes, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or suggestions, please reach out to [Your Name](mailto:your-email@example.com).

