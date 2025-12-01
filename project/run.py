import sys
import os
from agent import build_agent
from mcp import StdioServerParameters
from smolagents.tools import ToolCollection
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
TOKEN_PATH = os.path.join(TOOLS_DIR, "token.json")
CREDS_PATH = os.path.join(BASE_DIR, "credentials.json")


def init_google_auth():
    if not os.path.exists(CREDS_PATH):
        raise FileNotFoundError(f"credentials.json not found at {CREDS_PATH}")

    flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    os.makedirs(TOOLS_DIR, exist_ok=True)
    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())

    print(f"✅ Google token saved to {TOKEN_PATH}")


def main():
    if "--init-google-auth" in sys.argv:
        init_google_auth()
        return

    # Otherwise, expect a job search query
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(
            "Usage:\n"
            "  python run.py --init-google-auth              # Run once to set up Google token\n"
            "  python run.py \"<your job search query>\"      # Normal run\n"
        )
        return

    query = " ".join(args)
    print("Query:", query)

    server_params = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "chrome-devtools-mcp@latest",
            "--browser-url=http://127.0.0.1:9222",
        ],
    )

    with ToolCollection.from_mcp(server_params, trust_remote_code=True) as mcp_tool_collection:
        agent = build_agent(mcp_tool_collection, verbose=2)
        try:
            result = agent.run(query, max_steps=50)
            print("\n=== Final Answer ===\n", result)
        except Exception as e:
            print("\n[ERROR] Agent failed:", repr(e))


if __name__ == "__main__":
    main()
