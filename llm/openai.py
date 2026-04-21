from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client=OpenAI()


def openai(prompt: str):
    stream=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        stream=True # to stream requests
    )

    return stream