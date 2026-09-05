# Function Calling and Tool Integration

A practical example of connecting a Large Language Model (LLM) with external tools using **LangChain** and **Google Gemini**.

This project demonstrates how an LLM can understand a user's request, decide which tool is needed, call that tool through the application, receive the result, and then generate a final response using the retrieved information.

---

## Overview

A normal LLM can generate text based on the information available to it.

However, real-world AI applications often need to interact with external systems such as:

- Search engines
- APIs
- Databases
- Calculators
- File systems
- Internal application functions
- Weather services
- Business tools

**Function calling** allows an LLM to request the execution of a specific function when it needs additional information or needs to perform an operation.

This project demonstrates that workflow using three tools:

1. **DuckDuckGo Search** — searches the web
2. **Wikipedia API** — retrieves information from Wikipedia
3. **Personal Information Tool** — retrieves information from a local Python dictionary

The LLM used in this project is **Google Gemini**.

---

## How It Works

The basic workflow is:

```text
User Query
     |
     v
+----------------+
|  Google Gemini |
|      LLM       |
+-------+--------+
        |
        | Decide which tool(s) are required
        v
+-----------------------+
|      Tool Calls       |
+-----------+-----------+
            |
      +-----+-----+----------------+
      |           |                |
      v           v                v
 DuckDuckGo   Wikipedia      Personal Info
   Search       API              Tool
      |           |                |
      +-----------+----------------+
                  |
                  v
             Tool Results
                  |
                  v
          +---------------+
          | Google Gemini |
          +-------+-------+
                  |
                  v
            Final Answer
```

The important idea is that **the LLM does not directly execute Python functions**.

Instead:

1. The LLM decides which tool is needed.
2. It generates a structured tool call.
3. The Python application receives the tool call.
4. The application executes the corresponding function.
5. The result is returned to the LLM.
6. The LLM generates the final response.

---

# Function Calling

## What is Function Calling?

Function calling is a mechanism that allows an LLM to request a function with specific arguments.

For example, suppose the user asks:

```text
Tell me about Alice.
```

Gemini may determine that the `personal_info` tool is appropriate.

Conceptually, the model generates something similar to:

```json
{
  "name": "personal_info",
  "args": {
    "name": "Alice"
  }
}
```

The Python application then executes:

```python
personal_info("Alice")
```

The function returns:

```text
Alice is a software engineer with 5 years of experience in AI.
```

That result is then sent back to Gemini.

Gemini can finally generate:

```text
Alice is a software engineer with 5 years of experience in AI.
```

---

# Why Function Calling is Useful

Without tools:

```text
User
 |
 v
LLM
 |
 v
Answer
```

With tools:

```text
User
 |
 v
LLM
 |
 v
Tool Selection
 |
 v
External Tool
 |
 v
Tool Result
 |
 v
LLM
 |
 v
Final Answer
```

This allows AI applications to go beyond simple text generation.

For example:

```text
LLM
 |
 +---- Search the web
 |
 +---- Query a database
 |
 +---- Call an API
 |
 +---- Calculate something
 |
 +---- Retrieve company information
 |
 +---- Read a document
 |
 +---- Execute an application function
```

---

# Tools Included

## 1. DuckDuckGo Search

The first tool provides web search functionality.

It uses LangChain's:

```python
DuckDuckGoSearchRun
```

The tool is exposed to Gemini using:

```python
@tool("duckduckgo")
def duckduckgo(query: str) -> str:
```

For example:

```text
Search DuckDuckGo for the latest news about Geoffrey Hinton.
```

Gemini can decide to use:

```text
duckduckgo
```

The search results are then returned to the model.

---

## 2. Wikipedia API

The second tool communicates directly with the Wikipedia API.

The API endpoint used is:

```text
https://en.wikipedia.org/w/api.php
```

The custom LangChain tool is:

```python
@tool
def wiki_tool(query: str) -> str:
```

It accepts a search query and sends an HTTP request using Python's `requests` library.

Example:

