from akidocs_core.style_base import Style, pt_to_mm

pt = pt_to_mm

GENERIC = Style(
    name="generic",
    font_family="Helvetica",
    header_base_font_style="B",  # "", "B", "I", or "BI"
    paragraph_base_font_style="",
    base_font_size=pt(11),
    header_font_sizes={
        1: pt(28),
        2: pt(22),
        3: pt(16),
        4: pt(13),
        5: pt(11),
        6: pt(10),
    },
    header_line_height_factor=1.3,
    paragraph_line_height_factor=1.6,
    header_margin_after=pt(12),
    paragraph_margin_after=pt(8),
    page_margin_top=20.0,
    page_margin_right=25.0,
    page_margin_bottom=20.0,
    page_margin_left=25.0,
)

TIMES = Style(
    name="times",
    font_family="Times",
    header_base_font_style="B",
    paragraph_base_font_style="",
    base_font_size=pt(12),
    header_font_sizes={
        1: pt(24),
        2: pt(20),
        3: pt(16),
        4: pt(14),
        5: pt(12),
        6: pt(11),
    },
    header_line_height_factor=1.4,
    paragraph_line_height_factor=1.4,
    header_margin_after=pt(8),
    paragraph_margin_after=pt(4),
    page_margin_top=20.0,
    page_margin_right=25.0,
    page_margin_bottom=20.0,
    page_margin_left=25.0,
)

REGARD = Style(
    name="regard",
    font_family="Courier",
    header_base_font_style="B",
    paragraph_base_font_style="B",
    base_font_size=pt(12),
    header_font_sizes={
        1: pt(14),
        2: pt(13),
        3: pt(12),
        4: pt(12),
        5: pt(12),
        6: pt(12),
    },
    header_line_height_factor=1.8,
    paragraph_line_height_factor=2.0,
    header_margin_after=pt(16),
    paragraph_margin_after=pt(16),
    page_margin_top=60.0,
    page_margin_right=50.0,
    page_margin_bottom=60.0,
    page_margin_left=50.0,
)

STYLES = {
    "generic": GENERIC,
    "g": GENERIC,
    "times": TIMES,
    "t": TIMES,
    "regard": REGARD,
    "r": REGARD,
}
