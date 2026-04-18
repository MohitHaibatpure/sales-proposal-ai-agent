import io
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def create_pdf(text: str) -> bytes:
    replacements = {
        '—': '-', '–': '-', '•': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '…': '...', '✔': 'v',
        '✅': 'v', '▪': '-', '■': '-',
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)

    text = text.encode('ascii', 'ignore').decode('ascii')

    # Convert markdown to ReportLab-compatible HTML tags
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'###\s*(.*)', r'<font size="12"><b>\1</b></font>', text)
    text = re.sub(r'##\s*(.*)', r'<font size="13"><b>\1</b></font>', text)
    text = re.sub(r'#\s*(.*)', r'<font size="14"><b>\1</b></font>', text)

    # Build PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40,
    )
    styles = getSampleStyleSheet()

    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
    )

    flowables = []
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
            table_flowables = []
            for row in table_data:
                table_flowables.append(
                    [Paragraph(cell, custom_style) for cell in row]
                )

            t = Table(table_flowables)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            flowables.append(t)
            flowables.append(Spacer(1, 12))
            table_data.clear()

    for line in text.split('\n'):
        line = line.strip()

        if line.startswith('|') and line.endswith('|'):
            flush_paragraph()
            if '|---' in line.replace(' ', ''):
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            table_data.append(cells)
        elif not line:
            flush_paragraph()
            flush_table()
        else:
            flush_table()
            current_paragraph.append(line)

    flush_paragraph()
    flush_table()

    doc.build(flowables)
    buffer.seek(0)
    return buffer.getvalue()
