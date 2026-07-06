import re

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions?",
    r"forget\s+(all\s+)?previous\s+instructions?",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(your\s+)?system\s+prompt",
    r"print\s+(your\s+)?system\s+prompt",
    r"show\s+hidden\s+prompt",
    r"developer\s+instructions?",
    r"act\s+as\s+(the\s+)?developer",
    r"bypass\s+safety",
    r"disable\s+safety",
]

def contains_prompt_injection(message: str) -> bool:
    """
    Returns True if the message appears to contain
    a prompt injection attempt.
    """
    message = message.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, message):
            return True

    return False