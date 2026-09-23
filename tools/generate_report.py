"""Gera o PDF final das respostas a partir de RESPOSTAS.md."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "RESPOSTAS.md"
OUTPUT = ROOT / "output" / "pdf" / "Respostas_Atividade_Avaliativa_Design_Patterns.pdf"


def normalize(text: str) -> str:
    """Evita caracteres de hífen que podem renderizar de forma inconsistente."""
    return (
        text.replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )


def inline_markup(text: str) -> str:
    text = html.escape(normalize(text.strip()))
    text = re.sub(r"`([^`]+)`", r'<font name="DejaVuMono">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def register_fonts() -> None:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("DejaVu", font_dir / "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", font_dir / "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVuMono", font_dir / "DejaVuSansMono.ttf"))


def build_styles():
    base = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName="DejaVu",
        fontSize=9.0,
        leading=12.0,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#263238"),
        spaceAfter=5,
        allowWidows=0,
        allowOrphans=0,
    )
    return {
        "body": body,
        "h1": ParagraphStyle(
            "H1",
            parent=body,
            fontName="DejaVu-Bold",
            fontSize=17,
            leading=21,
            textColor=colors.HexColor("#17324D"),
            spaceBefore=4,
            spaceAfter=12,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=body,
            fontName="DejaVu-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1E5B75"),
            spaceBefore=9,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=body,
            fontName="DejaVu-Bold",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#365B6D"),
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=body,
            alignment=TA_LEFT,
            leftIndent=2,
            spaceAfter=2,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="DejaVuMono",
            fontSize=7.8,
            leading=10.5,
            leftIndent=8,
            rightIndent=8,
            textColor=colors.HexColor("#20313A"),
            backColor=colors.HexColor("#F1F5F7"),
            borderColor=colors.HexColor("#D6E0E5"),
            borderWidth=0.5,
            borderPadding=7,
            spaceBefore=4,
            spaceAfter=9,
        ),
    }


def markdown_story(markdown: str, styles: dict[str, ParagraphStyle]):
    lines = normalize(markdown).splitlines()
    story = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    started_content = False

    def flush_paragraph() -> None:
        if paragraph:
            raw_text = " ".join(paragraph)
            style = styles["bullet"] if raw_text.startswith("Arquivo `tests/") else styles["body"]
            story.append(Paragraph(inline_markup(raw_text), style))
            paragraph.clear()

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not started_content:
            if stripped.startswith("## Estrutura da solução"):
                started_content = True
            else:
                index += 1
                continue

        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["code"]))
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        heading = re.match(r"^(#{2,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            title = heading.group(2)
            if (
                level == 2
                and re.match(r"\d+\s+-", title)
                and not title.startswith("7 -")
                and story
            ):
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(title), styles[f"h{level - 1}"]))
            index += 1
            continue

        if stripped == "---":
            flush_paragraph()
            story.append(Spacer(1, 5))
            index += 1
            continue

        if stripped.startswith("* "):
            flush_paragraph()
            items = []
            while index < len(lines) and lines[index].strip().startswith("* "):
                item_text = lines[index].strip()[2:]
                items.append(ListItem(Paragraph(inline_markup(item_text), styles["bullet"])))
                index += 1
            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    bulletFontName="DejaVu",
                    bulletFontSize=7,
                    leftIndent=16,
                    bulletIndent=4,
                    spaceAfter=7,
                )
            )
            continue

        if not stripped:
            flush_paragraph()
        elif stripped.startswith(">"):
            flush_paragraph()
        else:
            paragraph.append(stripped)
        index += 1

    flush_paragraph()
    return story


def draw_first_page(canvas, document) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#17324D"))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu-Bold", 24)
    canvas.drawCentredString(A4[0] / 2, 20.7 * cm, "Atividade Avaliativa")
    canvas.setFont("DejaVu-Bold", 18)
    canvas.drawCentredString(A4[0] / 2, 19.4 * cm, "Design Patterns em Python")
    canvas.setStrokeColor(colors.HexColor("#72B7D2"))
    canvas.setLineWidth(2)
    canvas.line(5.1 * cm, 18.5 * cm, 15.9 * cm, 18.5 * cm)
    canvas.setFont("DejaVu", 12)
    canvas.drawCentredString(A4[0] / 2, 16.6 * cm, "Sistema de pedidos")
    canvas.setFont("DejaVu", 11)
    canvas.drawCentredString(A4[0] / 2, 12.5 * cm, "Isaías Gouvêa Gonçalves")
    canvas.drawCentredString(A4[0] / 2, 11.7 * cm, "Mateus Mourão")
    canvas.setFont("DejaVu", 9)
    canvas.setFillColor(colors.HexColor("#D8E8EF"))
    canvas.drawCentredString(A4[0] / 2, 3.0 * cm, "Engenharia de Software - 2026")
    canvas.restoreState()


def draw_later_pages(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#BDD0D8"))
    canvas.setLineWidth(0.5)
    canvas.line(2.0 * cm, height - 1.4 * cm, width - 2.0 * cm, height - 1.4 * cm)
    canvas.setFillColor(colors.HexColor("#526A75"))
    canvas.setFont("DejaVu", 7.5)
    canvas.drawString(2.0 * cm, height - 1.15 * cm, "Atividade Avaliativa - Design Patterns em Python")
    canvas.drawRightString(width - 2.0 * cm, 1.15 * cm, f"Página {document.page}")
    canvas.restoreState()


def main() -> None:
    register_fonts()
    styles = build_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2.0 * cm,
        leftMargin=2.0 * cm,
        topMargin=1.9 * cm,
        bottomMargin=1.8 * cm,
        title="Respostas da Atividade Avaliativa - Design Patterns em Python",
        author="Isaías Gouvêa Gonçalves e Mateus Mourão",
        subject="Engenharia de Software",
    )
    story = [Spacer(1, 24.5 * cm), PageBreak()]
    story.extend(markdown_story(SOURCE.read_text(encoding="utf-8"), styles))
    document.build(story, onFirstPage=draw_first_page, onLaterPages=draw_later_pages)
    print(OUTPUT)


if __name__ == "__main__":
    main()
