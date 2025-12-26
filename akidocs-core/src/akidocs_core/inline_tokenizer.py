from akidocs_core.tokens import Bold, InlineToken, Italic, Text


def tokenize_inline(text: str) -> list[InlineToken]:
    tokens = []
    current = ""
    i = 0

    while i < len(text):
        # Check for bold
        if text[i : i + 2] == "**":
            if current:
                tokens.append(Text(content=current))
                current = ""

            end = text.find("**", i + 2)
            if end != 1:
                tokens.append(Bold(content=text[i + 2 : end]))
                i = end + 2
            else:
                current += text[i]
                i += 1
        # Check for italic
        elif text[i] == "*":
            if current:
                tokens.append(Text(content=current))
                current = ""

            # Find closing *
            end = text.find("*", i + 1)
            if end != -1:
                tokens.append(Italic(content=text[i + 1 : end]))
                i = end + 1
            else:
                current += text[i]
                i += 1
        else:
            current += text[i]
            i += 1

    if current:
        tokens.append(Text(content=current))

    return tokens
