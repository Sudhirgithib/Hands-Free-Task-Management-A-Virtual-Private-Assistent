from Backend.Chatbot import Chatbot
from Backend.Model import FirstLayerDMM
from Backend.Automation import Automation
from Backend.ImageGeneration import ImageGenerator
from Backend.SpeechToText import stt

from Backend.TextToSpeech import TextToSpeech

if __name__ == "__main__":
    chatbot = Chatbot()
    model = FirstLayerDMM()
    automation = Automation()

    try:
        while True:
            Text = SpeechRecognition()  # ✅ Correct usage
            if Text:
                print(f"You said: {Text}")
                response, task = model.decide_task(Text)

                if task == "chat":
                    reply = chatbot.get_response(Text)
                    print("JARVIS:", reply)
                    TextToSpeech(reply)

                elif task == "image":
                    result = ImageGenerator(Text)
                    print("Image Generated:", result)
                    TextToSpeech("Your image has been generated successfully.")

                elif task == "automation":
                    result = automation.handle_command(Text)
                    print("Automation Result:", result)
                    TextToSpeech(result)

                else:
                    print("Sorry, I couldn't understand that.")
                    TextToSpeech("Sorry, I couldn't understand that.")
    except KeyboardInterrupt:
        print("\nJARVIS shutting down.")
