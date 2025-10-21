#############################################
# Environment loading
#############################################
import dotenv
import os
import time
g_dotenv_loaded = False
def getenv(variable: str) -> str:
    global g_dotenv_loaded
    if not g_dotenv_loaded:
        g_dotenv_loaded = True
        dotenv.load_dotenv()
    value = os.getenv(variable)
    return value

gemini_api_key = getenv("GEMINI_API_KEY")
openai_api_key = getenv("OPENAI_API_KEY")

if not gemini_api_key:
    raise Exception("GEMINI_API_KEY needs to be set in .env.")

#############################################
# Model connection
#############################################
from openai import OpenAI
from openai import RateLimitError

gemini_client = OpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
openai_client = OpenAI(api_key=openai_api_key)

def query_ai(model, query, candidate):
    llm = model.split("-")[0]
    system_prompt = """You are an information retrieval judge. Focus only on topical relevance to the query.
    Analyze the query and candidate text, then rate how relevant the candidate text is to the query on a scale from 0 (not relevant) to 1 (perfectly relevant).
    Respond with only a number."""

    user_content = f"""
    Query: "{query}"
    Candidate: "{candidate}"
    """

    for attempt in range(5):
        try:
            if llm == "gpt":
                response = openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ]
                )
            elif llm == "gemini":
                response = gemini_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ]
                )
                time.sleep(4)
            return(float(response.choices[0].message.content.strip()))

        except RateLimitError as e:
            if llm == "gemini":
                base_wait = 4   
            else:
                base_wait = 1   
            wait = base_wait + (2 * attempt)
            print(f"[{llm}] Rate-limited. Retrying in {wait}s…")
            time.sleep(wait)

        except Exception as e:
            print(f"[{llm}] Error: {e}")
            raise
