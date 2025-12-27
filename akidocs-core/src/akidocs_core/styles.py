from akidocs_core.style_base import Style, pt_to_mm

pt = pt_to_mm  # Alias for brevity

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
