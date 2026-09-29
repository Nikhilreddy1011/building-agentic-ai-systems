from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)
print("LLM Loaded Successfully")
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
@tool
def word_counter(text: str) -> str:
    """
    Count the number of words in a text.
    """

    return f"Total words = {len(text.split())}"
tools = [
    calculator,
    word_counter
]

print("Tools Loaded Successfully")
agent = create_react_agent(
    llm,
    tools
)

print("ReAct Agent Created Successfully")
print("\n========== TEST 1 ==========")

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

print("Question: What is 2345 * 789?")
print("Agent:", response["messages"][-1].content)
print("\n========== TEST 2 ==========")

response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "Count the words in 'Artificial Intelligence is transforming education.'"
            )
        ]
    }
)

print("Question: Count the words in 'Artificial Intelligence is transforming education.'")
print("Agent:", response["messages"][-1].content)
print("\n========== TEST 3 ==========")

response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "Calculate 123 * 45 and count the words in 'Artificial Intelligence is transforming the world'"
            )
        ]
    }
)

print("Question: Calculate 123 * 45 and count the words in the given sentence.")
print("Agent:", response["messages"][-1].content)
print("\n========== REACT PROCESS ==========")

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
print("\n======================================")
print("       INTERACTIVE REACT AGENT")
print("======================================")
print("Type 'exit' to stop.\n")


while True:

    question = input("You : ")

    if question.lower() == "exit":
        print("Agent stopped.")
        break

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
        print()

    except Exception as e:

        print("\nError:", e)
        print()s