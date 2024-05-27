'''
Using the ChatGPT API for morphological analysis of tokens
'''

import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a pithy Ancient Greek morphological analysis machine, skilled in separating the prefix from the rest of the word. E.g., given the prompt 'προσβαλοῦσα' you return only 'προσ-βαλοῦσα' If there is no prefix, as ἤνεγκα, you return the word as is. NB: You cannot add any other characters than hyphen (-)"},
    {"role": "user", "content": "συμφέρον"}
  ]
)

print(completion.choices[0].message)