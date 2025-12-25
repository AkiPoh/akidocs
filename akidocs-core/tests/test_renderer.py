from akidocs_core.renderer import render_pdf


def test_render_returns_bytes():
    tokens = [{"type": "paragraph", "content": "Hello"}]
    result = render_pdf(tokens)
    assert isinstance(result, bytes)
    assert len(result) > 0
