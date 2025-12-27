from fpdf import FPDF

from akidocs_core.style_base import Style, mm_to_pt
from akidocs_core.styles import GENERIC
from akidocs_core.tokens import (
    Bold,
    Header,
    InlineText,
    Italic,
    Paragraph,
    Token,
)


def _render_inline_tokens(
    pdf: FPDF,
    tokens: list[InlineText],
    base_style: str,
    size_pt: float,
    line_height: float,
    font_family: str,
) -> None:
    for token in tokens:
        style = base_style
        if Bold() in token.styles:
            style += "B"
        if Italic() in token.styles:
            style += "I"
        style = "".join(sorted(set(style)))
        pdf.set_font(font_family, style=style, size=size_pt)
        pdf.write(line_height, token.content)


def _render_header(
    pdf: FPDF, level: int, content: list[InlineText], style: Style
) -> None:
    size_mm = style.header_font_sizes.get(level, style.base_font_size)
    size_pt = mm_to_pt(size_mm)
    line_height = size_mm * style.header_line_height_factor
    header_base = style.base_font_style + "B"
    _render_inline_tokens(
        pdf, content, header_base, size_pt, line_height, style.font_family
    )
    pdf.ln(line_height + style.header_margin_after)


def _render_paragraph(pdf: FPDF, content: list[InlineText], style: Style) -> None:
    size_pt = mm_to_pt(style.base_font_size)
    line_height = style.base_font_size * style.paragraph_line_height_factor
    _render_inline_tokens(
        pdf, content, style.base_font_style, size_pt, line_height, style.font_family
    )
    pdf.ln(line_height + style.paragraph_margin_after)


def render_pdf(tokens: list[Token], style: Style = GENERIC) -> bytes:
    pdf = FPDF()
    pdf.set_margins(
        style.page_margin_left, style.page_margin_top, style.page_margin_right
    )
    pdf.set_auto_page_break(auto=True, margin=style.page_margin_bottom)
    pdf.add_page()

    for token in tokens:
        match token:
            case Header(level=level, content=content):
                _render_header(pdf, level, content, style)
            case Paragraph(content=content):
                _render_paragraph(pdf, content, style)

    return bytes(pdf.output())
