from docx import Document
from docx.shared import Pt
from io import BytesIO
from fpdf import FPDF


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


def generate_ats_friendly_pdf(tailored: dict) -> BytesIO:
    """
    Builds an ATS-Friendly PDF resume from the tailored resume data
    and returns it as an in-memory file (BytesIO), ready for download.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)

    def add_heading(text):
        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=11)

    def add_paragraph(text):
        pdf.multi_cell(0, 7, text)
        pdf.ln(2)

    def add_bullet(text):
        pdf.multi_cell(0, 7, f"-  {text}")

    # --- Summary ---
    if tailored.get("summary"):
        add_heading("Professional Summary")
        add_paragraph(tailored["summary"])

    # --- Skills ---
    if tailored.get("skills"):
        add_heading("Skills")
        add_paragraph(", ".join(tailored["skills"]))

    # --- Experience ---
    if tailored.get("experience"):
        add_heading("Experience")
        for job in tailored["experience"]:
            heading_text = f"{job.get('title', '')} - {job.get('company', '')}"
            if job.get("duration"):
                heading_text += f" ({job['duration']})"
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.multi_cell(0, 7, heading_text)
            pdf.set_font("Helvetica", size=11)

            for bullet in job.get("bullets", []):
                add_bullet(bullet)
            pdf.ln(2)

    # --- Education ---
    if tailored.get("education"):
        add_heading("Education")
        for edu in tailored["education"]:
            heading_text = f"{edu.get('degree', '')} - {edu.get('institution', '')}"
            if edu.get("duration"):
                heading_text += f" ({edu['duration']})"
            pdf.multi_cell(0, 7, heading_text)
        pdf.ln(2)

    # --- Projects ---
    if tailored.get("projects"):
        add_heading("Projects")
        for project in tailored["projects"]:
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.multi_cell(0, 7, project.get("name", ""))
            pdf.set_font("Helvetica", size=11)

            if project.get("description"):
                add_paragraph(project["description"])

            if project.get("technologies"):
                add_paragraph("Technologies: " + ", ".join(project["technologies"]))

    # Output as bytes, wrapped in an in-memory buffer
    buffer = BytesIO(pdf.output())
    buffer.seek(0)
    return buffer