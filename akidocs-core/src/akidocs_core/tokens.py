from dataclasses import dataclass


class InlineStyles:
    """Marker base class for inline styles."""

    pass


@dataclass(frozen=True)
class Bold(InlineStyles):
    pass


@dataclass(frozen=True)
class Italic(InlineStyles):
    pass


@dataclass
class InlineText:
    content: str
    styles: frozenset[InlineStyles] = frozenset()


@dataclass
class Header:
    level: int
    content: list[InlineText]


@dataclass
class Paragraph:
    content: list[InlineText]


Token = Header | Paragraph
