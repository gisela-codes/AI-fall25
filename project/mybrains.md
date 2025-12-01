## Agent Workflow Example

Here’s how the agent will operate:
Scrape job posting (Playwright MCP)
Evaluate fit (LLM)
Append to sheet (Google Sheets tool)
Generate resume in Markdown
Convert to DOCX/PDF via Pandoc
Upload to Drive → Resumes folder
Update sheet row with resume_link
(Future) Application Agent pre-fills applications

Application Orchestration Logic

A new agent or mode: ApplicationAgent

Knows how to:
Filter sheet rows
Call Playwright to open job URLs
Call LLM to generate application text
Update the sheet with statuses
Optional UI / CLI

Simple menu:
[1] Discover new jobs
[2] Generate resumes
[3] Draft & pre-fill applications for jobs marked 'Ready to Apply'

---
Nice, this is a good moment to “freeze” v1 and show how v2 evolves from it. I’ll break it into:

1. How the **workflow changes**
2. A clear list of **agents**
3. A clear list of **tools (MCPs)**

---

## 1️⃣ Workflow – v1 vs v2

### Current workflow (single-agent-ish)

**Goal:** Find good jobs, track them, and generate resumes.

1. **Job discovery**

   * You tell the agent a query (e.g., “junior SWE remote”).
   * Agent uses **Playwright MCP** to scrape job postings.

2. **Fit evaluation**

   * Agent reads your **profile** + **job description**.
   * LLM scores fit and decides if it’s worth tracking.

3. **Log in Google Sheet**

   * Agent uses the **Sheets tool** to append a row:
     `company, role, job_link, location, fit_score, status="Found", timestamp`

4. **Generate resume**

   * Agent generates a **Markdown resume** tailored to that job.
   * Uses **Resume tool** to:

     * `save_markdown` → `*.md`
     * `convert_markdown_to_docx` with Pandoc → `*.docx`

5. **Upload to Drive**

   * Agent calls **Drive tool** to upload the `.docx` to `JobAgent/Resumes/`.
   * Gets a `resume_link` URL.

6. **Update Sheet**

   * Agent updates the row with: `resume_link`, `status="Resume Generated"`.

That’s v1: **Find → Log → Resume → Link**.

---

### 🔹 Iteration 2 – Updated workflow with Application Agent

**Goal:** Add semi-automated applying on top of v1.

You keep everything above, but **extend** the workflow:

#### A. Discovery Flow (mostly unchanged)

Same as v1, except now:

* When a resume is generated and uploaded, the agent sets:
  `status="Ready to Apply"` instead of just `"Resume Generated"`.

So jobs move through states like:

* `Found` → `Ready to Apply`

#### B. New Application Flow (second iteration)

1. **Select jobs to apply**

   * **Application Agent** scans the Sheet for rows where:
     `status="Ready to Apply"`.

2. **Fetch context**

   * Reads:

     * Job info (company, role, job_link, description, fit_score)
     * `resume_link` (from Drive)
     * Your profile (via profile loader or config).

3. **Generate application content**

   * LLM creates:

     * A **cover letter** tailored to the job.
     * Short-form answers (e.g., “Why this company?”, “Describe a relevant project”).

4. **Pre-fill application form (semi-automated)**

   * Application Agent uses **Playwright MCP** to:

     * Open `job_link` (application page).
     * Locate fields (name, email, LinkedIn, text areas, etc.).
     * Fill them with:

       * Your personal info
       * Resume upload (if supported in v2)
       * Generated cover letter / answers.
   * **Stops before clicking Submit**.

5. **User review and manual submit**

   * You review what’s been filled in the browser.
   * You manually click **Submit** (or tweak text first).

6. **Update Sheet**

   * Application Agent updates the row via **Sheets tool**:
     `status="Applied (Manual Submit)"`, `applied_at=<timestamp>`
   * Optionally stores notes: `application_notes = "Pre-filled by Application Agent"`

So v2 adds: **Ready to Apply → Pre-filled → Applied**.

---

## 2️⃣ Agents in Iteration 2

You can describe your system as having **two main agents** (or modules) in v2:

1. **Discovery Agent**

   * Responsibilities:

     * Scrape job postings.
     * Evaluate fit based on your profile.
     * Log jobs into the Google Sheet.
     * Generate tailored resumes and upload to Drive.
     * Set job `status` to `"Ready to Apply"`.

2. **Application Agent** (new in v2)

   * Responsibilities:

     * Read jobs from the Sheet where `status="Ready to Apply"`.
     * Generate cover letters and short-form answers.
     * Use Playwright to **pre-fill** application forms (semi-automated).
     * Update job `status` to `"Applied (Manual Submit)"` and log timestamps/notes.

*(If you want to keep it simple in code, both can still be implemented with Smol Agents, just with different “roles” / entrypoints.)*

