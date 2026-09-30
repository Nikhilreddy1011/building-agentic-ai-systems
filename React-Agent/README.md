# ReAct Agent with Ollama and Tool Calling

A practical implementation of a **ReAct (Reasoning + Acting) Agent** using **LangChain**, **LangGraph**, and a locally running **Ollama Llama 3.2** model.

This project demonstrates how a single AI agent can understand a user's request, decide whether a tool is required, call the appropriate tool, use the returned result, and produce a final response.

## Experiment Name

**ReAct System Design**

## 1. What is a ReAct Agent?

**ReAct** stands for **Reasoning + Acting**.

A ReAct agent combines an LLM's reasoning capability with actions performed through tools.

```text
User Query
    |
    v
+------------------+
|      LLM         |
|   Llama 3.2      |
+--------+---------+
         |
         | Analyze request
         v
+------------------+
| Decide whether   |
| a tool is needed |
+--------+---------+
         |
         v
+---------------------------+
|        Tool Selection     |
+-------------+-------------+
              |
       +------+------+
       |             |
       v             v
 Calculator     Word Counter
       |             |
       +------+------+
              |
              v
        Tool Result
              |
              v
        +-----------+
        |    LLM    |
        +-----+-----+
              |
              v
         Final Answer
```

The important idea is that the LLM does not directly execute the Python functions. The agent framework coordinates the interaction:

1. User sends a request.
2. LLM analyzes the request.
3. Agent determines whether a tool is useful.
4. LLM produces a tool call when required.
5. Python tool is executed.
6. Tool returns its result.
7. Result is provided back to the agent.
8. LLM generates the final answer.

## 2. Why Use a ReAct Agent?

A normal LLM can generate text, but an agent can also interact with application tools.

For example:

```text
Calculate (345 + 678) * 23
```

can be handled by the calculator tool.

Similarly:

```text
Count the words in "Artificial Intelligence is transforming education."
```

can be handled by the word-counter tool.

The architecture is:

```text
LLM
 |
 +---- Calculator
 |
 +---- Word Counter
 |
 +---- Future tools
```

## 3. Technologies Used

- Python
- LangChain
- LangGraph
- LangChain Ollama
- Ollama
- Llama 3.2
- LangChain Tools

## 4. Project Architecture

```text
                         USER
                           |
                           v
                  +----------------+
                  |  ReAct Agent   |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Llama 3.2 LLM  |
                  |    Ollama      |
                  +-------+--------+
                          |
                   Decide on action
                          |
              +-----------+-----------+
              |                       |
              v                       v
      +---------------+       +---------------+
      |  Calculator   |       | Word Counter  |
      +-------+-------+       +-------+-------+
              |                       |
              +-----------+-----------+
                          |
                          v
                    Tool Results
                          |
                          v
                  +----------------+
                  |  ReAct Agent   |
                  +-------+--------+
                          |
                          v
                     FINAL ANSWER
```

## 5. Project Structure

```text
React-Agent/
│
├── main.py
├── README.md
└── .gitignore
```

## 6. Requirements

You need:

- Python 3.10+
- Ollama
- Llama 3.2
- LangChain
- LangGraph
- LangChain Ollama integration

Install:

```bash
python -m pip install langchain langchain-core langgraph langchain-ollama
```

## 7. Ollama Setup

Check the installed models:

```powershell
ollama list
```

The project expects:

```text
llama3.2:latest
```

If it is not installed:

```powershell
ollama pull llama3.2
```

Start the Ollama server:

```powershell
ollama serve
```

The server should report:

```text
Listening on 127.0.0.1:11434
```

Keep that terminal running while executing the Python program.

## 8. Loading the LLM

