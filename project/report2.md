## Assignment requirements
In the second week, you will extend your system with additional functionality and refine your documentation to provide a full PEAS assessment. This description should now serve as a complete and formal statement of your problem, capturing how your agent perceives, acts, and measures success. Continue to improve your prototype so that it demonstrates more realistic or complex behavior within its environment. Your report should show clear progress in implementation, describe how your system has evolved since the previous week, and explain how your PEAS elements connect to specific parts of your design. By the end of this week, both your code and your documentation should provide a coherent and well-specified view of your agent’s task and operation.
## Improvments that need to be made
After taking a closer look at the quality of my outputs of my prototype I realized that I need to review the following:

- [ ] Get keywords from job description  
- [ ] Better formatting of resume  (margins, spacing, etc.)
- [ ] Consistent resume formatting  
- [ ] Keeping the resume under 1 page
- [ ] Tool that reads my sheet to avoid duplicate rows (maybe based on job link?)

## Resume
A high quality resume is my overall goal of this project. To address the formatting issues I did some research on pandoc and found out that it allows you to specify a reference DOCX file (--reference-doc) as a style reference in producing a docx or ODT file. 

After several manual attempts and switching doc editors I was finally able to have a solid reference.docx and a md template that is optimized for pandoc. I then had to figure out the best way to communicate with my agent how I want it written.


[First attempt without reference](https://docs.google.com/document/d/1l3yusfLoomLyoLUmtuMycCADD2b-s3bi/edit)

[Reference Docx](https://docs.google.com/document/d/12hs09ergiBgylCwcPqj4XFjkRDO3YkeU/edit?usp=sharing&ouid=105910951170764711145&rtpof=true&sd=true)

[First attempt with reference + modified prompt](https://docs.google.com/document/d/1Tb6s5yzTziC3D-A69TyVdwkBx1BIBAfh/edit)

Example command from when I was manually tweaking my reference:
`pandoc resume.md -o ../resumes/resume.docx --reference-doc=ref.docx -t docx+styles -f markdown`


`-t TO` Docx using text style classes

`-f FROM` Markdown

## Read From Sheet Tool *NEW
To avoid duplicate jobs I revised my prompt and created a tool that'll read entire google sheets
In the process of tweaking my prompt I also specific that I was looking for keywords in the job descriptions.

## Outcome (10 Steps)
>=== Final Answer ===
>
>I found 9 new software engineering jobs in St. George, UT. I have logged these new jobs to your Google Sheet. I created a tailored resume for the "Senior Security Engineer - Application" position and uploaded it to Google Drive. The resume link has been stored in your spreadsheet at row 79.

I feel really good about the outcome it gave me but I'd like to optimize it so I reduces the amount of input tokens and goes through the workflow faster.
[Outcome Resume](https://docs.google.com/document/d/1YdfsurXQlnxdBoaMpAcOfMaKgY25Wsyd/edit)