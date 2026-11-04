// Get mode buttons and review sections
const singleModeButton = document.getElementById("singleMode");
const multipleModeButton = document.getElementById("multipleMode");

const singleReviewSection = document.getElementById("singleReviewContainer");
const multipleReviewSection = document.getElementById("multipleReviewContainer");

const addReviewButton = document.getElementById("addReviewButton");
const reviewList = document.getElementById("reviewList");

// Switch to single review mode
singleModeButton.addEventListener("click", function () {
    singleReviewSection.style.display = "block";
    multipleReviewSection.style.display = "none";

    singleModeButton.classList.add("active");
    multipleModeButton.classList.remove("active");
});

// Switch to multiple review mode
multipleModeButton.addEventListener("click", function () {
    singleReviewSection.style.display = "none";
    multipleReviewSection.style.display = "block";

    multipleModeButton.classList.add("active");
    singleModeButton.classList.remove("active");
});

// Add a new review card
addReviewButton.addEventListener("click", function () {
    const reviewCard = document.createElement("div");
    reviewCard.className = "review-input-card";

    reviewCard.innerHTML = `
        <textarea
            class="multiple-review-text"
            placeholder="Enter another product review..."
            rows="4"
        ></textarea>

        <select class="multiple-review-rating">
            <option value="5">5 Stars</option>
            <option value="4">4 Stars</option>
            <option value="3">3 Stars</option>
            <option value="2">2 Stars</option>
            <option value="1">1 Star</option>
        </select>
    `;

    reviewList.appendChild(reviewCard);
});
