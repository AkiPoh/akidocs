from akidocs_core.renderer import render_pdf
from akidocs_core.tokens import Bold, Header, Italic, Paragraph, Text


def test_render_returns_bytes():
    tokens = [Paragraph(content=[Text("Hello")])]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_handles_headers():
    tokens = [
        Header(level=1, content=[Text(content="Title")]),
        Paragraph(content=[Text(content="Body text")]),
    ]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_handles_italic():
    tokens = [Paragraph(content=[Text(content="hello "), Italic(content="world")])]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_handles_bold():
    tokens = [Paragraph(content=[Text(content="hello "), Bold(content="world")])]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0
