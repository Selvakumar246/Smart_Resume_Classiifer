from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import get_settings


def generate_pdf(analysis_id: str, filename: str, result: dict) -> Path:
    settings = get_settings()
    report_dir = Path(settings.reports_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"smart-resume-report-{analysis_id}.pdf"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Hero", parent=styles["Title"], fontSize=24, leading=29, textColor=colors.HexColor("#172554"), spaceAfter=10))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=15, leading=19, textColor=colors.HexColor("#1d4ed8"), spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=12, textColor=colors.HexColor("#475569")))

    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    story = [
        Paragraph("Smart Resume Classification", styles["Hero"]),
        Paragraph(f"AI-assisted resume report for <b>{filename}</b>", styles["BodyText"]),
        Spacer(1, 7 * mm),
    ]

    top = result["classification"]["top_categories"]
    story.append(Paragraph("Classification", styles["Section"]))
    table_data = [["Career category", "Confidence", "Evidence"]]
    for item in top:
        table_data.append([item["category"], f"{item['confidence']}%", ", ".join(item["evidence"]) or "Semantic match"])
    table = Table(table_data, colWidths=[48 * mm, 25 * mm, 95 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    ats = result["ats"]
    story.append(Paragraph(f"ATS score: {ats['overall_score']}/100", styles["Section"]))
    score_data = [[key.replace("_", " ").title(), value] for key, value in ats["scores"].items()]
    score_table = Table(score_data, colWidths=[80 * mm, 28 * mm])
    score_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#cbd5e1")), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eff6ff")), ("FONTSIZE", (0, 0), (-1, -1), 9), ("PADDING", (0, 0), (-1, -1), 6)]))
    story.append(score_table)
    story.append(Spacer(1, 4 * mm))
    for deduction in ats["deductions"]:
        story.append(Paragraph(f"• {deduction}", styles["Small"]))

    story.append(PageBreak())
    story.append(Paragraph("Skill gap and recommendations", styles["Section"]))
    detected = result["skills"]["detected"]
    story.append(Paragraph(f"<b>Detected skills:</b> {', '.join(detected) if detected else 'No taxonomy skills detected'}", styles["BodyText"]))
    story.append(Spacer(1, 3 * mm))
    gap_data = [["Skill", "Priority", "Difficulty", "Learning time"]]
    for gap in result["skills"]["gaps"]:
        gap_data.append([gap["skill"], gap["priority"], gap["difficulty"], gap["estimated_learning_time"]])
    if len(gap_data) > 1:
        gap_table = Table(gap_data, colWidths=[55 * mm, 30 * mm, 38 * mm, 42 * mm], repeatRows=1)
        gap_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#cbd5e1")), ("FONTSIZE", (0, 0), (-1, -1), 8), ("PADDING", (0, 0), (-1, -1), 6)]))
        story.append(gap_table)

    story.append(Paragraph("Priority improvements", styles["Section"]))
    for recommendation in result["improvements"]["recommendations"]:
        story.append(Paragraph(f"• {recommendation}", styles["BodyText"]))

    if result.get("job_match"):
        match = result["job_match"]
        story.append(Paragraph(f"Job description match: {match['match_score']}%", styles["Section"]))
        story.append(Paragraph(f"<b>Matched:</b> {', '.join(match['matched_keywords']) or 'No taxonomy keywords'}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Missing:</b> {', '.join(match['missing_keywords']) or 'No major taxonomy gaps'}", styles["BodyText"]))

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(result["classification"]["disclaimer"], styles["Small"]))
    doc.build(story)
    return path
