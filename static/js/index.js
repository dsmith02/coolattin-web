let townlands = [];

fetch('static/data/townlands.json')
    .then(response => response.json())
    .then(data => {
        townlands = data.features.map(feature => feature.properties.TL_ENGLISH);
    })
    .catch(error => console.error('Error fetching townlands:', error));

function filterTownlands() {
    const searchBar = document.getElementById("search-bar");
    const suggestions = document.getElementById("suggestions");
    const searchText = searchBar.value.trim().toLowerCase();

    // Clear previous suggestions
    suggestions.innerHTML = "";

    if (searchText === "") {
        suggestions.style.display = "none";
        return;
    }

    // Filter townlands based on search text
    const filteredTownlands = townlands.filter(townland =>
        townland.toLowerCase().includes(searchText)
    );

    if (filteredTownlands.length > 0) {
        // Display suggestions
        suggestions.style.display = "block";

        // Add filtered townlands to the suggestions div
        filteredTownlands.forEach(townland => {
            const rectangle = document.createElement("a"); // Use <a> for links
            rectangle.className = "result-rectangle";
            rectangle.textContent = toTitleCase(townland); // Convert to title case
            rectangle.href = `/townlands/${encodeURIComponent(townland)}`; // Generate link
            rectangle.style.display = "block"; // Ensure the link behaves like a block element
            rectangle.style.textDecoration = "none"; // Remove underline
            rectangle.style.color = "inherit"; // Inherit text color
            suggestions.appendChild(rectangle);
        });
    } else {
        suggestions.style.display = "none";
    }
}

function toTitleCase(string) {
    return string.replace(/\w\S*/g, (word) =>
        word.charAt(0).toUpperCase() + word.substr(1).toLowerCase()
    );
}