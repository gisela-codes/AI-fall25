import os
import re
import subprocess
import json
from datetime import datetime
from typing import Dict
from smolagents import Tool

PROFILE_PATH = "profile.json"

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
RESUME_DIR = os.path.join(PROJECT_ROOT, "resumes")

REFERENCE_ODT = os.path.join(TOOLS_DIR, "reference.docx")

def snake_case(name: str) -> str:
    name = re.sub(r'([A-Z][a-z]+)', r' \1', re.sub(r'([A-Z]+)', r' \1', name.replace('-', ' ')))
    return '_'.join(name.split()).lower()


class ResumeBuilderTool(Tool):
    name = "resume_builder"
    description = (
        "Takes ATS-friendly resume content in Markdown plus a job title, "
        "saves it to the resumes/ folder, and uses pandoc with a reference "
        "Converts md to DOCX. Returns the paths to the markdown "
        "and docx files."
    )

    inputs = {
        "job_title": {
            "type": "string",
            "description": "The job title for this resume (e.g., 'Software Engineer').",
        },
        "resume_markdown": {
            "type": "string",
            "description": (
                "Full resume content in Markdown. Must follow the fixed resume template."
            ),
        },
    }

    output_type = "object"

    def forward(self, job_title: str, resume_markdown: str) -> Dict:
        os.makedirs(RESUME_DIR, exist_ok=True)

        slug = snake_case(job_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        md_filename = f"{slug}_{timestamp}.md"
        docx_filename = f"{slug}_{timestamp}.docx"

        md_path = os.path.join(RESUME_DIR, md_filename)
        docx_path = os.path.join(RESUME_DIR, docx_filename)

        # Write markdown resume
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(resume_markdown)
        if os.path.exists(REFERENCE_ODT):
            subprocess.run( ["pandoc", md_path, "-o", docx_path, "-f", "markdown", "-t", "docx+styles", f"--reference-doc={REFERENCE_ODT}"], check=True)

        return {
            "job_title": job_title,
            "markdown_path": md_path,
            "docx_path": docx_path,
        }

class ReadProfileTool(Tool):
    name = "read_profile"
    description = (
        "Reads the user's profile.json file containing personal information, "
        "experience, skills, and education. Use this to get user information "
        "when creating tailored resumes."
    )
    
    inputs = {}
    
    output_type = "object"
    
    def forward(self) -> Dict:
        if not os.path.exists(PROFILE_PATH):
            return {"error": f"Profile file not found at {PROFILE_PATH}"}
        
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
        
        return profile_data
