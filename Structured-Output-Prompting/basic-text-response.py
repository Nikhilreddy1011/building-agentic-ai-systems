import ollama
response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

print(response["message"]["content"])