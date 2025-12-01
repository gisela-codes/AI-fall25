# JobHunterAI

JobHunterAI is an automated job-search assistant powered by smolagents, Chrome DevTools MCP, Google Sheets, and Google Drive. It scrapes job listings from the web, logs them to a tracking spreadsheet, generates ATS-friendly resumes, and uploads them automatically.

## Overview

JobHunterAI automates the repetitive parts of job applications:

- Searching job boards
- Scraping job listings
- Logging them into Google Sheets (without duplicates)
- Generating tailored Markdown resumes using a custom template
- Converting them to .docx with Pandoc
- Uploading resumes to Google Drive
- Writing resume links back into the sheet

Using AI automation and a modular tool system, JobHunterAI can run bulk job searches, track opportunities, produce resumes for new listings, and help users stay organized and consistent in their applications.

The agent is designed to be fully deterministic, tool-driven, and easily extendable.

## PEAS Assesment

### Performance Measure

#### Application Quality
- Finds jobs that match user qualifications and experience
- Creates personalized, ATS-friendly resumes using templates tailored to job descriptions
- Generates resumes in .docx format compatible with applicant tracking systems

#### Efficiency
- Identifies jobs that align with user interests and preferences
- Eliminates duplicate tracking and manual file management

#### Results
- Accurately tracks potential employers in Google Sheets without duplicates
- Maintains organized application history with resume links

### Environment

- **User profile data:** Experience, education, projects, skills, languages, job preferences stored in `profile.json`
- **Google Sheet:** Centralized tracking system for job applications
- **Resume templates:** Markdown and .docx reference templates for consistent formatting
- **Google Drive:** Cloud storage for generated resumes
- **Chrome browser:** Job board web scraping and DOM manipulation environment

### Actuators

- Editing and updating Google Sheets with new job entries
- Generating tailored resumes for each application
- Uploading resumes to Google Drive
- Writing resume links back to tracking spreadsheet

### Sensors

- Scraping job postings from web pages using Chrome DevTools MCP
- Reading and parsing user profile data from `profile.json`
- Reading current contents of Google Sheets to check for duplicates
- Capturing page snapshots for debugging and verification

## Features

### Intelligent Job Scraping

- Uses Chrome DevTools MCP to browse job boards
- Avoids Cloudflare issues by evaluating scripts directly in the DOM
- Dynamically adapts selectors to match the actual page HTML

### Automatic Duplicate Prevention

- Reads the existing Google Sheet
- Matches jobs by Job Link or Title+Company+Location
- Skips already logged jobs
- Only processes new opportunities

### Resume Generation

- Uses a user-defined Markdown template
- Fills the body with tailored ATS-friendly content
- Converts .md to .docx using Pandoc
- Produces consistent output across job listings

### Drive Upload and Sheet Update

- Uploads resume to Google Drive
- Writes the resume link back into the correct row
- No manual file management required

### Fully Modular smolagents Tools

Each operation is a clean tool:

- `read_profile`
- `read_job_sheets`
- `log_job_to_sheet`
- `resume_builder`
- `upload_resume_and_update_sheet`

### Debugging Automation

- Snapshot the page
- Inspect the returned HTML
- Retry selector strategy once if scraping returns empty

## Architecture

```
JobHunterAI/
├── agent.py
├── credentials.json
├── model_utils.py
├── profile.json            # User's skills, background, projects
├── requirements.txt
├── resumes/                # Output folder for .md and .docx resumes
├── run.py                  # Entry point for searching jobs & running the agent
├── tmp/                    # Saved snapshots (debugging)
└── tools/
    ├── drive_tools.py
    ├── reference.docx
    ├── reference.md
    ├── resume_tools.py
    └── token.json
```

## Core Components

| Component | Role |
|-----------|------|
| ToolCallingAgent | Orchestrates workflow via LLM tool calls |
| Chrome DevTools MCP | Executes DOM queries & JS inside real webpages |
| Google Sheets API | Tracks job entries and metadata |
| Google Drive API | Stores generated resumes |
| Pandoc | Converts Markdown to Word (.docx) resumes |
| smolagents tools | Each functionality exposed as a composable tool |

## Tools Documentation

### read_profile

Reads `profile.json` and returns the user's personal info, skills, projects, etc. Used to generate tailored resume content.

