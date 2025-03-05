# ChatGPT-Python-Application

A simple GUI application built with Tkinter for interacting with OpenAI's GPT models. This application allows users to input an API key, select a model, set parameters, and send messages to the model. The responses from the model are displayed in a chatbox.

## Features

- **API Key Input**: Securely input your OpenAI API key.
- **Model Selection**: Choose from a list of available GPT models.
- **Parameter Settings**: Adjust the temperature, frequency penalty, and maximum tokens for the model.
- **Message Sending**: Type and send messages to the selected GPT model.
- **Response Display**: View the model's responses in a chatbox.
- **Token Usage Display**: Monitor the number of prompt tokens, response tokens, and total tokens used.

## Widgets

- **Main Application Window**: The primary window of the application.
- **Model Dropdown**: A dropdown menu to select the GPT model.
- **API Key Entry**: An entry widget to input the API key.
- **Temperature Scale**: A scale widget to set the temperature parameter.
- **Frequency Penalty Scale**: A scale widget to set the frequency penalty parameter.
- **Max Tokens Entry**: An entry widget to set the maximum number of tokens.
- **Chatbox**: A scrolled text widget to display the conversation.
- **Textbox**: A scrolled text widget to input the user's message.
- **Send Button**: A button to send the message.
- **Prompt Tokens Label**: A label to display the number of prompt tokens used.
- **Response Tokens Label**: A label to display the number of response tokens used.
- **Total Tokens Label**: A label to display the total number of tokens used.

## Usage

1. Run the script to open the GUI application.
2. Enter your OpenAI API key in the provided entry field.
3. Select the desired GPT model from the dropdown menu.
4. Adjust the temperature and frequency penalty using the scale widgets.
5. Set the maximum number of tokens in the entry field.
6. Type your message in the textbox and click "Send Message" to interact with the GPT model.
7. View the model's response in the chatbox.

## Running the Application

To run the application, execute the following command:

```sh
python main.py
```

## Dependencies

- tkinter
- requests
- openai