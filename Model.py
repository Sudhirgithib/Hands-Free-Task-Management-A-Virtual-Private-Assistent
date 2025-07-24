from typing import List


class FirstLayerDMM:
    def __init__(self):
        self.funcs = [
            "exit", "general", "realtime", "open", "close", "play",
            "generate image", "system", "content", "google search",
            "youtube search", "reminder"
        ]
        self.command_keywords = {
            "exit": ["bye", "goodbye", "exit", "stop", "quit"],
            "open": ["open", "launch"],
            "close": ["close", "terminate"],
            "play": ["play", "start playing"],
            "generate image": ["generate image", "create image", "draw"],
            "google search": ["search on google", "google"],
            "youtube search": ["search on youtube", "youtube"],
            "reminder": ["remind", "reminder"],
            "system": ["shutdown", "restart", "log off"],
            "realtime": ["weather", "news", "time", "date", "current", "today"],
        }

    def process(self, prompt: str) -> List[str]:
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in self.command_keywords["exit"]):
            return ["exit"]

        matched = []

        for command, keywords in self.command_keywords.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    matched.append(f"{command} ({prompt})")
                    break

        if not matched:
            return [f"general ({prompt})"]

        return matched


# CLI-based test if running standalone
if __name__ == "__main__":
    model = FirstLayerDMM()

    while True:
        user_input = input("Enter your query (or 'quit' to stop): ")
        if user_input.strip().lower() in ["quit", "exit"]:
            print("Exiting test.")
            break
        result = model.process(user_input)
        print("Processed Result:", result)
