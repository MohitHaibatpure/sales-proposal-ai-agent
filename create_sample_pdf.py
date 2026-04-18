from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_sample_pdf():
    doc = SimpleDocTemplate("sample_client_context.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    
    flowables = []
    
    # Title
    flowables.append(Paragraph("<b>Client Brief & Internal Context: TechVista Solutions</b>", styles['Heading1']))
    flowables.append(Spacer(1, 12))
    
    # Content
    content = [
        "<b>Company Background:</b>",
        "TechVista Solutions is a rapidly growing enterprise manufacturing company specializing in industrial IoT devices. Over the last three years, they have expanded across 14 different countries in Europe and North America.",
        "<b>Current Architecture & Pain Points:</b>",
        "Currently, their manufacturing plants generate over 500TB of telemetry data daily. However, their existing on-premise data centers are struggling to keep up with the processing load resulting in downtime, delayed alerts, and high maintenance costs.",
        "The current monolithic architecture prevents them from deploying real-time predictive maintenance features. Machine failures often go unnoticed until standard scheduled checks, costing the business roughly $2.4M annually in unplanned downtime.",
        "<b>Project Goals:</b>",
        "TechVista is seeking a complete digital transformation. They want to migrate to a highly scalable, cloud-native analytics platform (preferably on AWS). They need microservices architecture to process data streams in real-time, generate predictive maintenance alerts, and provide executives with real-time dashboards via QuickSight.",
        "<b>Key Requirements:</b>",
        "- High Availability (HA) across multiple geographical regions.",
        "- Complete data security compliance including end-to-end encryption and IAM role-based access control.",
        "- Integration with Kinesis Data Streams for data ingestion.",
        "<b>Budget Expectations:</b>",
        "The executive board has earmarked approximately $3M for the entire migration and build phase, with an expected timeline of 6-8 months for minimum viable product rollout."
    ]
    
    for text in content:
        flowables.append(Paragraph(text, styles['Normal']))
        flowables.append(Spacer(1, 8))
        
    doc.build(flowables)
    print("Created sample_client_context.pdf")

if __name__ == "__main__":
    create_sample_pdf()
