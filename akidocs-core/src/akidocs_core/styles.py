from akidocs_core.style_base import Style, pt_to_mm

pt = pt_to_mm

GENERIC = Style(
    font_family="Times",
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
)

MODERN = Style(
    font_family="Helvetica",
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
)

STYLES = {
    "generic": GENERIC,
    "g": GENERIC,
    "modern": MODERN,
    "m": MODERN,
}
