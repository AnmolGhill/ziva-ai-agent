import pygame  # Import pygame library for handling audio playback
import random  # Import random for generating random choices
import asyncio  # Import asyncio for asynchronous operations
import edge_tts  # Import edge_tts for text-to-speech functionality
import os  # Import os for file path handling
from dotenv import dotenv_values  # Import dotenv for reading environment variables

# Load environment variables from a .env file
env_vars = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
AssistantVoice = env_vars.get("AssistantVoice")  # Get the AssistantVoice

# Get the absolute path to the Data directory
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(current_dir), "Data")

# Asynchronous function to convert text to audio file
async def TextToAudioFile(text) -> None:
    file_path = os.path.join(data_dir, "speech.mp3")  # Path where speech file will be saved

    # Remove old file if exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate speech
    communicate = edge_tts.Communicate(
        text,
        AssistantVoice,
        pitch="+5Hz",
        rate="+13%"
    )

    await communicate.save(file_path)


# Function to manage TTS playback
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to audio
            asyncio.run(TextToAudioFile(Text))

            # Initialize audio
            pygame.mixer.init()

            # Load and play audio
            pygame.mixer.music.load(os.path.join(data_dir, "speech.mp3"))
            pygame.mixer.music.play()

            # Wait until playback ends
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)

            return True

        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in cleanup: {e}")


# Function to handle long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    responses = [
    "The rest of the result has been printed to the chat screen, kindly check it out sir.",
    "The rest of the text is now on the chat screen, sir, please check it.",
    "You can see the rest of the text on the chat screen, sir.",
    "The remaining part of the text is now on the chat screen, sir.",
    "Sir, you'll find more text on the chat screen for you to see.",
    "The rest of the answer is now on the chat screen, sir.",
    "Sir, please look at the chat screen, the rest of the answer is there.",
    "You'll find the complete answer on the chat screen, sir.",
    "The next part of the text is on the chat screen, sir.",
    "Sir, please check the chat screen for more information.",
    "There's more text on the chat screen for you, sir.",
    "Sir, take a look at the chat screen for additional text.",
    "You'll find more to read on the chat screen, sir.",
    "Sir, check the chat screen for the rest of the text.",
    "The chat screen has the rest of the text, sir.",
    "There's more to see on the chat screen, sir, please look.",
    "Sir, the chat screen holds the continuation of the text.",
    "You'll find the complete answer on the chat screen, kindly check it out sir.",
    "Please review the chat screen for the rest of the text, sir.",
    "Sir, look at the chat screen for the complete answer."
    ]

    # If text is long
    if len(Data) > 4 and len(Text) >= 250:
        TTS(".".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)


# Main execution
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))