from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(
    api_key=my_api_key
)

our_first_message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hi there! Please write me a joke about a pet chicken"}
    ]
)

print(our_first_message.content[0].text)