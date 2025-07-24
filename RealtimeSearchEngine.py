import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("E:/Desktop/MINI-PROJECT/Backend/.env")

class Chatbot:
    def __init__(self):
        self.api_key = os.getenv("CohereAPIKey")
        self.client = cohere.Client(self.api_key)
        self.chat_history = []

    def get_response(self, query):
        try:
            response = self.client.chat(
                message=query,
                temperature=0.7,
                chat_history=self.chat_history
            )
            reply = response.text.strip()
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": reply})
            print(f"JARVIS: {reply}")
            return reply
        except Exception as e:
            print(f"JARVIS: Sorry, I'm currently unable to generate a response. Please try again shortly.")
            print(f"[ERROR]: {e}")
            return "Sorry, I'm currently unable to generate a response. Please try again shortly."

if __name__ == "__main__":
    bot = Chatbot()
    print("JARVIS Activated. Ask me anything! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("JARVIS: Goodbye!")
            break
        bot.get_response(user_input)
