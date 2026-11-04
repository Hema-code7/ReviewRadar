
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_duplicates(reviews, threshold=0.7):

    if len(reviews) < 2:
        return []

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(reviews)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    duplicates = []

    for i in range(len(reviews)):
        for j in range(i + 1, len(reviews)):

            score = similarity_matrix[i][j]

            if score >= threshold:
                duplicates.append({
                    "review_1": i,
                    "review_2": j,
                    "similarity": round(float(score), 2)
                })

    return duplicates