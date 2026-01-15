def sanitize_input(text: str) -> str:
    return text.strip().replace("\n", " ")

def enforce_length(text: str, max_len=3000):
    if len(text) > max_len:
        return text[:max_len]
    return text
