import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import wiki_tool, save_tool

load_dotenv()

# 1. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    disable_streaming=True,
    timeout=120,          # Fails fast if the network hangs
    max_retries=3        # Automatically retries the connection
)

# 2. Define Pydantic Schema for Final Output
class ResearchResponse(BaseModel):
    topic: str = Field(description="The primary topic being researched")
    summary: str = Field(description="A detailed breakdown of the research findings")
    sources: List[str] = Field(description="Sources or Wikipedia references used")
    tools_used: List[str] = Field(description="List of tool names called during research")

# 3. Clean System Prompt for Tool Calling (No JSON schema conflict)
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research assistant. Gather information using your available tools. "
        "Provide a complete, detailed final summary once you have gathered all necessary data."
    ),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Assemble Agent & Tools
tools = [wiki_tool, save_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# 5. Execution Loop
if __name__ == "__main__":
    user_query = input("\nWhat would you like me to research? ")
    
    # Step A: Run Agent with Tools
    raw_response = agent_executor.invoke({"input": user_query})
    final_text = raw_response.get("output", "")
    
    # Step B: Parse Final Response into Pydantic Object natively
    try:
        structured_llm = llm.with_structured_output(ResearchResponse)
        structured_data = structured_llm.invoke(f"Extract research details from this summary:\n\n{final_text}")
        
        print("\n=== PARSED STRUCTURED OUTPUT ===")
        print(f"Topic: {structured_data.topic}")
        print(f"Summary: {structured_data.summary}")
        print(f"Sources: {structured_data.sources}")
        print(f"Tools Used: {structured_data.tools_used}")
    except Exception as e:
        print("\nRaw Output:", final_text)
        print("Parsing Error:", e)