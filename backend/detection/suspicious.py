import re

PROMOTIONAL_PHRASES = [
    "buy now",
    "best product ever",
    "must buy",
    "highly recommended",
    "100% guaranteed"
]


def detect_suspicious(review):

    signals = []

    text = review.lower()

    # Check promotional phrases
    for phrase in PROMOTIONAL_PHRASES:
        if phrase in text:
            signals.append("Promotional language detected")
            break

    # Check repeated words
    words = re.findall(r"\b\w+\b", text)

    for word in set(words):
        if words.count(word) >= 4:
            signals.append("Excessive word repetition detected")
            break

    # Check very short reviews
    if len(words) < 4:
        signals.append("Very short review")

    return {
        "suspicious": len(signals) > 0,
        "signals": signals
    }
