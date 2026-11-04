
const API_BASE_URL = "http://127.0.0.1:8000";

// Send reviews to the combined analysis endpoint
async function analyzeReviews(reviews, ratings) {

    try {
        const response = await fetch(`${API_BASE_URL}/analyze/all`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                reviews: reviews,
                ratings: ratings
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to analyse reviews"
            );
        }

        return data;

    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}

