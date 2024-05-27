import numpy as np

import dotenv
import os
dotenv.load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_SIZE = 1536

COMPLETION_MODEL = "gpt-3.5-turbo"

# Placeholder for OpenAI API key

def generate_embedding_for_text(text):
    """
    Generates an embedding for the given text.
    Placeholder for actual embedding generation logic.
    """
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def generate_tags_for_text(text):
    """
    Generates a list of tags for the given text using GPT-3.
    """
    try:
        # prompt instructions
        instructions = "Given the following **Document**, generate a list of tags that describe the content. "\
            "Each tag should be a word or phrase that is a topic, subject, or keyword of the text. "\
            "You must include a tag on each line with no further markup.\n\n"\
            f"# **Document**:\n{text}"
        message_list = [
            {
                "role": "system",
                "content": instructions
            }
        ]
        # llm call
        response = client.chat.completions.create(
            model=COMPLETION_MODEL,  # Specify the GPT-3 model
            messages=message_list,
            temperature=0.1
        )
        content = response.choices[0].message.content
        return [_format_tag(tag) for tag in content.strip().split('\n')]
    except Exception as e:
        print(f"An error occurred while generating tags with GPT-3: {e}")
        return []

def _format_tag(tag):
    tag = tag.lower().strip()
    if tag[:2] == "- ":
        return tag[2:]
    return tag