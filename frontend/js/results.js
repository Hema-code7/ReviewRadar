
function displayResults(data) {
    const resultsContainer = document.getElementById("resultsContainer");

    // Clear previous results
    resultsContainer.replaceChildren();

    // Display summary
    const heading = document.createElement("h2");
    heading.textContent = "Analysis Results";

    const summary = document.createElement("p");
    summary.textContent = `Total reviews analysed: ${data.total_reviews}`;

    resultsContainer.appendChild(heading);
    resultsContainer.appendChild(summary);

    // Display duplicate candidates
    const duplicateHeading = document.createElement("h3");
    duplicateHeading.textContent = "Duplicate Review Detection";
    resultsContainer.appendChild(duplicateHeading);

    if (data.duplicate_candidates.length === 0) {
        const message = document.createElement("p");
        message.textContent = "No duplicate candidates found.";
        resultsContainer.appendChild(message);
    } else {
        data.duplicate_candidates.forEach(function (duplicate) {
            const item = document.createElement("p");

            item.textContent =
                `Review ${duplicate.review_1 + 1} and Review ${duplicate.review_2 + 1} ` +
                `may be duplicates (Similarity: ${(duplicate.similarity * 100).toFixed(1)}%).`;

            resultsContainer.appendChild(item);
        });
    }

    // Display individual review analysis
    data.review_analysis.forEach(function (result, index) {
        const card = document.createElement("div");
        card.className = "result-card";

        const reviewHeading = document.createElement("h3");
        reviewHeading.textContent = `Review ${index + 1}`;

        const reviewText = document.createElement("p");
        reviewText.textContent = result.review;

        const rating = document.createElement("p");
        rating.textContent = `Rating: ${result.rating}/5`;

        const suspicious = document.createElement("p");
        suspicious.textContent = result.suspicious_analysis.suspicious
            ? "Suspicious signals detected"
            : "No suspicious signals detected";

        const suspiciousSignals = document.createElement("p");
        suspiciousSignals.textContent =
            "Signals: " +
            (result.suspicious_analysis.signals.length
                ? result.suspicious_analysis.signals.join(", ")
                : "None");

        const consistency = document.createElement("p");
        consistency.textContent = result.consistency_analysis.consistent
            ? "Rating and review appear consistent"
            : "Rating and review may be inconsistent";

        const consistencySignal = document.createElement("p");
        consistencySignal.textContent =
            "Consistency signal: " + result.consistency_analysis.signal;

        const aiDetection = document.createElement("p");
        aiDetection.textContent =
            `Writing-origin estimate: ${result.ai_detection.prediction} ` +
            `(${(result.ai_detection.confidence * 100).toFixed(1)}% confidence)`;

        card.append(
            reviewHeading,
            reviewText,
            rating,
            suspicious,
            suspiciousSignals,
            consistency,
            consistencySignal,
            aiDetection
        );

        resultsContainer.appendChild(card);
    });
}
