from docx import Document
from docx.shared import Pt
from io import BytesIO


def _set_default_font(document, font_name="Arial", size=11):
    """
    Sets the default font for the whole document, so every paragraph
    we add automatically uses this font unless we override it.
    """
    style = document.styles["Normal"]
    style.font.name = font_name
    style.font.size = Pt(size)


def generate_ats_friendly_docx(tailored: dict) -> BytesIO:
    """
    Builds an ATS-Friendly DOCX resume from the tailored resume data
    and returns it as an in-memory file (BytesIO), ready for download
    — no file is saved to disk.
    """
    document = Document()
    _set_default_font(document)

    # --- Summary ---
    if tailored.get("summary"):
        document.add_heading("Professional Summary", level=1)
        document.add_paragraph(tailored["summary"])

    # --- Skills ---
    if tailored.get("skills"):
        document.add_heading("Skills", level=1)
        document.add_paragraph(", ".join(tailored["skills"]))

    # --- Experience ---
    if tailored.get("experience"):
        document.add_heading("Experience", level=1)
        for job in tailored["experience"]:
            heading_text = f"{job.get('title', '')} — {job.get('company', '')}"
            if job.get("duration"):
                heading_text += f" ({job['duration']})"

            p = document.add_paragraph()
            run = p.add_run(heading_text)
            run.bold = True

            for bullet in job.get("bullets", []):
                document.add_paragraph(bullet, style="List Bullet")

    # --- Education ---
    if tailored.get("education"):
        document.add_heading("Education", level=1)
        for edu in tailored["education"]:
            heading_text = f"{edu.get('degree', '')} — {edu.get('institution', '')}"
            if edu.get("duration"):
                heading_text += f" ({edu['duration']})"

            p = document.add_paragraph()
            run = p.add_run(heading_text)
            run.bold = True

    # --- Projects ---
    if tailored.get("projects"):
        document.add_heading("Projects", level=1)
        for project in tailored["projects"]:
            p = document.add_paragraph()
            run = p.add_run(project.get("name", ""))
            run.bold = True

            if project.get("description"):
                document.add_paragraph(project["description"])

            if project.get("technologies"):
                document.add_paragraph("Technologies: " + ", ".join(project["technologies"]))

    # Save to an in-memory buffer instead of a file on disk
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer