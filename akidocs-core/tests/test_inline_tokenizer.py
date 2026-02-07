from akidocs_core.inline_tokenizer import tokenize_inline
from akidocs_core.tokens import Bold, Code, InlineText, Italic

BOLD = frozenset({Bold()})
ITALIC = frozenset({Italic()})
BOLD_ITALIC = frozenset({Bold(), Italic()})
CODE = frozenset({Code()})
BOLD_CODE = frozenset({Bold(), Code()})
ITALIC_CODE = frozenset({Italic(), Code()})


def test_plain_text():
    result = tokenize_inline("hello world")
    assert result == [InlineText(content="hello world")]


def test_italic_only():
    result = tokenize_inline("*hello*")
    assert result == [InlineText(content="hello", styles=ITALIC)]


def test_text_then_italic():
    result = tokenize_inline("hello *world*")
    assert result == [
        InlineText(content="hello "),
        InlineText(content="world", styles=ITALIC),
    ]


def test_bold_only():
    result = tokenize_inline("**hello**")
    assert result == [InlineText(content="hello", styles=BOLD)]


def test_text_then_bold():
    result = tokenize_inline("hello **world**")
    assert result == [
        InlineText(content="hello "),
        InlineText(content="world", styles=BOLD),
    ]


def test_bold_italic():
    result = tokenize_inline("***bold italic***")
    assert result == [InlineText(content="bold italic", styles=BOLD_ITALIC)]


def test_bold_containing_italic():
    result = tokenize_inline("**bold *and italic* text**")
    assert result == [
        InlineText(content="bold ", styles=BOLD),
        InlineText(content="and italic", styles=BOLD_ITALIC),
        InlineText(content=" text", styles=BOLD),
    ]


def test_italic_containing_bold():
    result = tokenize_inline("*italic **and bold** text*")
    assert result == [
        InlineText(content="italic ", styles=ITALIC),
        InlineText(content="and bold", styles=BOLD_ITALIC),
        InlineText(content=" text", styles=ITALIC),
    ]


def test_adjacent_styles():
    result = tokenize_inline("**bold***italic*")
    assert result == [
        InlineText(content="bold", styles=BOLD),
        InlineText(content="italic", styles=ITALIC),
    ]


def test_unclosed_bold():
    result = tokenize_inline("**bold without closing")
    assert result == [InlineText(content="**bold without closing")]


def test_empty_bold():
    result = tokenize_inline("****")
    assert result == [InlineText(content="", styles=BOLD)]


def test_code_span():
    result = tokenize_inline("`hello`")
    assert result == [InlineText(content="hello", styles=CODE)]


def test_text_then_code_span():
    result = tokenize_inline("hello `world`")
    assert result == [
        InlineText(content="hello "),
        InlineText(content="world", styles=CODE),
    ]


def test_code_span_preserves_asterisks():
    result = tokenize_inline("`**not bold**`")
    assert result == [InlineText(content="**not bold**", styles=CODE)]


def test_code_span_in_bold():
    result = tokenize_inline("**bold `code` text**")
    assert result == [
        InlineText(content="bold ", styles=BOLD),
        InlineText(content="code", styles=BOLD_CODE),
        InlineText(content=" text", styles=BOLD),
    ]


def test_unclosed_backtick():
    result = tokenize_inline("`unclosed")
    assert result == [InlineText(content="`unclosed")]


def test_empty_code_span():
    result = tokenize_inline("``")
    assert result == [InlineText(content="", styles=CODE)]


def test_code_span_adjacent_to_bold():
    result = tokenize_inline("**bold**`code`")
    assert result == [
        InlineText(content="bold", styles=BOLD),
        InlineText(content="code", styles=CODE),
    ]


def test_multiple_code_spans():
    result = tokenize_inline("`one` and `two`")
    assert result == [
        InlineText(content="one", styles=CODE),
        InlineText(content=" and "),
        InlineText(content="two", styles=CODE),
    ]


def test_italic_containing_code_with_asterisks():
    result = tokenize_inline("*italic `**` end*")
    assert result == [
        InlineText(content="italic ", styles=ITALIC),
        InlineText(content="**", styles=ITALIC_CODE),
        InlineText(content=" end", styles=ITALIC),
    ]
