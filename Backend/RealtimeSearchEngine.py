import requests
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.
from tavily import TavilyClient  # Importing Tavily client for search functionality.
import os

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
TavilyAPIKey = env_vars.get("TavilyAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Get the absolute path to the Data directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), "Data")
chatlog_path = os.path.join(data_dir, "ChatLog.json")

# Define the system instructions for the chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(chatlog_path, "r") as f:
        messages = load(f)
except:
    with open(chatlog_path, "w") as f:
        dump([], f)

# Function to perform a Tavily search and format the results.
def TavilySearch(query):
    client = TavilyClient(api_key=TavilyAPIKey)
    
    # Perform search with Tavily
    response = client.search(query=query, max_results=5)
    
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    if "results" in response and response["results"]:
        for item in response["results"]:
            Answer += f"Title: {item.get('title', 'N/A')}\nDescription: {item.get('content', 'N/A')}\n\n"
    else:
        Answer += "No results found.\n\n"
    
    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    data = ""
    current_date_time = datetime.datetime.now()

    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"

    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load chat log
    with open(chatlog_path, "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Tavily search results
    SystemChatBot.append({"role": "system", "content": TavilySearch(prompt)})

    # Generate response using Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    # Collect streaming response
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean response
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save chat log
    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    # Remove last system search message
    SystemChatBot.pop()

    return AnswerModifier(Answer=Answer)

# Main entry point
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))