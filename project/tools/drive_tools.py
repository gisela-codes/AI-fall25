
# https://docs.google.com/spreadsheets/d/1SIYmwu69bMw8r-Ytk_TtD3l_IKL0f_qKwo4Q7DtBLLY/edit?gid=0#gid=0
import os.path
import re
from smolagents import Tool
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, List
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]

PARENT_FOLDER_ID = "1vkbrWYq6sHhIYJj8rq86Anps7iN8nfjq"
FOLDER_ID = "1mgA_fUFL79OPwyjg6T4lyFis2zUtt7HG" #Resumes folder
SAMPLE_SPREADSHEET_ID = "1SIYmwu69bMw8r-Ytk_TtD3l_IKL0f_qKwo4Q7DtBLLY"
RANGE_NAME = "Sheet1!A:G"

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(TOOLS_DIR, "token.json")


def auth() -> Credentials:
    """Return valid Google API credentials for tools (no interactive OAuth here)."""
    if not os.path.exists(TOKEN_PATH):
        raise RuntimeError(
            "Google API token not found. Run `python run.py --init-google-auth` first."
        )

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return creds
class ReadJobSheetsTool(Tool):
    name = "read_job_sheets"
    description = (
        "Reads all job rows from the Google Sheet and returns them as a list of "
        "objects with row_number and columns: Title, Description, Company, "
        "location, Job Link, Resume Link, Status."
    )
    inputs = {}  
    output_type = "array"

    def forward(self) -> List[Dict]:
        creds = auth() 
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=RANGE_NAME
            )
            .execute()
        )

        values = result.get("values", [])
        header = values[0]     
        rows = values[1:]       

        output = []
        for idx, row in enumerate(rows, start=2):  
            obj = {}
            for col_index, col_name in enumerate(header):
                obj[col_name] = row[col_index] if col_index < len(row) else ""
            obj["row_number"] = idx
            output.append(obj)
        return output
    
class LogJobToSheetTool(Tool):
    name = "log_job_to_sheet"
    description = (
        "REQUIRED: After scraping a job listing from a website, use this tool to save it to Google Sheets. "
        "Call this tool for EACH job you find. Parameters: title (job title), description (job summary), "
        "company (company name), location (job location), job_link (full URL to job posting). "
        "Returns the row number where the job was saved."
    )

    inputs = {
        "title": {"type": "string", "description": "Job title."},
        "description": {"type": "string", "description": "Short job description or summary."},
        "company": {"type": "string", "description": "Company name."},
        "location": {"type": "string", "description": "Job location."},
        "job_link": {"type": "string", "description": "URL to the job posting."},
    }

    output_type = "object" 

    def forward(
        self,
        title: str,
        description: str,
        company: str,
        location: str,
        job_link: str,
    ) -> Dict:

        creds = auth()
        service = build("sheets", "v4", credentials=creds)
        new_row = [
            title,
            description,
            company,
            location,
            job_link,
            "",         # Resume Link 
            "not applied"  # Status (default value)
        ]

        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [new_row]},
            )
            .execute()
        )

        # Extract row number from range like "Sheet1!A2:G2"
        updated_range = result["updates"]["updatedRange"]
        m = re.search(r"[A-Z]+(\d+):", updated_range)  # match the row number
        row_number = int(m.group(1)) if m else None

        return {
            "row_number": row_number,
            "updated_range": updated_range,
            "sheet_id": SAMPLE_SPREADSHEET_ID
        }
	

class UploadResumeAndUpdateSheetTool(Tool):
	name = "upload_resume_and_update_sheet"
	description = (
		"Upload a local resume PDF to Google Drive using the job title as the file name, "
		"then write the resume link into the given row in the jobs Google Sheet."
	)
	inputs = {
		"local_path": {
			"type": "string",
			"description": "Path to the local PDF resume file.",
		},
		"job_title": {
			"type": "string",
			"description": "Job title to derive the Drive filename from.",
		},
		"row_number": {
			"type": "integer",
			"description": "Row number in the sheet where the resume link should be stored.",
		},
	}
	output_type = "object"

	def forward(self, local_path: str, job_title: str, row_number: int) -> Dict:
		creds = auth()
		drive = build("drive", "v3", credentials=creds)
		job_title = job_title.lower().strip()
		job_title = re.sub(r"[^a-z0-9]+", "_", job_title)        # Replace spaces/symbols with _
		job_title = re.sub(r"_+", "_", job_title) 
		filename = f"gisela_benavides_{job_title}.docx"

		file_metadata = {
			"name": filename,
			"parents": [FOLDER_ID]
		}

		media = MediaFileUpload(local_path, resumable=True)

		uploaded = (
			drive.files()
			.create(
				body=file_metadata,
				media_body=media,
				fields="id"
			)
			.execute()
		)

		file_id = uploaded["id"]
		resume_url = f"https://docs.google.com/document/d/{file_id}/edit"

		sheets = build("sheets", "v4", credentials=creds)
		range_str = f"Sheet1!F{row_number}"  # column F = Resume Link

		body = {"values": [[resume_url]]}

		update_result = (
			sheets.spreadsheets()
			.values()
			.update(
				spreadsheetId=SAMPLE_SPREADSHEET_ID,
				range=range_str,
				valueInputOption="RAW",
				body=body,
			)
			.execute()
		)

		return {
			"resume_url": resume_url,
			"row_number": row_number,
			"updated_range": update_result.get("updatedRange", range_str),
		}
