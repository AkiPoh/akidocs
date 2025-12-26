from fpdf import FPDF

from akidocs_core.tokens import Header, InlineToken, Italic, Paragraph, Text, Token

# Typography (points - standard typographic unit)
FONT_FAMILY = "Times"
BASE_FONT_SIZE = 12  # in points
HEADER_FONT_SIZES = {1: 24, 2: 20, 3: 16, 4: 14, 5: 12, 6: 11}

# Line height as factor of font size (1.4 = 140% of font size)
HEADER_LINE_HEIGHT_FACTOR = 1.4
PARAGRAPH_LINE_HEIGHT_FACTOR = 1.4

# Vertical spacing after blocks (points)
HEADER_MARGIN_AFTER = 8
PARAGRAPH_MARGIN_AFTER = 4


def _pt_to_mm(pt: float) -> float:
    """Convert points to millimeters. fpdf2 uses mm for spacing but pt for fonts."""
    return pt * 0.352778


def _render_inline_tokens(
    pdf: FPDF,
    tokens: list[InlineToken],
    base_style: str,
    size: float,
    line_height: float,
) -> None:
    for token in tokens:
        match token:
            case Text(content=content):
                pdf.set_font(FONT_FAMILY, style=base_style, size=size)
                pdf.write(line_height, content)
            case Italic(content=content):
                italic_style = "BI" if "B" in base_style else "I"
                pdf.set_font(FONT_FAMILY, style=italic_style, size=size)
                pdf.write(line_height, content)


def _render_header(pdf: FPDF, level: int, content: list[InlineToken]) -> None:
    size = HEADER_FONT_SIZES.get(level, BASE_FONT_SIZE)
    line_height = _pt_to_mm(size * HEADER_LINE_HEIGHT_FACTOR)
    _render_inline_tokens(pdf, content, "B", size, line_height)
    pdf.ln(line_height + _pt_to_mm(HEADER_MARGIN_AFTER))


def _render_paragraph(pdf: FPDF, content: list[InlineToken]) -> None:
    line_height = _pt_to_mm(BASE_FONT_SIZE * PARAGRAPH_LINE_HEIGHT_FACTOR)
    _render_inline_tokens(pdf, content, "", BASE_FONT_SIZE, line_height)
    pdf.ln(line_height + _pt_to_mm(PARAGRAPH_MARGIN_AFTER))


def render_pdf(tokens: list[Token]) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    for token in tokens:
        match token:
            case Header(level=level, content=content):
                _render_header(pdf, level, content)
            case Paragraph(content=content):
                _render_paragraph(pdf, content)

    return bytes(pdf.output())
