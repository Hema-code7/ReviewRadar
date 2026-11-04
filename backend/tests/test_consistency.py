
from detection.consistency import check_consistency


def test_negative_review_high_rating():
    result = check_consistency(
        "Terrible quality and very poor product", 5
    )
    assert result["consistent"] == False


def test_positive_review_low_rating():
    result = check_consistency(
        "Excellent product, amazing quality", 1
    )
    assert result["consistent"] == False


def test_matching_review_and_rating():
    result = check_consistency(
        "Excellent product, very good quality", 5
    )
    assert result["consistent"] == True
