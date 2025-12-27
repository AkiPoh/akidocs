from dataclasses import dataclass


def pt_to_mm(pt: float) -> float:
    """Convert points to millimeters."""
    return pt * 0.352778


def mm_to_pt(mm: float) -> float:
    """Convert millimeters to points."""
    return mm / 0.352778


@dataclass(frozen=True)
class Style:
    """Document style configuration. All dimensions in millimeters."""

    font_family: str
    base_font_style: str  # "", "B", "I", or "BI"
    base_font_size: float
    header_font_sizes: dict[int, float]
    header_line_height_factor: float
    paragraph_line_height_factor: float
    header_margin_after: float
    paragraph_margin_after: float
    page_margin_top: float
    page_margin_right: float
    page_margin_bottom: float
    page_margin_left: float
