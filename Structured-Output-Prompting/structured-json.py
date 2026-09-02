import ollama
import json

prompt = """
Return ONLY valid JSON.

Topic: Python

Include these fields:
- language
- creator
- year
"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])