```text
Search Wikipedia for Geoffrey Hinton's biography.
```

Gemini can select:

```text
wiki_tool
```

The Wikipedia response is then returned to Gemini.

---

## 3. Personal Information Tool

The third tool is a custom Python function.

It contains predefined information:

```python
info = {
    "Alice":
        "Alice is a software engineer with 5 years of experience in AI.",

    "Bob":
        "Bob is a data scientist who loves working with large datasets.",

    "Charlie":
        "Charlie is a product manager with a background in tech."
}
```

The function is exposed to Gemini using:

```python
@tool
def personal_info(name: str) -> str:
```

For example:

```text
Tell me about Alice.
```

Gemini can select:

```text
personal_info
```

The application executes:

```python
personal_info("Alice")
```

---

# Multiple Tool Calling

One of the useful parts of this project is that the LLM can work with multiple tools in a single workflow.

For example, the application sends:

```text
Tell me about Alice using the personal information tool.

Search Wikipedia for Geoffrey Hinton's biography.

Search DuckDuckGo for the latest news about Geoffrey Hinton.

Combine everything into a single response.
```

This request requires three different sources.

The model can generate tool calls for:

```text
personal_info
wiki_tool
duckduckgo
```

The application executes each requested tool and collects the results.

The results are then sent back to Gemini.

```text
                    User
                     |
                     v
                  Gemini
                     |
        +------------+------------+
        |            |            |
        v            v            v
 personal_info   wiki_tool    duckduckgo
        |            |            |
        v            v            v
     Result       Result       Result
        |            |            |
        +------------+------------+
                     |
                     v
                  Gemini
                     |
                     v
               Final Answer
```

---

# Project Structure

```text
Function-Calling-and-Tool-Integration/
│
├── main.py
├── README.md
└── .gitignore
```

For local development, you will also have:

```text
.env
```

So your local structure will be:

```text
Function-Calling-and-Tool-Integration/
│
├── main.py
├── README.md
├── .gitignore
└── .env
```

The `.env` file should **not** be pushed to GitHub.

---

# Requirements

You need:

- Python 3.10+
- Google Gemini API key
- Internet connection
- LangChain
- Google GenAI integration
- DuckDuckGo search package

---

# Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd building-agentic-ai-systems/Function-Calling-and-Tool-Integration
```

Install the dependencies:

```bash
python -m pip install langchain langchain-community langchain-google-genai python-dotenv requests duckduckgo-search
```

---

# Verify Installation

You can check the installed packages using:

```bash
python -m pip show langchain langchain-community langchain-google-genai python-dotenv requests duckduckgo-search
```

If all packages are installed, Python will display their package information.

---

# Google Gemini API Key

This project uses Google Gemini, so you need a Google API key.

Create a file named:

```text
.env
```

Add:

```text
GOOGLE_API_KEY=your_google_api_key_here
```

For example:

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

Do not put the API key directly inside `main.py`.

---

# Environment Variables

The project uses `python-dotenv` to load the API key.

The code:

```python
from dotenv import load_dotenv

load_dotenv()
```

loads the variables from `.env`.

The key is then accessed using:

```python
os.environ.get("GOOGLE_API_KEY")
```

---

# Security

Never commit your API key to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
.env.*
```

A recommended `.gitignore` is:

```gitignore
# Environment variables
.env
.env.*

# Python cache
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/
env/

# IDE settings
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints/

# Logs
*.log

# Temporary files
*.tmp
*.temp

# OS files
.DS_Store
Thumbs.db
```

The GitHub repository should contain:

```text
main.py
README.md
.gitignore
```

but not:

```text
.env
```

---

# Running the Project

After installing the dependencies and configuring the API key, run:

```bash
python main.py
```

You should see output similar to:

```text
Google API Key is set.
Gemini model loaded successfully!
DuckDuckGo tool created successfully!
Wikipedia tool created successfully!
Personal information tool created successfully!
All tools created successfully!
Tools successfully bound to Gemini!
```

---

# Understanding the Code

## 1. Loading the API Key

