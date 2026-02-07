import pytest

from akidocs_core.renderer import render_pdf
from akidocs_core.tokens import Bold, Code, Header, InlineText, Italic, Paragraph

BOLD = frozenset({Bold()})
ITALIC = frozenset({Italic()})
BOLD_ITALIC = frozenset({Bold(), Italic()})
CODE = frozenset({Code()})
BOLD_CODE = frozenset({Bold(), Code()})
ITALIC_CODE = frozenset({Italic(), Code()})


def assert_valid_pdf_bytes(result: bytes) -> None:
    """Assert that result is non-empty PDF bytes."""
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_returns_bytes():
    tokens = [Paragraph(content=[InlineText(content="Hello")])]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)


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


def test_render_handles_hard_break():
    tokens = [
        Paragraph(
            content=[
                InlineText(content="Line one\nLine two"),
            ]
        )
    ]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)


def test_render_handles_code_span():
    tokens = [
        Paragraph(
            content=[
                InlineText(content="hello "),
                InlineText(content="world", styles=CODE),
            ]
        )
    ]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)


@pytest.mark.parametrize("style", [CODE, BOLD_CODE, ITALIC_CODE])
def test_render_handles_code_with_styles(style):
    tokens = [
        Paragraph(
            content=[
                InlineText(content="styled code", styles=style),
            ]
        )
    ]
    result = render_pdf(tokens)
    assert_valid_pdf_bytes(result)
