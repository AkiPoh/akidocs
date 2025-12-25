def tokenize(text: str) -> list:
    if text == "":
        return []

    blocks = text.split("\n\n")
    tokens = []

    for block in blocks:
        block = block.strip()
        if block == "":
            continue

        if block.startswith("#"):
            content = block.lstrip("#").strip()
            tokens.append({"type": "header", "level": 1, "content": content})
        else:
            tokens.append({"type": "paragraph", "content": block})

    return tokens
