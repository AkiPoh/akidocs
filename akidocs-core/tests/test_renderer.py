import pytest

from akidocs_core.renderer import render_pdf
from akidocs_core.tokens import Bold, Header, InlineText, Italic, Paragraph

BOLD = frozenset({Bold()})
ITALIC = frozenset({Italic()})
BOLD_ITALIC = frozenset({Bold(), Italic()})


def assert_valid_pdf_bytes(result: bytes) -> None:
    """Assert that result is non-empty PDF bytes."""
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_returns_bytes():
    tokens = [Paragraph(content=[InlineText(content="Hello")])]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_handles_headers():
    tokens = [
        Header(level=1, content=[InlineText(content="Title")]),
        Paragraph(content=[InlineText(content="Body text")]),
    ]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)


@pytest.mark.parametrize("style", [ITALIC, BOLD, BOLD_ITALIC])
def test_render_handles_styled_text(style):
    tokens = [
        Paragraph(
            content=[
                InlineText(content="hello "),
                InlineText(content="world", styles=style),
            ]
        )
    ]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)
