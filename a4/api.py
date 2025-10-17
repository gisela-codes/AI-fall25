#############################################
# Environment loading
#############################################
import dotenv
import os
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

gemini_client = OpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
openai_client = OpenAI(api_key=openai_api_key)

def query_ai(model, query, candidate):
    llm = model.split("-")[0]
    prompt = f""" Analyze the query and candidate text then rate how relevant the candidate text is to the query below on a scale from 0 (not relevant) to 1 (perfectly relevant).
            Query: {query}
            Candidate: {candidate}
            Output only a number between 0 and 1
            """
    if llm == "gpt":
        response = openai_client.chat.completions.create(
            model=model, 
            messages= [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt }
                ]
            }]
        )
    elif llm == "gemini":
        response = gemini_client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": prompt
                    }
                ]}]
        )
    # print(response)
    return(float(response.choices[0].message.content.strip()))

