const analyzeButton = document.getElementById("analyzeButton");
const inputMessage = document.getElementById("inputMessage");

// Handle Analyze button click
analyzeButton.addEventListener("click", async function () {
    let reviews = [];
    let ratings = [];

    const isSingleMode =
        document.getElementById("singleReviewContainer").style.display !== "none";

    // Get single review
    if (isSingleMode) {
        const review = document.getElementById("reviewText").value.trim();
        const rating = Number(document.getElementById("rating").value);

        if (!review) {
            inputMessage.textContent = "Please enter a review.";
            return;
        }

        reviews.push(review);
        ratings.push(rating);
    }

    // Get multiple reviews
    else {
        const reviewCards = document.querySelectorAll(".review-input-card");

        for (const card of reviewCards) {
            const review = card.querySelector(".multiple-review-text").value.trim();
            const rating = Number(card.querySelector(".multiple-review-rating").value);

            if (!review) {
                inputMessage.textContent = "Please fill in all review fields.";
                return;
            }

            reviews.push(review);
            ratings.push(rating);
        }
    }

    inputMessage.textContent = "Analyzing reviews...";
    analyzeButton.disabled = true;

    try {
        const data = await analyzeReviews(reviews, ratings);

        displayResults(data);

        inputMessage.textContent = "Analysis completed successfully.";

        document.getElementById("results").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        inputMessage.textContent =
            "Unable to connect to the server. Please check whether the backend is running.";
    } finally {
        analyzeButton.disabled = false;
    }
});
