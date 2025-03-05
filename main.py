from tkinter import *
from tkinter import ttk, scrolledtext
import openai
from pathlib import Path
import threading
from playsound import playsound

client = None
message_history = []

def initialize_client():
    global client
    api_key = apikeyEntry.get()
    client = openai.OpenAI(api_key=api_key)
    print("OpenAI client initialized.")

def play_audio_in_background(file_path):
    """Play the audio file in a separate thread."""
    playsound("./speech.mp3")

def send_request():
    global client
    if client is None:
        initialize_client()

    selected_model = modelComboBox.get()
    temperature = tempScale.get()
    message = textbox.get("1.0", END).strip()
    freqPen = freqScale.get()
    tokens = tokenEntry.get()
    readAloud = readAloudVar.get()
    aiVoice = aiVoiceComboBox.get()

    if not message:
        print("No message provided.")
        return

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

        if readAloud == True:
            speech_file_path = Path(__file__).parent / "speech.mp3"
            audio = client.audio.speech.create(
            model="tts-1",
            voice=aiVoice,
            input=response)

            audio.stream_to_file(speech_file_path)

        message_history.append({"role": "assistant", "content": response})

        chatbox.config(state="normal")
        chatbox.insert(END, f"Assistant: {response}\n\n")
        chatbox.config(state="disabled")

        window.update()

        if readAloud == True:
            # Start the audio playing in a separate thread
            threading.Thread(target=play_audio_in_background, args=(speech_file_path,)).start()

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
apikeyEntry = Entry(window, textvariable=apiKey, font=('calibre',10,'normal'), show="*")

tempLabel = Label(window, text="Temperature")
tempScale = Scale(window, from_=0.0, to=2.0, orient=HORIZONTAL, resolution=0.01, length=200)

freqLabel = Label(window, text="Frequency Penalty")
freqScale = Scale(window, from_=-2.0, to=2.0, orient=HORIZONTAL, resolution=0.01, length=200)
freqScale.set(0)

tokenLabel = Label(window, text="Max Tokens")
maxTokens.set(1000)
tokenEntry = Entry(window, textvariable=maxTokens, font=('calibre',10,'normal'))

chatbox = scrolledtext.ScrolledText(window, wrap=WORD, height=30, width=108)
chatbox.config(state="disabled")

textbox = scrolledtext.ScrolledText(window, wrap=WORD, height=4, width=108)
textSend = Button(window, text="Send Message", command=send_request)

promptTokensLabel = Label(window, textvariable=promptTokens)
responseTokensLabel = Label(window, textvariable=responseTokens)
totalTokensLabel = Label(window, textvariable=totalTokens)

readAloudVar = BooleanVar()
readAloud = Checkbutton(window, text="Read Aloud", variable=readAloudVar)

aiVoice = StringVar()
aiVoiceComboBox = ttk.Combobox(window, values=["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
aiVoiceComboBox.set("alloy")

# Positioning widgets with grid
chatbox.grid(column=2, row=0, rowspan=10, sticky='nsew')
textbox.grid(column=2, row=12, sticky='ews')
textSend.grid(column=2, row=13, sticky='s')

modelLabel.grid(column=0, row=0, sticky="w")
modelComboBox.grid(column=1, row=0, sticky="ew")

apikeyLabel.grid(column=0, row=1, sticky="w")
apikeyEntry.grid(column=1, row=1, sticky="ew")

tempLabel.grid(column=0, row=2, sticky="w")
tempScale.grid(column=1, row=2, sticky="ew")

freqLabel.grid(column=0, row=3, sticky="w")
freqScale.grid(column=1, row=3, sticky="ew")

tokenLabel.grid(column=0, row=4, sticky="w")
tokenEntry.grid(column=1, row=4, sticky="ew")

promptTokensLabel.grid(column=0, row=5, sticky="w")
responseTokensLabel.grid(column=0, row=6, sticky="w")
totalTokensLabel.grid(column=0, row=7, sticky="w")

readAloud.grid(column=0, row=8, sticky="w")
aiVoiceComboBox.grid(column=1, row=8, sticky="ew")

# Configure row and column weights to allow resizing
window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
window.grid_rowconfigure(12, weight=0) # Keep row 12 fixed
window.grid_rowconfigure(13, weight=0) # Keep row 13 fixed
window.grid_columnconfigure(2, weight=1)  # Allow column 2 to expand

# Set specific row weights for the sidebar
for i in range(8):  # Assuming rows 0 to 7 for sidebar elements
    window.grid_rowconfigure(i, weight=0)

# Make the model combobox expand horizontally within its column
window.grid_columnconfigure(0, weight=0)  # Keep label columns non-expandable
window.grid_columnconfigure(1, weight=0)  # Allow widgets in column 1 to stretch horizontally

window.mainloop()
