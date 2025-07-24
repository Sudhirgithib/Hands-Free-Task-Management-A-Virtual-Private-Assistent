import os
import time
import re
import mtranslate as mt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

# HTML for Speech Recognition
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start</button>
    <button id="end" onclick="stopRecognition()">Stop</button>
    <p id="output"></p>

    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + " ";
            }};

            recognition.onend = function() {{
                recognition.start();
            }};
            recognition.start();
        }}

        function stopRecognition() {{
            recognition.stop();
        }}
    </script>
</body>
</html>'''

# Setup Path
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

html_file_path = os.path.join(TempDirPath, "Voice.html")
status_file_path = os.path.join(TempDirPath, "Status.data")

with open(html_file_path, "w", encoding="utf-8") as file:
    file.write(HtmlCode)

# Selenium WebDriver Setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def SetAssistantStatus(Status):
    with open(status_file_path, "w", encoding="utf-8") as file:
        file.write(Status)

def QueryModifier(Query):
    Query = Query.strip().capitalize()
    Query = re.sub(r"\s+", " ", Query)
    if not Query.endswith(('.', '?', '!')):
        Query += "."
    words = Query.split()
    Query = " ".join(dict.fromkeys(words))
    return Query

def UniversalTranslator(Text):
    try:
        return QueryModifier(mt.translate(Text, "en", "auto"))
    except Exception as e:
        print(f"Translation error: {e}")
        return Text

def SpeechRecognition():
    driver.get("file:///" + html_file_path.replace("\\", "/"))
    driver.find_element(By.ID, "start").click()
    cache = set()

    try:
        while True:
            Text = driver.find_element(By.ID, "output").text.strip()
            if Text and Text not in cache:
                cache.add(Text)
                driver.find_element(By.ID, "end").click()
                if "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    return UniversalTranslator(Text)
            time.sleep(0.5)
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return None

if __name__ == "__main__":
    try:
        while True:
            Text = SpeechRecognition()
            if Text:
                print(f"Recognized: {Text}")
    except KeyboardInterrupt:
        print("\nExiting program.")
        driver.quit()