The code uses:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)
```

`ChatOllama` connects LangChain to the local Ollama server.

The model is `llama3.2:latest`.

`temperature=0` makes responses more deterministic.

## 9. Creating Tools

The program imports:

```python
from langchain_core.tools import tool
```

The `@tool` decorator exposes a Python function as a tool that the agent can use.

This project contains two tools:

```text
calculator
word_counter
```

## 10. Calculator Tool

```python
@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return str(e)
```

The calculator receives an expression such as:

```text
2345 * 789
```

and returns the calculated result.

The `try/except` prevents a calculation error from immediately terminating the program.

### Security Note

This educational implementation uses:

```python
eval(expression)
```

Unrestricted `eval()` should not be exposed to arbitrary user input in production. A safe expression parser or calculator library should be used instead.

## 11. Word Counter Tool

```python
@tool
def word_counter(text: str) -> str:
    """
    Count the number of words in a text.
    """

    return f"Total words = {len(text.split())}"
```

For:

```text
Artificial Intelligence is transforming education.
```

the tool splits the text into words and returns:

```text
Total words = 5
```

## 12. Registering the Tools

The tools are stored in:

```python
tools = [
    calculator,
    word_counter
]
```

These are the capabilities available to the agent.

## 13. Creating the ReAct Agent

The code uses:

```python
from langgraph.prebuilt import create_react_agent
```

and:

```python
agent = create_react_agent(
    llm,
    tools
)
```

This connects the Llama 3.2 model with the calculator and word-counter tools.

The agent can now determine which available tool is relevant to a request.

## 14. How the Agent Solves a Query

Suppose the user asks:

```text
What is 2345 * 789?
```

The conceptual workflow is:

```text
User
 |
 v
"What is 2345 * 789?"
 |
 v
ReAct Agent
 |
 v
Llama 3.2 analyzes request
 |
 v
Mathematical operation detected
 |
 v
Select calculator
 |
 v
calculator("2345 * 789")
 |
 v
Tool returns result
 |
 v
LLM generates final answer
 |
 v
User
```

The application does not manually decide which tool to use. The agent has access to the tools and can select an appropriate one.

## 15. Test 1 — Calculator

The code sends:

```python
response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "What is 2345 * 789?"
            )
        ]
    }
)
```

The agent can select `calculator`.

The calculator evaluates:

```text
2345 * 789
```

which produces:

```text
1850155
```

The final response is retrieved using:

```python
response["messages"][-1].content
```

## 16. Test 2 — Word Counter

The second test sends:

```text
Count the words in 'Artificial Intelligence is transforming education.'
```

The agent recognizes this as a word-counting task and can select:

```text
word_counter
```

The tool executes:

```python
len(text.split())
```

and returns:

```text
Total words = 5
```

## 17. Test 3 — Multiple Tools

The third query is:

```text
Calculate 123 * 45 and count the words in
'Artificial Intelligence is transforming the world'
```

This contains two tasks:

```text
Task 1 -> Mathematical calculation
Task 2 -> Word counting
```

The workflow can be represented as:

```text
                  User
                   |
                   v
              ReAct Agent
                   |
          +--------+--------+
          |                 |
          v                 v
     calculator        word_counter
          |                 |
          v                 v
       5535             Total words = 7
          |                 |
          +--------+--------+
                   |
                   v
              Final Answer
