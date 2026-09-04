import os
import requests

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun


# ============================================================
# Function Calling and Tool Integration
# ============================================================


# ============================================================
# STEP 1: Load Google API Key
# ============================================================

load_dotenv()

if os.environ.get("GOOGLE_API_KEY"):
    print("Google API Key is set.")
else:
    print("Google API Key is NOT set.")
    print("Please create a .env file with:")
    print("GOOGLE_API_KEY=your_api_key")
    exit()


# ============================================================
# STEP 2: Initialize Gemini
# ============================================================

llm = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai"
)

print("Gemini model loaded successfully!")


# ============================================================
# STEP 3: Create DuckDuckGo Search Tool
# ============================================================

@tool("duckduckgo")
def duckduckgo(query: str) -> str:
    """
    Search DuckDuckGo for the given query
    and return the search results.
    """

    duck_search = DuckDuckGoSearchRun()

    return duck_search.invoke(query)


print("DuckDuckGo tool created successfully!")


# ============================================================
# STEP 4: Create Wikipedia Tool
# ============================================================

@tool
def wiki_tool(query: str) -> str:
    """
    Search Wikipedia for information.
    """

    headers = {
        "User-Agent": "MyLangChainDemo/1.0"
    }

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }

    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.text


print("Wikipedia tool created successfully!")


# ============================================================
# STEP 5: Create Personal Information Tool
# ============================================================

@tool
def personal_info(name: str) -> str:
    """
    Get personal information about Alice, Bob, or Charlie.
    """

    info = {
        "Alice":
            "Alice is a software engineer with 5 years of experience in AI.",

        "Bob":
            "Bob is a data scientist who loves working with large datasets.",

        "Charlie":
            "Charlie is a product manager with a background in tech."
    }

    return info.get(
        name,
        "No information available for this person."
    )


print("Personal information tool created successfully!")


# ============================================================
# STEP 6: Create List of Tools
# ============================================================

tools = [
    duckduckgo,
    wiki_tool,
    personal_info
]

print("All tools created successfully!")


# ============================================================
# STEP 7: Bind Tools to Gemini
# ============================================================

llm_with_tools = llm.bind_tools(tools)

print("Tools successfully bound to Gemini!")


# ============================================================
# STEP 8: User Query
# ============================================================

user_query = """
Tell me about Alice using the personal information tool.

Search Wikipedia for Geoffrey Hinton's biography.

Search DuckDuckGo for the latest news about Geoffrey Hinton.

Combine everything into a single response.
"""


# ============================================================
# STEP 9: Ask Gemini to Decide Which Tools to Use
# ============================================================

response = llm_with_tools.invoke(user_query)

print("\n========================================")
print("TOOL CALLS")
print("========================================")

print(response.tool_calls)


# ============================================================
# STEP 10: Create Tool Dictionary
# ============================================================

tool_dict = {
    tool.name: tool
    for tool in tools
}


# ============================================================
# STEP 11: Execute All Tool Calls
# ============================================================

tool_messages = []

for tool_call in response.tool_calls:

    print("\n----------------------------------------")
    print("Executing Tool:", tool_call["name"])
    print("----------------------------------------")

    selected_tool = tool_dict[tool_call["name"]]

    tool_result = selected_tool.invoke(
        tool_call["args"]
    )

    print("Tool executed successfully.")

    tool_messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )
    )


# ============================================================
# STEP 12: Create Messages for Gemini
# ============================================================

messages = [
    HumanMessage(content=user_query),
    response,
    *tool_messages
]


# ============================================================
# STEP 13: Send Tool Results Back to Gemini
# ============================================================

final_response = llm_with_tools.invoke(messages)


# ============================================================
# STEP 14: Display Final Answer
# ============================================================

print("\n========================================")
print("FINAL ANSWER")
print("========================================")

if isinstance(final_response.content, list):

    for block in final_response.content:

        if isinstance(block, dict):

            if block.get("type") == "text":
                print(block.get("text"))

        else:
            print(block)

else:
    print(final_response.content)


print("\n========================================")
print("EXPERIMENT COMPLETED")
print("========================================")