```python
load_dotenv()

if os.environ.get("GOOGLE_API_KEY"):
    print("Google API Key is set.")
else:
    print("Google API Key is NOT set.")
    exit()
```

This loads and verifies the Google API key.

---

## 2. Initializing Gemini

```python
llm = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai"
)
```

This creates the Gemini LLM used by the application.

---

## 3. Creating Tools

Tools are created using LangChain's `@tool` decorator.

Example:

```python
@tool
def personal_info(name: str) -> str:
    ...
```

The decorator provides the LLM with information about the function and its input.

The function's name and description help Gemini understand when the tool should be used.

---

## 4. Registering the Tools

All tools are stored in a list:

```python
tools = [
    duckduckgo,
    wiki_tool,
    personal_info
]
```

This list represents the capabilities available to Gemini.

---

## 5. Binding Tools to Gemini

The tools are connected to the model:

```python
llm_with_tools = llm.bind_tools(tools)
```

After this step, Gemini knows which tools are available.

---

## 6. Sending the User Query

The application sends the user request:

```python
response = llm_with_tools.invoke(user_query)
```

Gemini analyzes the request.

It can decide:

```text
I need personal_info
I need wiki_tool
I need duckduckgo
```

---

## 7. Reading Tool Calls

Tool calls can be accessed using:

```python
response.tool_calls
```

This provides the application with the tools Gemini wants to use.

Conceptually:

```text
Tool Name
    +
Arguments
    +
Tool Call ID
```

---

## 8. Finding the Correct Tool

The application creates a dictionary:

```python
tool_dict = {
    tool.name: tool
    for tool in tools
}
```

This makes it possible to map a tool name to the actual Python function.

For example:

```text
"personal_info" → personal_info function

"wiki_tool" → wiki_tool function

"duckduckgo" → duckduckgo function
```

---

## 9. Executing the Tool

The application loops through the requested tools:

```python
for tool_call in response.tool_calls:
```

Then finds the corresponding function:

```python
selected_tool = tool_dict[tool_call["name"]]
```

And executes it:

```python
tool_result = selected_tool.invoke(
    tool_call["args"]
)
```

This is the point where the actual Python function is executed.

---

## 10. Returning Tool Results

The result is converted into a `ToolMessage`:

```python
tool_messages.append(
    ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"]
    )
)
```

This connects the result to the original tool call.

---

## 11. Sending Results Back to Gemini

The original request, Gemini's tool call, and the tool results are combined:

```python
messages = [
    HumanMessage(content=user_query),
    response,
    *tool_messages
]
```

They are then sent back to Gemini:

```python
final_response = llm_with_tools.invoke(messages)
```

Gemini uses these results to generate the final response.

---

# The Complete Tool-Calling Loop

The most important part of the project is this loop:

```text
1. User sends query
          |
          v
2. Gemini analyzes query
          |
          v
3. Gemini selects tool
          |
          v
4. Gemini creates tool call
          |
          v
5. Python receives tool call
          |
          v
6. Python executes tool
          |
          v
7. Tool returns result
          |
          v
8. Python sends result to Gemini
          |
          v
9. Gemini generates final response
```

This is the foundation of many tool-using AI agents.

---

# Example

Suppose the user asks:

```text
Tell me about Alice.
```

Gemini can identify:

```text
Tool: personal_info

Arguments:
name = Alice
```

The application executes:

```python
personal_info("Alice")
```

The result is:

```text
Alice is a software engineer with 5 years of experience in AI.
```

The result is returned to Gemini.

Gemini can then generate the final answer.

---

# Another Example

User:

```text
Search Wikipedia for Geoffrey Hinton's biography.
```

Gemini can select:

```text
wiki_tool
```

The application executes:

```python
wiki_tool("Geoffrey Hinton biography")
```

The Wikipedia API returns search results.

Those results are provided to Gemini.

---

# Multi-Tool Example

User:

```text
Tell me about Alice.

Search Wikipedia for Geoffrey Hinton's biography.

Search DuckDuckGo for the latest news about Geoffrey Hinton.

Combine everything into a single response.
```

