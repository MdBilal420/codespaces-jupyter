from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(
    api_key=my_api_key
)


# our_first_message = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=1000,
#     messages=[
#         {"role": "user", "content": "Hi there! Please write me a joke about a pet chicken"}
#     ]
# )

# print(our_first_message)

### TRANSLATE
# word = "Hello, how are you?"
# language = "Spanish"

# translated = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=1000,
#     messages=[
#         {"role": "user", "content": f"Translate the following text to {language}: {word}. Only return the translated text, do not include any other information."}
#     ]
# )

# print(translated.content[0].text)

### FEW SHOT LEARNING

# response = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=500,
#     messages=[
#         {"role": "user", "content": "Unpopular opinion: Pickles are disgusting. Don't @ me"},
#         {"role": "assistant", "content": "NEGATIVE"},
#         {"role": "user", "content": "I think my love for pickles might be getting out of hand. I just bought a pickle-shaped pool float"},
#         {"role": "assistant", "content": "POSITIVE"},
#         {"role": "user", "content": "Seriously why would anyone ever eat a pickle?  Those things are nasty!"},
#         {"role": "assistant", "content": "NEGATIVE"},
#         {"role": "user", "content": "Just tried the new spicy pickles from @PickleCo, and my taste buds are doing a happy dance! 🌶️🥒 #pickleslove #spicyfood"},
#     ]
# )
# print(response.content[0].text)

# Chatbot + Streaming

conversation_history = []

while True:
    user_input = input("")
    conversation_history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=conversation_history,
        stream=True
    )

    print("R",response)
    response_text = ""
    for chunk in response:
        if chunk.type == "content_block_delta":
            response_text += chunk.delta.text
            print(chunk.delta.text, flush=True, end="")
    
    conversation_history.append({"role": "assistant", "content": response_text})
