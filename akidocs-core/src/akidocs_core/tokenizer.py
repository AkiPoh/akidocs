from akidocs_core.tokens import Header, Paragraph, Token


def tokenize(text: str) -> list[Token]:
    text = text.replace("\r\n", "\n")

    if text == "":
        return []

    blocks = text.split("\n\n")
    tokens = []

    for block in blocks:
        block = block.strip()
        if block == "":
            continue

        if block.startswith("#"):
            stripped = block.lstrip("#")
            level = len(block) - len(stripped)
            if level <= 6 and (stripped == "" or stripped.startswith(" ")):
                content = stripped.strip()
                tokens.append(Header(level=level, content=content))
            else:
                tokens.append(Paragraph(content=block))
        else:
            tokens.append(Paragraph(content=block))

    return tokens
