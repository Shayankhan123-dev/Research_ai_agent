from datetime import datetime
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# # 1. DuckDuckGo Web Search Tool
# search_tool = DuckDuckGoSearchRun()

# 2. Wikipedia Search Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# 3. Custom File Saver Tool
@tool
def save_tool(data: str, filename: str = "research_output.txt") -> str:
    """Saves structured research text data to a local text file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_content = f"--- Research Report ({timestamp}) ---\n\n{data}\n"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
        
    return f"Successfully saved output to {filename}"