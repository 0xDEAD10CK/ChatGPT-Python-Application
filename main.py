from tkinter import *
from tkinter import ttk, scrolledtext
import requests
import openai

client = None
message_history = []

def initialize_client():

    global client
    api_key = apikeyEntry.get()
    client = openai.OpenAI(api_key=api_key)
    
    print("OpenAI client initialized.")

def send_request():
    
    global client
    
    if client is None:
        initialize_client()

    selected_model = modelComboBox.get()
    temperature = tempScale.get()
    message = textbox.get("1.0", END).strip()
    freqPen = freqScale.get()
    tokens = tokenEntry.get()

    if not message:
        print("No message provided.")
        return

    print(f"Selected Model: {selected_model}")

    textbox.delete("1.0", END)

    chatbox.config(state="normal")
    chatbox.insert(END, f"User: {message}\n\n")
    chatbox.config(state="disabled")

    window.update()
    
    message_history.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model=selected_model,
            temperature=temperature,
            max_tokens=int(tokens),
            frequency_penalty=freqPen,
            messages=message_history
        )
        
        response = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": response})

        chatbox.config(state="normal")
        chatbox.insert(END, f"Assistant: {response}\n\n")
        chatbox.config(state="disabled")

        promptTokens.set(f"Prompt Tokens: {completion.usage.prompt_tokens}")
        responseTokens.set(f"Response Tokens: {completion.usage.completion_tokens}")
        totalTokens.set(f"Total Tokens: {completion.usage.total_tokens}")

    except Exception as e:
        print(f"An error occurred: {e}")

    window.update()


window = Tk()

window.title("ChatGPT Application")
window.geometry("1200x600")

maxTokens = StringVar()
apiKey = StringVar()

promptTokens = StringVar()
responseTokens = StringVar()
totalTokens = StringVar()

promptTokens.set("Prompt Tokens: 0")
responseTokens.set("Response Tokens: 0")
totalTokens.set("Total Tokens: 0")

modelLabel = Label(window, text="Model")
modelComboBox = ttk.Combobox(window, values=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo-0125"])
modelComboBox.set("gpt-3.5-turbo-0125")

apikeyLabel = Label(window, text="Api Key")
apikeyEntry = Entry(window, textvariable = apiKey, font = ('calibre',10,'normal'), show="*")

tempLabel = Label(window, text="Temperature")
tempScale = Scale(window, from_=0.0, to=2.0, orient=HORIZONTAL, resolution=0.01, length=200)

freqLabel = Label(window, text="Frequency Penalty")
freqScale = Scale(window, from_=-2.0, to=2.0, orient=HORIZONTAL, resolution=0.01, length=200)
freqScale.set(0)

tokenLabel = Label(window, text="Max Tokens")
maxTokens.set(1000)
tokenEntry = Entry(window, textvariable = maxTokens, font = ('calibre',10,'normal'))

chatbox = scrolledtext.ScrolledText(window, wrap=WORD, height=30, width=108)
chatbox.config(state="disabled")

textbox = scrolledtext.ScrolledText(window, wrap=WORD, height=4, width=108)
textSend = Button(window, text="Send Message", command = send_request)

promptTokensLabel = Label(window, textvariable = promptTokens)
responseTokensLabel = Label(window, textvariable = responseTokens)
totalTokensLabel = Label(window, textvariable = totalTokens)

chatbox.grid(column=2, row=0, rowspan=10)
textbox.grid(column=2, row=12)
textSend.grid(column=2, row=13)

modelLabel.grid(column=0, row=0)
modelComboBox.grid(column=1, row=0)

apikeyLabel.grid(column=0, row=1)
apikeyEntry.grid(column=1, row=1)

tempLabel.grid(column=0, row=2)
tempScale.grid(column=1, row=2)

freqLabel.grid(column=0, row=3)
freqScale.grid(column=1, row=3)

tokenLabel.grid(column=0, row=4)
tokenEntry.grid(column=1, row=4)

promptTokensLabel.grid(column = 0, row = 5)
responseTokensLabel.grid(column = 0, row = 6)
totalTokensLabel.grid(column = 0, row = 7)

window.mainloop()
