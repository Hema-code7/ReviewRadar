
from detection.suspicious import detect_suspicious


def test_promotional_language():
    review = "Best product ever, buy now!"

    result = detect_suspicious(review)

    assert result["suspicious"] == True


def test_repeated_words():
    review = "Good good good good product"

    result = detect_suspicious(review)

    assert result["suspicious"] == True


def test_normal_review():
    review = "The product works well and arrived on time"

    result = detect_suspicious(review)

    assert result["suspicious"] == False