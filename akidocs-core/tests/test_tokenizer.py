from akidocs_core.tokenizer import tokenize
from akidocs_core.tokens import Header, Italic, Paragraph, Text


def test_empty_string_returns_empty_list():
    assert tokenize("") == []


def test_whitespace_only_returns_empty_list():
    assert tokenize("   ") == []
    assert tokenize("\n\n") == []
    assert tokenize("  \n\n  ") == []


def test_plain_paragraph():
    result = tokenize("Hello world")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="Hello world")]


def test_header_level_one():
    result = tokenize("# Hello")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 1
    assert result[0].content == [Text(content="Hello")]


def test_multiple_paragraphs():
    result = tokenize("First paragraph\n\nSecond paragraph")
    assert len(result) == 2
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="First paragraph")]
    assert isinstance(result[1], Paragraph)
    assert result[1].content == [Text(content="Second paragraph")]


def test_header_levels():
    assert tokenize("# One")[0].level == 1
    assert tokenize("## Two")[0].level == 2
    assert tokenize("### Three")[0].level == 3


def test_windows_line_endings():
    result = tokenize("First paragraph\r\n\r\nSecond paragraph")
    assert len(result) == 2
    assert result[0].content == [Text(content="First paragraph")]
    assert result[1].content == [Text(content="Second paragraph")]


def test_header_requires_space():
    result = tokenize("#NoSpace")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="#NoSpace")]


def test_header_empty_content():
    result = tokenize("##")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 2
    assert result[0].content == []


def test_header_level_seven_becomes_paragraph():
    result = tokenize("####### Seven hashes")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="####### Seven hashes")]


def test_single_newline_stays_in_paragraph():
    result = tokenize("Line one\nLine two")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="Line one\nLine two")]


def test_multiple_blank_lines():
    result = tokenize("First\n\n\n\nSecond")
    assert len(result) == 2
    assert result[0].content == [Text(content="First")]
    assert result[1].content == [Text(content="Second")]


def test_leading_trailing_whitespace_ignored():
    result = tokenize("\n\nContent\n\n")
    assert len(result) == 1
    assert result[0].content == [Text(content="Content")]


def test_paragraph_with_italic():
    result = tokenize("hello *world*")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [Text(content="hello "), Italic(content="world")]