**Inputs:** none

**Output:** object

```json
{
  "name": "...",
  "skills": [...],
  "experience": [...],
  ...
}
```

### read_job_sheets

Fetches all rows from the Google Sheet and returns structured objects:

```json
[
  {
    "Title": "...",
    "Description": "...",
    "Company": "...",
    "location": "...",
    "Job Link": "...",
    "Resume Link": "...",
    "Status": "...",
    "row_number": 5
  }
]
```

Used for deduplication and conditional logic.

### log_job_to_sheet

Appends new job listings (no duplicates). Returns the row number of the new entry.

**Inputs:** `title`, `description`, `company`, `location`, `job_link`

**Output:**

```json
{ "row_number": 7 }
```

### resume_builder

Injects AI-generated BODY markdown into your resume template and converts to .docx.

**Inputs:** `job_title`, `body_markdown`

**Output:**

```json
{
  "markdown_path": "resumes/swe_20240102.md",
  "docx_path": "resumes/swe_20240102.docx"
}
```

### upload_resume_and_update_sheet

Uploads DOCX to Drive and updates the Resume Link column in the correct row.

**Inputs:** `local_path`, `job_title`, `row_number`

**Output:**

```json
{
  "row_number": 7,
  "resume_url": "https://drive.google.com/file/d/.../view"
}
```

## End-to-End Workflow

Here is the complete JobHunterAI pipeline:

1. **Parse query** - Extract job title and location
2. **Navigate and load job search page** - Using Chrome DevTools MCP
3. **Take snapshot** - HTML or AX tree, saved for debugging
4. **Inspect DOM using evaluate_script** - Detect job card selectors
5. **Run a single JavaScript extraction script** - Returns:
   ```json
   [
     {
       "title": "...",
       "company": "...",
       "location": "...",
       "job_link": "...",
       "description": "..."
     }
   ]
   ```
6. **read_job_sheets** - Check for duplicates
7. **For each new job:**
   - `log_job_to_sheet` - Get row_number
8. **If at least one new job exists:**
   - `read_profile`
   - Generate tailored resume BODY
   - `resume_builder`
   - `upload_resume_and_update_sheet`
9. **If no new jobs:**
   - Skip resume generation/upload
   - Summarize to the user
10. **Final summary:**
    - New jobs logged
    - Best job selected
    - Resume created and uploaded
    - Sheet updated

## Usage Examples

### Search for Software Engineer Jobs

```bash
python run.py "search for software engineer jobs in st.george"
```

### Initialize Google OAuth (One-Time)

```bash
python run.py --init-google-auth
```

## Requirements

See `requirements.txt` for the complete list of dependencies.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Google API credentials to `credentials.json`
4. Initialize Google OAuth: `python run.py --init-google-auth`
5. Configure your profile in `profile.json`
6. Run your first job search



# JobHunterAI

JobHunterAI is an automated job-search assistant powered by smolagents, Chrome DevTools MCP, Google Sheets, and Google Drive. It scrapes job listings from the web, logs them to a tracking spreadsheet, generates ATS-friendly resumes, and uploads them automatically.

## Overview

JobHunterAI automates the repetitive parts of job applications:

- Searching job boards
- Scraping job listings
- Logging them into Google Sheets (without duplicates)
- Generating tailored Markdown resumes using a custom template
- Converting them to .docx with Pandoc
- Uploading resumes to Google Drive
- Writing resume links back into the sheet

Using AI automation and a modular tool system, JobHunterAI can run bulk job searches, track opportunities, produce resumes for new listings, and help users stay organized and consistent in their applications.

The agent is designed to be fully deterministic, tool-driven, and easily extendable.

## Features

### Intelligent Job Scraping

- Uses Chrome DevTools MCP to browse job boards
- Avoids Cloudflare issues by evaluating scripts directly in the DOM
- Dynamically adapts selectors to match the actual page HTML

### Automatic Duplicate Prevention

- Reads the existing Google Sheet
- Matches jobs by Job Link or Title+Company+Location
- Skips already logged jobs
- Only processes new opportunities

### Resume Generation

- Uses a user-defined Markdown template
- Fills the body with tailored ATS-friendly content
- Converts .md to .docx using Pandoc
- Produces consistent output across job listings

### Drive Upload and Sheet Update

- Uploads resume to Google Drive
- Writes the resume link back into the correct row
- No manual file management required

### Fully Modular smolagents Tools

Each operation is a clean tool:

- `read_profile`
- `read_job_sheets`
- `log_job_to_sheet`
- `resume_builder`
- `upload_resume_and_update_sheet`

### Debugging Automation

- Snapshot the page
- Inspect the returned HTML
- Retry selector strategy once if scraping returns empty

## Architecture

```
JobHunterAI/
├── agent.py
├── credentials.json
├── model_utils.py
├── profile.json            # User's skills, background, projects
├── requirements.txt
├── resumes/                # Output folder for .md and .docx resumes
├── run.py                  # Entry point for searching jobs & running the agent
├── tmp/                    # Saved snapshots (debugging)
└── tools/
    ├── drive_tools.py
    ├── reference.docx
    ├── reference.md
    ├── resume_tools.py
    └── token.json
```

## Core Components

| Component | Role |
|-----------|------|
| ToolCallingAgent | Orchestrates workflow via LLM tool calls |
| Chrome DevTools MCP | Executes DOM queries & JS inside real webpages |
| Google Sheets API | Tracks job entries and metadata |
| Google Drive API | Stores generated resumes |
| Pandoc | Converts Markdown to Word (.docx) resumes |
| smolagents tools | Each functionality exposed as a composable tool |

## Tools Documentation

### read_profile

Reads `profile.json` and returns the user's personal info, skills, projects, etc. Used to generate tailored resume content.

**Inputs:** none

**Output:** object

```json
{
  "name": "...",
  "skills": [...],
  "experience": [...],
  ...
}
```

### read_job_sheets

Fetches all rows from the Google Sheet and returns structured objects:

```json
[
  {
    "Title": "...",
    "Description": "...",
    "Company": "...",
    "location": "...",
    "Job Link": "...",
    "Resume Link": "...",
    "Status": "...",
    "row_number": 5
  }
]
```

Used for deduplication and conditional logic.

### log_job_to_sheet

Appends new job listings (no duplicates). Returns the row number of the new entry.

**Inputs:** `title`, `description`, `company`, `location`, `job_link`

**Output:**

```json
{ "row_number": 7 }
```

### resume_builder

Injects AI-generated BODY markdown into your resume template and converts to .docx.

**Inputs:** `job_title`, `body_markdown`

**Output:**

```json
{
  "markdown_path": "resumes/swe_20240102.md",
  "docx_path": "resumes/swe_20240102.docx"
}
```

### upload_resume_and_update_sheet

Uploads DOCX to Drive and updates the Resume Link column in the correct row.

**Inputs:** `local_path`, `job_title`, `row_number`

**Output:**

```json
{
  "row_number": 7,
  "resume_url": "https://drive.google.com/file/d/.../view"
}
```

## End-to-End Workflow

Here is the complete JobHunterAI pipeline:

1. **Parse query** - Extract job title and location
2. **Navigate and load job search page** - Using Chrome DevTools MCP
3. **Take snapshot** - HTML or AX tree, saved for debugging
4. **Inspect DOM using evaluate_script** - Detect job card selectors
5. **Run a single JavaScript extraction script** - Returns:
   ```json
   [
     {
       "title": "...",
       "company": "...",
       "location": "...",
       "job_link": "...",
       "description": "..."
     }
   ]
   ```
6. **read_job_sheets** - Check for duplicates
7. **For each new job:**
   - `log_job_to_sheet` - Get row_number
8. **If at least one new job exists:**
   - `read_profile`
   - Generate tailored resume BODY
   - `resume_builder`
   - `upload_resume_and_update_sheet`
9. **If no new jobs:**
   - Skip resume generation/upload
   - Summarize to the user
10. **Final summary:**
    - New jobs logged
    - Best job selected
    - Resume created and uploaded
    - Sheet updated

## Usage Examples

### Search for Software Engineer Jobs

```bash
python run.py "search for software engineer jobs in st.george"
```

### Initialize Google OAuth (One-Time)

```bash
python run.py --init-google-auth
```

## Requirements

See `requirements.txt` for the complete list of dependencies.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Google API credentials to `credentials.json`
4. Initialize Google OAuth: `python run.py --init-google-auth`
5. Configure your profile in `profile.json`
6. Run your first job search

