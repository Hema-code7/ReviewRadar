
POSITIVE_WORDS = [
    "excellent", "good", "great", "amazing",
    "love", "perfect", "wonderful", "best"
]

NEGATIVE_WORDS = [
    "bad", "poor", "terrible", "worst",
    "hate", "disappointed", "broken", "useless"
]


def check_consistency(review, rating):

    text = review.lower()

    positive_count = sum(text.count(word) for word in POSITIVE_WORDS)
    negative_count = sum(text.count(word) for word in NEGATIVE_WORDS)

    if rating >= 4 and negative_count > positive_count:
        return {
            "consistent": False,
            "signal": "Negative text with high rating"
        }

    elif rating <= 2 and positive_count > negative_count:
        return {
            "consistent": False,
            "signal": "Positive text with low rating"
        }

    return {
        "consistent": True,
        "signal": "No rating-text mismatch detected"
    }

