import io
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from backend.agent import run_agent

app = FastAPI(title="Sales Proposal AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    client: str
    use_case: str

class ExportRequest(BaseModel):
    proposal: str

@app.post("/run-agent")
def run(req: AgentRequest):
    return run_agent(req.client, req.use_case)

def _create_stateless_pdf(text: str) -> io.BytesIO:
    """Generates PDF directly into memory with word-wrapping, basic markdown, and beautiful Native Tables."""
    
    # Sanitize markdown/unicode characters that Reportlab's Helvetica doesn't support
    replacements = {
        '—': '-', '–': '-', '•': '-', '’': "'", '‘': "'", '“': '"', '”': '"',
        '…': '...', '✔': 'v', '✅': 'v', '▪': '-', '■': '-'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
        
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Convert basic markdown into HTML tags supported by ReportLab Paragraphs
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text) # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)     # Italics
    text = re.sub(r'###\s*(.*)', r'<font size="12"><b>\1</b></font>', text) # H3
    text = re.sub(r'##\s*(.*)', r'<font size="13"><b>\1</b></font>', text)  # H2
    text = re.sub(r'#\s*(.*)', r'<font size="14"><b>\1</b></font>', text)   # H1
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14
    )

    flowables = []
    # Document Title
    flowables.append(Paragraph("<b>Sales Proposal</b>", styles['Heading1']))
    flowables.append(Spacer(1, 10))

    current_paragraph = []
    table_data = []

    def flush_paragraph():
        if current_paragraph:
            text_block = "<br/>".join(current_paragraph)
            flowables.append(Paragraph(text_block, custom_style))
            flowables.append(Spacer(1, 8))
            current_paragraph.clear()

    def flush_table():
        if table_data:
            # Convert text cells to Paragraphs so long text wraps beautifully INSIDE the table cells
            table_flowables = []
            for row in table_data:
                table_flowables.append([Paragraph(cell, custom_style) for cell in row])
                
            t = Table(table_flowables)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke), # Header row styling
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),       # Borders
                ('VALIGN', (0,0), (-1,-1), 'TOP'),                # Align top
                ('PADDING', (0,0), (-1,-1), 6)                    # Cell Padding
            ]))
            flowables.append(t)
            flowables.append(Spacer(1, 12))
            table_data.clear()

    for line in text.split('\n'):
        line = line.strip()
        
        # Detect if line is a markdown table row (starts and ends with |)
        if line.startswith('|') and line.endswith('|'):
            flush_paragraph()
            # Ignore the purely decorative markdown separator rows like |---|---|
            if '|---' in line.replace(' ', ''):
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            table_data.append(cells)
        elif not line:
            # Empty line means break between paragraphs or end of a table
            flush_paragraph()
            flush_table()
        else:
            flush_table()
            current_paragraph.append(line)

    flush_paragraph()
    flush_table()

    doc.build(flowables)
    buffer.seek(0)
    return buffer

@app.post("/export-pdf")
def export_pdf(req: ExportRequest):
    pdf_buffer = _create_stateless_pdf(req.proposal)
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "attachment; filename=Sales_Proposal.pdf"}
    )
