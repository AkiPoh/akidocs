from fpdf import FPDF


def render_pdf(tokens: list) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    for token in tokens:
        if token["type"] == "paragraph":
            pdf.multi_cell(0, 10, token["content"])

    return bytes(pdf.output())
