from akidocs_core.inline_tokenizer import tokenize_inline
from akidocs_core.tokens import Bold, InlineText, Italic

BOLD = frozenset({Bold()})
ITALIC = frozenset({Italic()})
BOLD_ITALIC = frozenset({Bold(), Italic()})


def test_plain_text():
    result = tokenize_inline("hello world")
    assert result == [InlineText(content="hello world")]


def test_italic_only():
    result = tokenize_inline("*hello*")
    assert result == [InlineText(content="hello", styles=frozenset({Italic()}))]


def test_text_then_italic():
    result = tokenize_inline("hello *world*")
    assert result == [
        InlineText(content="hello "),
        InlineText(content="world", styles=frozenset({Italic()})),
    ]


def test_bold_only():
    result = tokenize_inline("**hello**")
    assert result == [InlineText(content="hello", styles=BOLD)]


def test_text_then_bold():
    result = tokenize_inline("hello **world**")
    assert result == [
        InlineText(content="hello "),
        InlineText(content="world", styles=frozenset({Bold()})),
    ]


def test_bold_italic():
    result = tokenize_inline("***hello***")
    assert len(result) == 1
    assert result[0].content == "hello"
    assert Bold() in result[0].styles
    assert Italic() in result[0].styles


def test_bold_containing_italic():
    result = tokenize_inline("**bold *and italic* text**")
    assert len(result) == 3
    assert result[0] == InlineText(content="bold ", styles=frozenset({Bold()}))
    assert result[1] == InlineText(
        content="and italic", styles=frozenset({Bold(), Italic()})
    )
    assert result[2] == InlineText(content=" text", styles=frozenset({Bold()}))


def test_italic_containing_bold():
    result = tokenize_inline("*italic **and bold** text*")
    assert len(result) == 3
    assert result[0] == InlineText(content="italic ", styles=frozenset({Italic()}))
    assert result[1] == InlineText(
        content="and bold", styles=frozenset({Italic(), Bold()})
    )
    assert result[2] == InlineText(content=" text", styles=frozenset({Italic()}))


def test_adjacent_styles():
    result = tokenize_inline("**bold***italic*")
    assert len(result) == 2
    assert result[0] == InlineText(content="bold", styles=frozenset({Bold()}))
    assert result[1] == InlineText(content="italic", styles=frozenset({Italic()}))


def test_unclosed_bold():
    result = tokenize_inline("**bold without closing")
    assert result == [InlineText(content="**bold without closing")]


def test_empty_bold():
    result = tokenize_inline("****")
    assert result == [InlineText(content="", styles=frozenset({Bold()}))]


def test_triple_nested():
    result = tokenize_inline("***bold italic***")
    assert len(result) == 1
    assert result[0].content == "bold italic"
    assert Bold() in result[0].styles
    assert Italic() in result[0].styles
