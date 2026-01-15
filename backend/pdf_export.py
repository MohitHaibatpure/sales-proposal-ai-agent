from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_proposal_pdf(proposal_text: str) -> str:
    """
    Generates a PDF from proposal text and returns file path.
    """

    file_id = f"proposal_{uuid.uuid4().hex}.pdf"
    file_path = EXPORT_DIR / file_id

    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    x_margin = 40
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, "Sales Proposal")
    y -= 30

    c.setFont("Helvetica", 10)

    for line in proposal_text.split("\n"):
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40

        c.drawString(x_margin, y, line)
        y -= 14

    c.save()

    return str(file_path)