---

## 3️⃣ Tools / MCPs in Iteration 2

Here’s the list you can put in your proposal.

### Shared by both agents

1. **Playwright MCP**

   * Used by **Discovery Agent** to scrape job pages.
   * Used by **Application Agent** to open application pages and pre-fill forms.

2. **Google Sheets Tool**

   * `append_job_row(job_data)` – add a new job.
   * `update_job_row(row_id, updates)` – status, resume link, applied_at.
   * `get_jobs_by_status(status)` – e.g., fetch `"Ready to Apply"` jobs.

3. **Google Drive Tool**

   * `upload_resume_to_drive(local_path, folder_id, file_name) -> drive_url`
   * Stores all resumes in `JobAgent/Resumes/`.
   * Returns URLs to be written into the Sheet.

4. **Resume Document Tool (Markdown + Pandoc)**

   * `save_markdown(markdown_text, base_name) -> md_path`
   * `convert_markdown_to_docx(md_path, base_name) -> docx_path`
   * (Optionally later) `convert_markdown_to_pdf`.

5. **Profile Loader Tool (simple)**

   * `get_profile() -> profile_json`
   * Stores your experience, education, skills, preferences.
   * Used by both agents for fit evaluation and content generation.

--- 
Here is a clean, professor-ready **“Iteration 1 vs. Iteration 2 Workflow”** section with a table and a tools/agents list you can paste directly into your report.

---

# **Iteration 1 vs. Iteration 2 Workflow**

### **Iteration 1: Job Discovery + Resume Generation**

In the first iteration, the system functions as a discovery and resume-generation agent. It scrapes job postings using Playwright MCP, evaluates their fit based on the user’s profile, and logs promising roles into a Google Sheet. For each tracked job, the agent generates a tailored Markdown resume, converts it to DOCX using Pandoc, uploads it to a dedicated Google Drive folder, and stores the file link in the tracking sheet.

### **Iteration 2: Semi-Automated Application Agent**

The second iteration introduces an Application Agent that operates on top of the existing pipeline. It scans the Google Sheet for jobs marked “Ready to Apply,” generates application materials such as cover letters and short-form responses, and uses Playwright MCP to pre-fill common fields on application forms. The agent pauses before final submission, allowing the user to manually review and submit. Afterward, it updates the job’s status in the sheet, completing a semi-automated application workflow.

---

# **Workflow Comparison**

| Stage                       | **Iteration 1**                               | **Iteration 2**                                          |
| --------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| **Job Discovery**           | Scrape listings with Playwright MCP           | Same as Iteration 1                                      |
| **Fit Evaluation**          | LLM analyzes profile vs. job                  | Same as Iteration 1                                      |
| **Tracking**                | Append job row to Google Sheet                | Adds new statuses: “Ready to Apply,” “Applied”           |
| **Resume Creation**         | Generate MD → Pandoc → DOCX → Upload to Drive | Same, but resumes trigger the apply pipeline             |
| **Application Preparation** | Not included                                  | Application Agent generates cover letters + Q&A          |
| **Form Interaction**        | None                                          | Playwright MCP pre-fills application forms               |
| **Submission**              | None                                          | User manually reviews and clicks submit                  |
| **Sheet Updates**           | Stores job + resume link                      | Updates status to “Applied (Manual Submit)” + timestamps |

---

# **Agents**

### **1. Discovery Agent (Iteration 1 & 2)**

* Scrapes job postings
* Evaluates fit score
* Logs jobs into Google Sheet
* Generates tailored resumes
* Uploads resumes to Drive
* Marks jobs as **“Ready to Apply”**

### **2. Application Agent (Iteration 2)**

* Reads jobs with `status="Ready to Apply"`
* Generates cover letters and short-answer responses
* Opens application pages via Playwright MCP
* Pre-fills common form fields
* Requires user confirmation before submission
* Updates job status to **“Applied (Manual Submit)”**

---

# **Tools (MCPs) Used by the Agents**

### **1. Playwright MCP**

* Iteration 1: scrape job descriptions
* Iteration 2: pre-fill fields on application forms

### **2. Google Sheets Tool**

* Append new job rows
* Update job status, timestamps, resume links
* Retrieve jobs by status
* Acts as the system’s structured job database

### **3. Google Drive Tool**

* Upload DOCX/PDF resumes
* Return shareable Drive URLs
* Store all resumes under `JobAgent/Resumes/`

### **4. Resume Document Tool (Markdown + Pandoc)**

* Save generated resume content as Markdown
* Convert MD → DOCX (Pandoc)
* Provide output paths for Drive upload

### **5. Profile Loader Tool**

* Provide structured representation of the user’s skills, experience, and preferences
* Used for fit scoring and personalized content generation