Possible tool calls:

```text
personal_info("Alice")

wiki_tool("Geoffrey Hinton biography")

duckduckgo("latest news about Geoffrey Hinton")
```

The application executes all required tools.

The results are combined and passed back to Gemini.

---

# Why LangChain?

LangChain provides useful abstractions for connecting LLMs with tools.

In this project, LangChain is used for:

- Initializing the model
- Creating tools
- Binding tools
- Invoking the model
- Managing messages
- Handling tool calls
- Passing tool results back to the model

Without a framework, developers would need to implement more of this orchestration manually.

---

# Why Google Gemini?

Google Gemini provides tool/function calling capabilities that allow the model to produce structured requests for available tools.

In this project, Gemini is responsible for:

```text
Understanding the user request
          |
          v
Determining required tools
          |
          v
Generating tool calls
          |
          v
Using returned tool results
          |
          v
Generating the final response
```

---

# External Tools vs Custom Tools

This project demonstrates both.

## External Tools

These communicate with external services:

```text
DuckDuckGo
Wikipedia API
```

## Custom Tool

This is implemented directly in Python:

```text
Personal Information
```

This distinction is important because real AI applications often combine external APIs with internal application functions.

For example:

```text
LLM Agent
    |
    +---- Web Search
    |
    +---- Company Database
    |
    +---- Internal API
    |
    +---- Calculator
    |
    +---- File Search
```

---

# Adding Your Own Tool

You can create another tool using LangChain's `@tool` decorator.

For example:

```python
@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    """
    return str(eval(expression))
```

Then add it to the tools list:

```python
tools = [
    duckduckgo,
    wiki_tool,
    personal_info,
    calculator
]
```

And bind the updated list:

```python
llm_with_tools = llm.bind_tools(tools)
```

The LLM can then potentially select the calculator when a mathematical operation is requested.

> In production applications, avoid using unrestricted `eval()` for user-controlled input. Use a safe expression parser or dedicated calculator library instead.

---

# Designing Good Tools

A good tool should have:

### 1. Clear Name

Good:

```text
search_wikipedia
```

Less descriptive:

```text
tool1
```

### 2. Clear Description

For example:

```python
"""
Search Wikipedia for information about a topic.
"""
```

### 3. Well-Defined Arguments

For example:

```python
def wiki_tool(query: str) -> str:
```

The type annotation tells the model that the function expects a string.

### 4. Predictable Output

Tools should return useful and understandable results.

---

# Tool Calling vs RAG

Function calling and RAG are related concepts, but they solve different problems.

## RAG

RAG retrieves relevant information from a knowledge source:

```text
Document
   |
   v
Embeddings
   |
   v
Vector Database
   |
   v
Relevant Context
   |
   v
LLM
```

Your repository's RAG project demonstrates this approach.

## Function Calling

Function calling allows the LLM to request an operation:

```text
User
 |
 v
LLM
 |
 v
Tool
 |
 v
Result
 |
 v
LLM
```

This project demonstrates function calling.

Together, these concepts can be used to build more capable AI agents.

---

# Potential Applications

Tool-enabled LLM applications can be used for:

### AI Assistants

```text
User
 |
 v
AI Assistant
 |
 +---- Search
 +---- Calendar
 +---- Email
 +---- Weather
 +---- Database
```

### Customer Support

```text
Customer
   |
   v
AI Agent
   |
   +---- Search Knowledge Base
   +---- Check Order
   +---- Check Account
   +---- Create Ticket
```

### Research Assistants

```text
Question
   |
   v
AI Research Agent
   |
   +---- Search Web
   +---- Search Wikipedia
   +---- Search Documents
   +---- Summarize
```

### Enterprise Agents

```text
AI Agent
   |
   +---- CRM
   +---- Database
   +---- Internal APIs
   +---- Documents
   +---- Search
```

---

# Limitations

This project is intended as a simple demonstration of tool calling.

Some limitations include:

- Search results depend on external services.
- External APIs can become unavailable.
- The LLM may occasionally choose an unexpected tool.
- Tool arguments should be validated in production.
- API requests can fail.
- Real-world agents require authentication and authorization.
- Sensitive tools should have strict access controls.
- Tool execution should not allow unrestricted arbitrary code execution.

---

# Security Considerations

When building real tool-enabled agents:

- Never expose API keys to the model.
- Never commit secrets to GitHub.
- Validate all tool arguments.
- Restrict access to sensitive tools.
- Use authentication for protected APIs.
- Apply rate limits.
- Log tool execution where appropriate.
- Avoid unrestricted code execution.
- Implement authorization before performing sensitive operations.

The tools in this project are intentionally simple for demonstration purposes.

---

# Troubleshooting

## `Google API Key is NOT set`

Check that `.env` exists:

```text
Function-Calling-and-Tool-Integration/
├── main.py
├── README.md
├── .gitignore
└── .env
```

The `.env` file should contain:

```text
GOOGLE_API_KEY=your_api_key
```

---

## `ModuleNotFoundError: No module named 'langchain'`

Install:

```bash
python -m pip install langchain
```

---

## `ModuleNotFoundError: No module named 'langchain_community'`

Install:

```bash
python -m pip install langchain-community
```

---

## `ModuleNotFoundError: No module named 'langchain_google_genai'`

Install:

```bash
python -m pip install langchain-google-genai
```

---

## `ModuleNotFoundError: No module named 'dotenv'`

Install:

```bash
python -m pip install python-dotenv
```

---

## `ModuleNotFoundError: No module named 'requests'`

Install:

```bash
python -m pip install requests
```

---

## DuckDuckGo Search Problems

Update the package:

```bash
python -m pip install -U duckduckgo-search
```

---

# Future Improvements

This project can be extended into a more complete AI agent.

Possible improvements include:

- Add a calculator tool
- Add weather API integration
- Add a database tool
- Add file/document search
- Add persistent memory
- Add conversation history
- Add multiple search providers
- Add structured tool outputs
- Add error handling and retries
- Add tool execution logging
- Add asynchronous tool execution
- Add human approval before sensitive actions
- Build a web interface
- Build a REST API
- Add automated tests

A more advanced architecture could look like:

```text
                       User
                        |
                        v
                 +-------------+
                 | AI Agent    |
                 |    LLM      |
                 +------+------+
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       Search       Database       Calculator
          |             |             |
          v             v             v
       Results        Results       Results
          |             |             |
          +-------------+-------------+
                        |
                        v
                   Agent / LLM
                        |
                        v
                   Final Answer
```

---

# Key Concepts Demonstrated

This project demonstrates the following concepts:

```text
LLM
 |
 +-- Function Calling
 |
 +-- Tool Calling
 |
 +-- Custom Tools
 |
 +-- External APIs
 |
 +-- Search Integration
 |
 +-- Tool Binding
 |
 +-- Tool Execution
 |
 +-- Tool Results
 |
 +-- Multi-Tool Workflows
 |
 +-- Agent Workflow
```

---

# Summary

The project demonstrates how to extend an LLM beyond simple text generation by connecting it to external tools.

The core workflow is:

```text
User Query
    |
    v
Gemini
    |
    v
Tool Selection
    |
    v
Tool Call
    |
    v
Python Application
    |
    v
External / Custom Tool
    |
    v
Tool Result
    |
    v
Gemini
    |
    v
Final Response
```

The three tools used in this implementation are:

| Tool | Purpose |
|---|---|
| `duckduckgo` | Web search |
| `wiki_tool` | Wikipedia search |
| `personal_info` | Local application data |

This provides a simple foundation for understanding how modern AI agents interact with external tools and services.

---

# Technologies

- Python
- LangChain
- Google Gemini
- LangChain Google GenAI
- DuckDuckGo Search
- Wikipedia API
- Requests
- Python Dotenv

---

## License

This project is intended for educational and experimental purposes.