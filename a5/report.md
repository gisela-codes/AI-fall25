# Campus Companion


## System Prompt
> You are an agent that helps users learn about and navigate Utah Tech University (UT). 
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
---

## Tools Added

### `UtahTechSearchTool`

**Class:**

```python
class UtahTechSearchTool(Tool):
    name = "utahtech_search"
    description = "Given a query, this tool will return top results about utahtech."
    inputs = {
        "query": {"type": "string", "description": "The query to search"}
    }
    output_type = "string"
```

---

### `UtahTechEventsTool`

**Class:**

```python
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
```

---

## Prompts Modified

For my csv tool I realized I can't return the entire dataframe to the llm. So I had to revise my system and tool prompt. In the system prompt I included the schema for the csv. In the tool prompt, instead of receiving a query, it now accepts Python code as a string, which I can execute programmatically to return smaller chunks of data.

---

## Example Interactions

### Example 1

**Prompt:**
`what does gisela do for work at utahtech?`

**Answer:**
Gisela Benavides Canas is a Web Developer for Utah Tech University.

---

### Example 2

**Prompt:**
`who is the president at utahtech?`

**Answer:**
Shane B. Smeed

---

### Example 3

**Prompt:**
`what events are there in november?`

**Answer:**
Here are the events happening in November:

1. **Southern Utah Code Camp**
   Date: November 1, 2025
   Time: 09:00 – 16:00
   Description: Regional coding event with prizes and workshops.

2. **AI Ethics Panel**
   Date: November 5, 2025
   Time: 14:00 – 16:00
   Description: Perspectives on responsible AI at UTU.

3. **Women in Tech Meetup**
   Date: November 12, 2025
   Time: 17:30 – 19:00
   Description: Meet fellow students and local engineers.

4. **Python for Bioinformatics Workshop**
   Date: November 15, 2025
   Time: 10:00 – 12:00
   Description: Notebook-driven intro tailored for biology professionals.

---

### Example 4

**Prompt:**
`who is the previous president at ut?`

**Answer:**
The previous president of Utah Tech University was Richard “Biff” Williams.

