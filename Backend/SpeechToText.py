from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace language dynamically
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), "Data")
voice_html_path = os.path.join(data_dir, "Voice.html")

# Save HTML file
with open(voice_html_path, "w") as f:
    f.write(HtmlCode)

# Get working directory (project root)
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Link = voice_html_path

# Setup Chrome options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Temporary path
TempDirPath = os.path.join(current_dir, "Frontend", "Files")

# Save assistant status
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

# Modify query formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()

    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom",
                      "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

# Translate to English
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Speech recognition function
def SpeechRecognition():
    driver.get("file:///" + Link)
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                driver.find_element(by=By.ID, value="end").click()

                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

        except Exception:
            pass

# Main execution
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)