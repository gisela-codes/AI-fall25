from smolagents import ToolCallingAgent
import model_utils
from tools.web_tools import UtahTechEventsTool, ScrapePageTool, UtahTechSearchTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.google_build_reasoning_model()

    tools = [
        UtahTechEventsTool(),
        ScrapePageTool(),
        UtahTechSearchTool()
    ]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""You are an agent that helps users learn about and navigate Utah Tech University (UT). 
            When the user asks a question about the university, find accurate, up-to-date information.
            Keep tone friendly and helpful.

            Your goal: help students, faculty, and visitors quickly find what they need at Utah Tech 
            University, including upcoming events, courses, and campus opportunities.

            You have access to a list of Utah Tech events. Here is the schema 
            Data columns (total 8 columns):
            #   Column       Non-Null Count  Dtype 
            ---  ------       --------------  ----- 
            0   date         24 non-null     object
            1   start_time   23 non-null     object
            2   end_time     23 non-null     object
            3   title        24 non-null     object
            4   location     23 non-null     object
            5   category     23 non-null     object
            6   description  23 non-null     object
            7   url          22 non-null     object
            dtypes: object(8)
        """
    )
    return agent


