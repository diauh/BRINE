/* ==========================================================
   BRINE – Deep Sea Search Engine
   Frontend interactions
   ========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ------------------------------------------------------
       1. If results are showing, scroll down to them
       ------------------------------------------------------ */
    const resultsSection = document.getElementById("results");
    if (resultsSection) {
        setTimeout(function () {
            resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 200);
    }

    /* ------------------------------------------------------
       2. Random Dive button
       ------------------------------------------------------ */
    const diveButton = document.getElementById("random-dive-btn");
    if (diveButton) {
        diveButton.addEventListener("click", showRandomDive);
    }
});


/* ==========================================================
   Explore a category (called by the category cards)
   ========================================================== */
function exploreCategory(categoryName) {
    const queryInput = document.getElementById("query-input");
    const categorySelect = document.getElementById("category-select");
    const form = document.querySelector(".search-form");

    if (!form || !categorySelect) {
        return;
    }

    if (queryInput) {
        queryInput.value = "";
    }
    categorySelect.value = categoryName;
    form.submit();
}


/* ==========================================================
   Random Dive
   ========================================================== */
async function showRandomDive() {
    const panel = document.getElementById("random-dive-panel");

    try {
        const response = await fetch("/random-dive");
        const documentData = await response.json();

        document.getElementById("dive-category").textContent = documentData.category;
        document.getElementById("dive-title").textContent = documentData.title;
        document.getElementById("dive-desc").textContent = documentData.description;
        document.getElementById("dive-keywords").textContent =
            "Keywords: " + (documentData.keywords || []).join(", ");

        panel.hidden = false;
        panel.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (error) {
        console.error("Could not load a random document:", error);
    }
}


/* ==========================================================
   Close the Random Dive panel
   ========================================================== */
function closeRandomDive() {
    const panel = document.getElementById("random-dive-panel");
    if (panel) {
        panel.hidden = true;
    }
}