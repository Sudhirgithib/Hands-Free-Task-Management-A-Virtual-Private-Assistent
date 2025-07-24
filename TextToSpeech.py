from Backend.Chatbot import Chatbot
from Backend.Automation import Automation
from Backend.ImageGeneration import ImageGenerator
from Backend.SpeechRecognition import stt
from Backend.TextToSpeech import TextToSpeech

import time

def main():
    print(" Ask me anything! (Type 'exit' to quit)")
    bot = Chatbot()
    automation = Automation()

    while True:
        # Voice input
        query = stt()
        if not query:
            continue

        print(f"You: {query}")

        if query.lower() == "exit":
            print("JARVIS: Goodbye!")
            break

        # Handle image generation
        elif "generate image of" in query.lower():
            prompt = query.lower().split("generate image of")[-1].strip()
            if prompt:
                print(f"JARVIS: Generating image for '{prompt}'...")
                result = generate_image(prompt)
                print("JARVIS:", result)
                TextToSpeech(f"Image generated for {prompt}")
            else:
                print("JARVIS: Please provide a prompt for image generation.")
                TextToSpeech("Please provide a prompt for image generation.")

        # Handle automation
        elif automation.can_handle(query):
            result = automation.handle(query)
            print("JARVIS:", result)
            TextToSpeech(result)

        # Chatbot response
        else:
            response = bot.get_response(query)
            print("JARVIS:", response)
            TextToSpeech(response)

        time.sleep(1)

if __name__ == "__main__":
    main()
