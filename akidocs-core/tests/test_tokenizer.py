from akidocs_core.tokenizer import tokenize
from akidocs_core.tokens import Header, InlineText, Italic, Paragraph

ITALIC = frozenset({Italic()})


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
    assert result[0].content == [InlineText(content="Hello world")]


def test_header_level_one():
    result = tokenize("# Hello")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 1
    assert result[0].content == [InlineText(content="Hello")]


def test_multiple_paragraphs():
    result = tokenize("First paragraph\n\nSecond paragraph")
    assert len(result) == 2
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [InlineText(content="First paragraph")]
    assert isinstance(result[1], Paragraph)
    assert result[1].content == [InlineText(content="Second paragraph")]


def test_header_levels():
    assert tokenize("# One")[0].level == 1
    assert tokenize("## Two")[0].level == 2
    assert tokenize("### Three")[0].level == 3
    assert tokenize("#### Four")[0].level == 4
    assert tokenize("##### Five")[0].level == 5
    assert tokenize("###### Six")[0].level == 6


def test_windows_crlf_line_endings():
    result = tokenize("First paragraph\r\n\r\nSecond paragraph")
    assert len(result) == 2
    assert result[0].content == [InlineText(content="First paragraph")]
    assert result[1].content == [InlineText(content="Second paragraph")]


def test_header_requires_space():
    result = tokenize("#NoSpace")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [InlineText(content="#NoSpace")]


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
    assert result[0].content == [InlineText(content="####### Seven hashes")]


def test_single_newline_stays_in_paragraph():
    result = tokenize("Line one\nLine two")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [InlineText(content="Line one\nLine two")]


def test_multiple_blank_lines():
    result = tokenize("First\n\n\n\nSecond")
    assert len(result) == 2
    assert result[0].content == [InlineText(content="First")]
    assert result[1].content == [InlineText(content="Second")]


def test_leading_trailing_whitespace_ignored():
    result = tokenize("\n\nContent\n\n")
    assert len(result) == 1
    assert result[0].content == [InlineText(content="Content")]


def test_paragraph_with_italic():
    result = tokenize("hello *world*")
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)
    assert result[0].content == [
        InlineText(content="hello "),
        InlineText(content="world", styles=ITALIC),
    ]


def test_header_with_tab_separator():
    result = tokenize("#\tHello")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 1
    assert result[0].content == [InlineText(content="Hello")]


def test_header_with_mixed_whitespace_separator():
    result = tokenize("##   \t\t   \t\t   Mixed")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 2
    assert result[0].content == [InlineText(content="Mixed")]


def test_header_with_pound_signs():
    result = tokenize("#### #Header# ## # # Continues##")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 4
    assert result[0].content == [InlineText(content="#Header# ## # # Continues##")]


def test_header_trailing_pound_signs_trimmed():
    result = tokenize("###### Header# ##  ###")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 6
    assert result[0].content == [InlineText(content="Header# ##")]


def test_header_trailing_pound_signs_trimmed_tab():
    result = tokenize("###### Header# ##\t\t###")
    assert len(result) == 1
    assert isinstance(result[0], Header)
    assert result[0].level == 6
    assert result[0].content == [InlineText(content="Header# ##")]
