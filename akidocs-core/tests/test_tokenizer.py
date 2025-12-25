from akidocs_core.tokenizer import tokenize


def test_empty_string_returns_empty_list():
    assert tokenize("") == []


def test_plain_paragraph():
    result = tokenize("Hello world")
    assert len(result) == 1
    assert result[0]["type"] == "paragraph"
    assert result[0]["content"] == "Hello world"


def test_header_level_one():
    result = tokenize("# Hello")
    assert len(result) == 1
    assert result[0]["type"] == "header"
    assert result[0]["level"] == 1
    assert result[0]["content"] == "Hello"


def test_multiple_paragraphs():
    result = tokenize("First paragraph\n\nSecond paragraph")
    assert len(result) == 2
    assert result[0]["type"] == "paragraph"
    assert result[0]["content"] == "First paragraph"
    assert result[1]["type"] == "paragraph"
    assert result[1]["content"] == "Second paragraph"


def test_header_levels():
    assert tokenize("# One")[0]["level"] == 1
    assert tokenize("## Two")[0]["level"] == 2
    assert tokenize("### Three")[0]["level"] == 3
