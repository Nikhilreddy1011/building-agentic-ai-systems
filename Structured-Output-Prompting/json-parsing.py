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
    format="json",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

json_text = response["message"]["content"]

print("JSON returned by the model:")
print(json_text)

data = json.loads(json_text)

print("\nExtracted Values")
print("Language:", data["language"])
print("Creator:", data["creator"])
print("Year:", data["year"])