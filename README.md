# AI Research Agent (Practice Project)

This repository contains a simple AI agent built using Python, LangChain, and Google's Gemini. 

I created this as a practice project to understand the basics of Agentic AI, learn how the LangChain framework operates, and figure out how to give a Large Language Model (LLM) access to external tools. 

**Note:** This is not a fully functional or production-ready AI assistant. It is a basic-level educational project designed to perform simple research using Wikipedia and save the results. Building this taught me the core concepts of agent loops, tool calling, and structuring LLM outputs.

## What It Does

* **Tool Calling:** The agent takes a natural language query and decides when to use its provided tools.
* **Wikipedia Search:** It uses the LangChain Wikipedia tool to search for factual information related to the prompt.
* **Custom File Saver:** It uses a custom Python function (wrapped as a tool) to write its findings to a local `.txt` file.
* **Structured Output:** After the research is done, it parses the final response into a structured format (JSON/Pydantic model) containing the topic, summary, sources, and tools used.

## Tech Stack

* **Language:** Python
* **Framework:** LangChain (`langchain`, `langchain-classic`)
* **LLM:** Google Gemini (`langchain-google-genai`)
* **Data Validation:** Pydantic

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your free Google AI Studio API key:
   ```text
   GEMINI_API_KEY="your_google_gemini_api_key_here"
   ```

##  Usage

To run the agent, simply execute the main script in your terminal:

```bash
python main.py
```

**Example Interaction:**
1. The terminal will ask: `What would you like me to research?`
2. You can type something like: `Tell me about Artificial Intelligence and save it to a file.`
3. The agent will trigger the Wikipedia tool, write a summary to your local disk using the save tool, and print a structured summary in your terminal.

## Project Structure

* `main.py`: The core agent logic, system prompts, Pydantic schemas, and execution loop.
* `tools.py`: Definitions for the Wikipedia tool and the custom File Saver tool.
* `requirements.txt`: The required Python packages.
* `.env`: Your local environment variables (ignored by Git).
