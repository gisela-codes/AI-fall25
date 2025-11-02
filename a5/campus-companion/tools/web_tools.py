from smolagents import Tool, DuckDuckGoSearchTool
from bs4 import BeautifulSoup
import pandas as pd
import requests

class UtahTechSearchTool(Tool):
    name = "utahtech_search"
    description = "Given a query, this tool will return top results about utahtech."
    inputs = {
        "query": {"type": "string", "description": "The query to search"}
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self._ddgs = DuckDuckGoSearchTool()
    def forward(self, query: str) -> str:
        q = f'"utahtech" {query}'
        return self._ddgs(q)
    
class UtahTechEventsTool(Tool):
    name = "pandas_query_tool"
    description = "Executes Python/Pandas code on a DataFrame named 'df'. The code must assign its final answer to a variable named 'result'."
    
    inputs = {
        "code_snippet": {
            "type": "string",
            "description": "A string of valid Python/Pandas code that operates on a DataFrame named 'df' and assigns the output to a variable named 'result'."
        }
    }
    output_type = "string"

    def __init__(self, csv_path: str = "events.csv"):
        super().__init__()
        self.df = pd.read_csv(csv_path)

            # --- Optional Pre-processing ---
            # It's good practice to convert types here so the LLM doesn't have to.
            # self.df['date'] = pd.to_datetime(self.df['date'])
            # self.df['start_time'] = pd.to_datetime(self.df['start_time'], format='%H:%M').dt.time
            
    def forward(self, code_snippet: str) -> str:
        if self.df.empty:
            return "Error: The event data is not available or could not be loaded."
        
        local_scope = {"df": self.df, "pd": pd}
        try:
            # create/modify variables within 'local_scope'
            exec(code_snippet, globals(), local_scope)
            # print(code_snippet)

            # Check if the 'result' variable was created by the code
            if "result" in local_scope:
                return str(local_scope["result"])
            else:
                return "Error: Code executed, but no 'result' variable was set. The code must assign the final answer to a variable named 'result'."
        
        except Exception as e:
            return f"Error executing code: {e}"


class ScrapePageTool(Tool):
    name = "scrape_page"
    description = "Fetch a web page and return a cleaned text summary (title + first ~800 characters)."
    inputs = {"url": {"type":"string","description":"HTTP/HTTPS URL to fetch"}}
    output_type = "string"

    def forward(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            return f"Request failed: {e}"
        soup = BeautifulSoup(resp.text, "html.parser")
        title = (soup.title.string.strip() if soup.title and soup.title.string else url)
        # crude extract of visible text
        for tag in soup(["script","style","noscript"]):
            tag.decompose()
        text = " ".join(t.get_text(" ", strip=True) for t in soup.find_all(["p","li","h1","h2","h3"]))
        text = " ".join(text.split())
        snippet = text[:800] + ("…" if len(text) > 800 else "")
        return f"{title}\n{snippet}"