```

This demonstrates that one agent can coordinate multiple tools in a single request.

## 18. ReAct Process Demonstration

The code also streams the agent:

```python
for event in agent.stream(
    {
        "messages": [
            (
                "user",
                "Calculate (345 + 678) * 23"
            )
        ]
    },
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
```

The expression is:

```text
(345 + 678) * 23
```

First:

```text
345 + 678 = 1023
```

Then:

```text
1023 * 23 = 23529
```

So the calculator can return:

```text
23529
```

Streaming displays agent events as the workflow progresses.

## 19. What Happens Internally?

For:

```text
Calculate (345 + 678) * 23
```

the conceptual sequence is:

```text
1. User sends query
          |
          v
2. ReAct Agent receives query
          |
          v
3. LLM analyzes request
          |
          v
4. Agent determines calculation is required
          |
          v
5. Calculator tool is selected
          |
          v
6. Calculator executes expression
          |
          v
7. Tool returns 23529
          |
          v
8. Agent receives tool result
          |
          v
9. LLM generates final answer
          |
          v
10. User receives answer
```

## 20. Interactive ReAct Agent

After the predefined tests, the program starts:

```text
======================================
       INTERACTIVE REACT AGENT
======================================
Type 'exit' to stop.
```

The program reads:

```python
question = input("You : ")
```

and sends the question to the agent.

The loop continues until:

```text
exit
```

is entered.

Example:

```text
You : What is 25 * 40?

Agent : 1000
```

## 21. Interactive Workflow

```text
              START
                |
                v
       Ask user for question
                |
                v
          Is it "exit"?
          /          \
        YES           NO
        |              |
        v              v
      STOP        Send to agent
                       |
                       v
                  LLM analyzes
                       |
                       v
                Select tool
                       |
                       v
                 Execute tool
                       |
                       v
                Get tool result
                       |
                       v
                Generate answer
                       |
                       v
                 Show answer
                       |
                       v
              Ask next question
```

## 22. Error Handling

The interactive section uses:

```python
try:
    response = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    print("\nAgent :", response["messages"][-1].content)

except Exception as e:
    print("\nError:", e)
```

If an exception occurs, the error is displayed and the interactive loop can continue.

## 23. What Makes This a Single Agent?

There is one agent:

```python
agent = create_react_agent(
    llm,
    tools
)
```

That single agent has multiple capabilities:

```text
Single Agent
 |
 +---- Calculator
 |
 +---- Word Counter
```

This differs from a multi-agent architecture, where several specialized agents communicate with each other.

## 24. Agent vs Tool

A **tool** performs a specific operation:

```text
calculator -> performs calculations
word_counter -> counts words
```

The **agent** decides when those capabilities are useful:

```text
Agent
 |
 +---- decide -> calculator
 |
 +---- decide -> word_counter
```

Therefore:

```text
Tool  = performs an operation
Agent = decides how/when to use available capabilities
```

## 25. Tool Selection Examples

| User Request | Appropriate Tool |
|---|---|
| `What is 45 * 20?` | `calculator` |
| `Calculate (10 + 5) * 2` | `calculator` |
| `Count the words in "Hello world"` | `word_counter` |
| `How many words are in this sentence?` | `word_counter` |
| `Calculate 10 * 20 and count these words` | Both tools |

## 26. Why Tool Descriptions Matter

The calculator has the description:

```text
Evaluate a mathematical expression.
```

The word counter has:

```text
Count the number of words in a text.
```

These descriptions help the agent understand the purpose of each tool.

Clear names, descriptions, and argument types make tool selection more reliable.

## 27. Complete Agent Workflow

```text
                         USER
                           |
                           v
                    User Query
                           |
                           v
                  +----------------+
                  |  ReAct Agent   |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  | Llama 3.2 LLM  |
                  |    Ollama      |
                  +-------+--------+
                          |
                          v
                   Analyze Request
                          |
                          v
                    Select Tool(s)
                          |
             +------------+------------+
             |                         |
             v                         v
       Calculator                Word Counter
             |                         |
             v                         v
       Mathematical                Word Count
          Result                     Result
             |                         |
             +------------+------------+
                          |
                          v
                    Tool Result(s)
                          |
                          v
                    ReAct Agent
                          |
                          v
                   Final Response
                          |
                          v
                         USER
```

## 28. Running the Project

Start Ollama first:

```powershell
ollama serve
```

Then open another terminal:

```powershell
cd "C:\Users\nikhi\Desktop\building-agentic-ai-systems\React-Agent"
```

Run:

```powershell
python main.py
```

Expected startup messages:

```text
LLM Loaded Successfully
Tools Loaded Successfully
ReAct Agent Created Successfully
```

## 29. Troubleshooting

### Ollama Connection Error

If you see:

```text
WinError 10061
No connection could be made because the target machine actively refused it
```

start Ollama:

```powershell
ollama serve
```

Verify:

```text
Listening on 127.0.0.1:11434
```

### Model Not Found

Check:

```powershell
ollama list
```

If necessary:

```powershell
ollama pull llama3.2
```

### Missing Python Package

For example:

```powershell
python -m pip install langchain-ollama
```

or:

```powershell
python -m pip install langgraph
```

## 30. Limitations

This is an educational implementation.

Limitations include:

- Calculator uses unrestricted `eval()`.
- The LLM may occasionally select an unexpected tool.
- Tool arguments should be validated in production.
- Ollama must be running locally.
- Llama 3.2 performance depends on available hardware.
- There is no persistent memory.
- There is no database integration.
- There is no authentication or authorization layer.
- There is no human approval mechanism for sensitive actions.
- The current agent has only two tools.

## 31. Future Improvements

Possible extensions:

```text
ReAct Agent
 |
 +---- Calculator
 |
 +---- Word Counter
 |
 +---- Web Search
 |
 +---- Wikipedia
 |
 +---- Weather API
 |
 +---- Database
 |
 +---- File Search
 |
 +---- RAG
 |
 +---- REST API
```

Other improvements include:

- Replace `eval()` with a safe calculator.
- Add structured tool outputs.
- Add persistent conversation memory.
- Add tool execution logging.
- Add retries.
- Add asynchronous tool execution.
- Add a web interface.
- Add FastAPI integration.
- Add authentication and authorization.
- Add human approval for sensitive actions.
- Add automated tests.
- Add evaluation and benchmarking.

## 32. ReAct vs Function Calling

**Function calling** allows an LLM to request a specific function:

```text
User
 |
 v
LLM
 |
 v
Tool Call
 |
 v
Python Function
 |
 v
Tool Result
 |
 v
LLM
```

A **ReAct agent** manages an action-oriented workflow:

```text
User
 |
 v
Agent
 |
 v
LLM
 |
 v
Decide Action
 |
 v
Tool
 |
 v
Observation / Result
 |
 v
Agent / LLM
 |
 v
Final Answer
```

This project uses:

```python
create_react_agent(...)
```

to implement the ReAct-style workflow.

> **Note:** Depending on the installed LangGraph/LangChain version, you may see a deprecation warning for `create_react_agent`. That warning concerns the API version, not the ReAct concept demonstrated by this experiment.

## 33. Key Concepts Demonstrated

```text
Python
 |
 +-- Local LLM
 |
 +-- Ollama
 |
 +-- Llama 3.2
 |
 +-- LangChain
 |
 +-- LangGraph
 |
 +-- ReAct Agent
 |
 +-- Custom Tools
 |
 +-- Tool Selection
 |
 +-- Tool Execution
 |
 +-- Tool Results
 |
 +-- Multiple Tool Usage
 |
 +-- Agent Streaming
 |
 +-- Interactive Agent
```

## 34. Learning Outcomes

After completing this experiment, you should understand:

1. What a ReAct agent is.
2. How an LLM can be connected to tools.
3. How LangChain exposes Python functions as tools.
4. How an agent can select an appropriate tool.
5. How tool results are returned to the agent.
6. How multiple tools can be used in one request.
7. How streaming exposes agent execution events.
8. How to build an interactive terminal-based agent.
9. Why tool descriptions and input types matter.
10. Why unrestricted code execution should be avoided in production.

## 35. Summary

This project demonstrates a basic ReAct agent using a local Llama 3.2 model through Ollama.

The core workflow is:

```text
User Query
    |
    v
ReAct Agent
    |
    v
Llama 3.2
    |
    v
Analyze Request
    |
    v
Select Tool
    |
    +------> Calculator
    |
    +------> Word Counter
    |
    v
Tool Result
    |
    v
Llama 3.2
    |
    v
Final Answer
```

The main idea is:

> **The LLM decides what action is appropriate, the application executes the selected tool, and the result is returned to the LLM so it can produce the final response.**

This provides a foundation for more advanced agentic systems involving search, APIs, databases, RAG, MCP, memory, and multi-agent orchestration.

## License

This project is intended for educational and experimental purposes.
