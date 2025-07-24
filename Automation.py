from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from tld import get_tld
from groq import Groq
import subprocess
import requests
import keyboard
import asyncio
import os
from pathlib import Path


class Automation:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.env_vars = dotenv_values(self.base_dir / ".env")
        self.groq_api_key = self.env_vars.get("GroqAPIKey")
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None

        self.classes = [
            "Zc7Cubf", "hgKElc", "LTT0o SYyric", "Z2LQvd",
            "gsrt vk_bk FzvWSb VwPmhf", "pcJeqe",
            "tw-Data-text tw-text-small tw-ta", "lzXerdc",
            "OSr6Id LTk0O", "VyY6d",
            "webanswers-webanswers_table__webanswers-table",
            "dD0No kHb4Bb gsrt", "sXLaOe", "lMFkHe",
            "vOFp3", "v3W9pe", "kno-resDesc", "SPZz6b"
        ]

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        self.data_dir = self.base_dir / "Data"
        self.data_dir.mkdir(exist_ok=True)

    async def execute_commands(self, commands: list[str]):
        results = []

        for command in commands:
            command = command.lower()

            if command.startswith("open "):
                app_name = command.replace("open ", "", 1)
                try:
                    appopen(app_name)
                    results.append(f"Opened {app_name}.")
                except Exception as e:
                    results.append(f"Failed to open {app_name}: {e}")

            elif command.startswith("close "):
                app_name = command.replace("close ", "", 1)
                try:
                    close(app_name)
                    results.append(f"Closed {app_name}.")
                except Exception as e:
                    results.append(f"Failed to close {app_name}: {e}")

            elif command.startswith("google search "):
                query = command.replace("google search ", "", 1)
                search(query)
                results.append(f"Searching Google for {query}.")

            elif command.startswith("youtube search "):
                query = command.replace("youtube search ", "", 1)
                playonyt(query)
                results.append(f"Playing {query} on YouTube.")

            elif command.startswith("content "):
                query = command.replace("content ", "", 1)
                result = await self.fetch_content(query)
                results.append(result)

            elif command.startswith("system shutdown"):
                os.system("shutdown /s /t 1")
                results.append("System is shutting down...")

            elif command.startswith("system restart"):
                os.system("shutdown /r /t 1")
                results.append("System is restarting...")

            elif command.startswith("system logout"):
                os.system("shutdown /l")
                results.append("Logging out...")

            else:
                results.append("Sorry, command not recognized!")

        return results

    async def fetch_content(self, query: str):
        try:
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            for class_name in self.classes:
                data = soup.find(class_=class_name)
                if data:
                    return data.text.strip()

            return "No relevant content found!"

        except Exception as e:
            return f"Error fetching content: {e}"
if __name__ == "__main__":
    import asyncio

    automation = Automation()

    while True:
        user_input = input("Enter command (or 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break
        if user_input:
            results = asyncio.run(automation.execute_commands([user_input]))
            for res in results:
                print(res)

