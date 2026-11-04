
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from detection.duplicate import find_duplicates
from detection.suspicious import detect_suspicious
from detection.consistency import check_consistency
from detection.ai_detection import detect_ai_review
from pydantic import BaseModel, Field, field_validator, model_validator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ReviewRadar API",
    description="AI-powered Review Intelligence Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to ReviewRadar"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Request Models

class ReviewInput(BaseModel):
    reviews: list[str]

    @field_validator("reviews")
    @classmethod
    def validate_reviews(cls, reviews):
        if not reviews:
            raise ValueError("At least one review is required")

        for review in reviews:
            if not review or not review.strip():
                raise ValueError("Reviews cannot be empty")

        return reviews


class ConsistencyInput(BaseModel):
    review: str
    rating: int = Field(ge=1, le=5)

    @field_validator("review")
    @classmethod
    def validate_review(cls, review):
        if not review or not review.strip():
            raise ValueError("Review cannot be empty")

        return review


class CombinedReviewInput(BaseModel):
    reviews: list[str]
    ratings: list[int]

    @field_validator("reviews")
    @classmethod
    def validate_reviews(cls, reviews):
        if not reviews:
            raise ValueError("At least one review is required")

        for review in reviews:
            if not review or not review.strip():
                raise ValueError("Reviews cannot be empty")

        return reviews

    @field_validator("ratings")
    @classmethod
    def validate_ratings(cls, ratings):
        for rating in ratings:
            if rating < 1 or rating > 5:
                raise ValueError("Ratings must be between 1 and 5")

        return ratings

    @model_validator(mode="after")
    def validate_review_rating_count(self):
        if len(self.reviews) != len(self.ratings):
            raise ValueError("Number of reviews and ratings must match")

        return self


# Duplicate Detection API

@app.post("/analyze/duplicates")
def analyze_duplicates(data: ReviewInput):
    result = find_duplicates(data.reviews)

    return {
        "total_reviews": len(data.reviews),
        "duplicate_candidates": result
    }


# Suspicious Review Detection API

@app.post("/analyze/suspicious")
def analyze_suspicious(data: ReviewInput):
    results = []

    for review in data.reviews:
        result = detect_suspicious(review)

        results.append({
            "review": review,
            "suspicious": result["suspicious"],
            "signals": result["signals"]
        })

    return {
        "total_reviews": len(data.reviews),
        "results": results
    }


# Review Consistency API

@app.post("/analyze/consistency")
def analyze_consistency(data: ConsistencyInput):
    result = check_consistency(data.review, data.rating)

    return {
        "review": data.review,
        "rating": data.rating,
        "consistent": result["consistent"],
        "signal": result["signal"]
    }


# AI Detection API

@app.post("/analyze/ai")
def analyze_ai(review: str):
    return detect_ai_review(review)


# Combined Review Analysis API


@app.post("/analyze/all")
def analyze_all(data: CombinedReviewInput):

    # Duplicate detection across all reviews
    duplicate_results = find_duplicates(data.reviews)

    results = []

    # Analyse each review individually
    for review, rating in zip(data.reviews, data.ratings):

        suspicious_result = detect_suspicious(review)

        consistency_result = check_consistency(
            review,
            rating
        )

        ai_result = detect_ai_review(review)

        results.append({
            "review": review,
            "rating": rating,

            "suspicious_analysis": {
                "suspicious": suspicious_result["suspicious"],
                "signals": suspicious_result["signals"]
            },

            "consistency_analysis": {
                "consistent": consistency_result["consistent"],
                "signal": consistency_result["signal"]
            },

            "ai_detection": ai_result
        })

    return {
        "total_reviews": len(data.reviews),
        "duplicate_candidates": duplicate_results,
        "review_analysis": results
    }
