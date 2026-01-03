from akidocs_core.tokens import Bold, InlineStyles, InlineText, Italic

DELIMITERS: list[tuple[str, frozenset[InlineStyles]]] = [
    ("***", frozenset({Bold(), Italic()})),
    ("**", frozenset({Bold()})),
    ("*", frozenset({Italic()})),
]


def _claimed_by_longer(text: str, delim: str, pos: int) -> bool:
    """Check if a longer delimiter claims this position."""
    for check_delim, _ in DELIMITERS:
        if len(check_delim) <= len(delim):
            continue
        if text[pos : pos + len(check_delim)] != check_delim:
            continue
        if _find_closing(text, check_delim, pos + len(check_delim)) != -1:
            return True
    return False


def _skip_nested_at(text: str, delim: str, pos: int) -> int | None:
    """If a different delimiter opens here and closes, return position after it."""
    for check_delim, _ in DELIMITERS:
        if check_delim == delim:
            continue
        if text[pos : pos + len(check_delim)] != check_delim:
            continue
        close = _find_closing(text, check_delim, pos + len(check_delim))
        if close != -1:
            return close + len(check_delim)
    return None


def _find_closing(text: str, delim: str, start: int) -> int:
    """Find closing delimiter, skipping nested sections."""
    i = start
    while i < len(text):
        if text[i : i + len(delim)] == delim:
            if not _claimed_by_longer(text, delim, i):
                return i

        skipped_to = _skip_nested_at(text, delim, i)
        if skipped_to is not None:
            i = skipped_to
        else:
            i += 1

    return -1


def _find_styled_section(
    text: str, pos: int
) -> tuple[str, frozenset[InlineStyles], int] | None:
    """Find a styled section that STARTS at pos. Returns (delim, inline_styles, end_pos) or None."""
    # Longest delimiter that opened, but failed to close
    longest_failed_opener_len = 0

    # Iterate in correct order, as specified by DELIMITERS
    for delim, inline_styles in DELIMITERS:
        # If current delimiter, does not find match at current position
        if text[pos : pos + len(delim)] != delim:
            continue

        # Search for matching closer delimiter
        content_end_pos = _find_closing(text, delim, pos + len(delim))
        # If none found, record as failed, if longer than previous failed
        if content_end_pos == -1:
            longest_failed_opener_len = max(longest_failed_opener_len, len(delim))
            continue

        # Closer falls within longest failed opener
        # Prevents ** from parsing as italic that wraps nothing
        if longest_failed_opener_len:
            if content_end_pos < pos + longest_failed_opener_len:
                continue

        return delim, inline_styles, content_end_pos

    return None


def tokenize_inline(
    text: str, inherited_styles: frozenset[InlineStyles] = frozenset()
) -> list[InlineText]:
    inline_tokens: list[InlineText] = []
    text_buffer = ""
    pos = 0

    while pos < len(text):
        section = _find_styled_section(text, pos)

        # No match for style in section
        if section is None:
            text_buffer += text[pos]
            pos += 1
            continue

        # Styled section was found, unpack section
        delim, styles, content_end_pos = section

        # Add accumulated text buffer to inline_tokens, and flush text buffer
        if text_buffer:
            inline_tokens.append(
                InlineText(content=text_buffer, styles=inherited_styles)
            )
            text_buffer = ""

        # Extract content between delimiters
        inner_content = text[pos + len(delim) : content_end_pos]
        # Combine new styles and inherited styles
        combined_styles = inherited_styles | styles

        # Recursive call, to parse inner content for nested styles
        if inner_content:
            inner_inline_tokens = tokenize_inline(inner_content, combined_styles)
            inline_tokens.extend(inner_inline_tokens)
        # If section is empty, emit empty token with the styles
        else:
            inline_tokens.append(InlineText(content="", styles=combined_styles))

        # Move position past closing delimiter
        pos = content_end_pos + len(delim)

    # After loop, add accumulated text buffer to inline_tokens, and flush text buffer
    if text_buffer:
        inline_tokens.append(InlineText(content=text_buffer, styles=inherited_styles))

    return inline_tokens
