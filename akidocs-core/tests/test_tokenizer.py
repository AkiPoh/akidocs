from akidocs_core.tokenizer import tokenize
from akidocs_core.tokens import Header, Paragraph


def test_empty_string_returns_empty_list():
    assert tokenize("") == []


def test_plain_paragraph():
    result = tokenize("Hello world")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == "Hello world"


def test_header_level_one():
    result = tokenize("# Hello")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 1
    assert result[0].content == "Hello"


def test_multiple_paragraphs():
    result = tokenize("First paragraph\n\nSecond paragraph")
    assert len(result) == 2
    assert isinstance(result[0], Paragraph)
    assert result[0].content == "First paragraph"
    assert isinstance(result[1], Paragraph)
    assert result[1].content == "Second paragraph"


def test_header_levels():
    assert tokenize("# One")[0].level == 1
    assert tokenize("## Two")[0].level == 2
    assert tokenize("### Three")[0].level == 3


def test_windows_line_endings():
    result = tokenize("First paragraph\r\n\r\nSecond paragraph")
    assert len(result) == 2
    assert result[0].content == "First paragraph"
    assert result[1].content == "Second paragraph"


def test_header_requires_space():
    result = tokenize("#NoSpace")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == "#NoSpace"


def test_header_empty_content():
    result = tokenize("##")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 2
    assert result[0].content == ""


def test_header_level_seven_becomes_paragraph():
    result = tokenize("####### Seven hashes")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == "####### Seven hashes"
