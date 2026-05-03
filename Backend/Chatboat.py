from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing datetime module for real-time info.
from dotenv import dotenv_values  # To load environment variables.
import os

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

# Retrieve environment variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using API key.
client = Groq(api_key=GroqAPIKey)

# Get absolute path to Data directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), "Data")
chatlog_path = os.path.join(data_dir, "ChatLog.json")

# Initialize an empty list to store chat messages.
messages = []

# Define system message (can customize assistant behavior here)
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# System instruction list
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load chat history from JSON file
try:
    with open(chatlog_path, "r") as f:
        messages = load(f)  # Load existing messages
except FileNotFoundError:
    # If file not found, create empty chat log
    with open(chatlog_path, "w") as f:
        dump([], f)

# Function to get real-time date and time
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # Current date & time

    day = current_date_time.strftime("%A")  # Day name
    date = current_date_time.strftime("%d")  # Date
    month = current_date_time.strftime("%B")  # Month
    year = current_date_time.strftime("%Y")  # Year
    hour = current_date_time.strftime("%H")  # Hour
    minute = current_date_time.strftime("%M")  # Minute
    second = current_date_time.strftime("%S")  # Second

    # Format into readable string
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds.\n"

    return data

# Function to clean chatbot response
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split lines
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
    modified_answer = '\n'.join(non_empty_lines)  # Join cleaned lines
    return modified_answer

# Main chatbot function
def ChatBot(Query):
    """This function sends user query to chatbot and returns response."""

    try:
        # Load chat history
        with open(chatlog_path, "r") as f:
            messages = load(f)

        # Add user query
        messages.append({"role": "user", "content": f"{Query}"})

        # Send request to Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Model name
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,  # Response length limit
            temperature=0.7,  # Creativity level
            top_p=1,
            stream=True,  # Enable streaming
            stop=None
        )

        # Store response
        Answer = ""

        # Process streaming response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Clean unwanted tokens
        Answer = Answer.replace("</s>", "")

        # Save assistant response
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open(chatlog_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        # Handle errors and reset chat log
        print(f"Error: {e}")
        with open(chatlog_path, "w") as f:
            dump([], f, indent=4)

        return ChatBot(Query)  # Retry

# Run chatbot loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))