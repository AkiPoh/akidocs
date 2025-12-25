from fpdf import FPDF

from akidocs_core.tokens import Header, Paragraph

HEADER_FONT_SIZES = {1: 24, 2: 20, 3: 16, 4: 14, 5: 12, 6: 11}


def render_pdf(tokens: list) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    for token in tokens:
        match token:
            case Header(level=level, content=content):
                size = HEADER_FONT_SIZES.get(level, 12)
                pdf.set_font("Times", style="B", size=size)
                pdf.multi_cell(0, size * 0.5, content)
                pdf.ln(4)
            case Paragraph(content=content):
                pdf.set_font("Times", size=12)
                pdf.multi_cell(0, 6, content)
                pdf.ln(2)

    return bytes(pdf.output())
