
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# Test 1: Single review analysis

def test_single_review():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": [
                "This product is excellent and works perfectly."
            ],
            "ratings": [5]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_reviews"] == 1
    assert len(data["review_analysis"]) == 1
    assert "ai_detection" in data["review_analysis"][0]


# Test 2: Multiple review analysis

def test_multiple_reviews():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": [
                "This product is excellent and works perfectly.",
                "The product is terrible and completely useless."
            ],
            "ratings": [5, 1]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_reviews"] == 2
    assert len(data["review_analysis"]) == 2


# Test 3: Duplicate detection

def test_duplicate_detection():
    review = "This product is amazing and works perfectly."

    response = client.post(
        "/analyze/all",
        json={
            "reviews": [review, review],
            "ratings": [5, 5]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["duplicate_candidates"]) == 1
    assert data["duplicate_candidates"][0]["similarity"] == 1.0


# Test 4: Mismatched review and rating counts

def test_mismatched_counts():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": [
                "Excellent product.",
                "Very poor product."
            ],
            "ratings": [5]
        }
    )

    assert response.status_code == 422


# Test 5: Invalid rating

def test_invalid_rating():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": ["Excellent product."],
            "ratings": [6]
        }
    )

    assert response.status_code == 422


# Test 6: Empty review

def test_empty_review():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": ["   "],
            "ratings": [5]
        }
    )

    assert response.status_code == 422


# Test 7: Empty review list

def test_empty_review_list():
    response = client.post(
        "/analyze/all",
        json={
            "reviews": [],
            "ratings": []
        }
    )

    assert response.status_code == 422
