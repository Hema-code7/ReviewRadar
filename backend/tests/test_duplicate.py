from detection.duplicate import find_duplicates


def test_exact_duplicates():
    reviews = [
        "Excellent product and good quality",
        "Excellent product and good quality"
    ]

    result = find_duplicates(reviews)

    assert len(result) == 1


def test_different_reviews():
    reviews = [
        "Excellent product",
        "Terrible product"
    ]

    result = find_duplicates(reviews)

    assert len(result) == 0


def test_single_review():
    reviews = ["Excellent product"]

    result = find_duplicates(reviews)

    assert result == []
