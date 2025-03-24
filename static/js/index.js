let townlands = [];

fetch("static/data/townlands.json")
    .then(response => response.json())
    .then(data => {
        townlands = data.features.map(feature => feature.properties.TL_ENGLISH);
    })
    .catch(error => console.error("Error fetching townlands:", error));

function filterTownlands() {
    const searchBar = document.getElementById("search-bar");
    const suggestions = document.getElementById("suggestions");
    const searchText = searchBar.value.trim().toLowerCase();

    suggestions.innerHTML = "";

    if (searchText === "") {
        suggestions.style.display = "none";
        return;
    }

    const filteredTownlands = townlands.filter(townland =>
        townland.toLowerCase().includes(searchText)
    );

    if (filteredTownlands.length > 0) {
        suggestions.style.display = "block";
        filteredTownlands.forEach(townland => {
            const rectangle = document.createElement("a");
            rectangle.className = "result-rectangle";
            rectangle.textContent = toTitleCase(townland);
            rectangle.href = `/townlands/${encodeURIComponent(townland)}`; // Link generation
            rectangle.style.display = "block";
            rectangle.style.textDecoration = "none";
            rectangle.style.color = "inherit";
            rectangle.target = "_blank" // Open new tab on click
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

document.addEventListener("DOMContentLoaded", function () {
    const legend = document.getElementById("legend");
    if (legend) {
        legend.style.display = "none";
    }
    function toggleLegend() {
        const tenanciesLayer = document.querySelector(".leaflet-control-layers-selector[name=\"Tenancies Heat Map\"]");
        const evictionsLayer = document.querySelector(".leaflet-control-layers-selector[name=\"Evictions Heat Map\"]");
        const emigrationsLayer = document.querySelector(".leaflet-control-layers-selector[name=\"Emigrations Heat Map\"]");
        const townlandsLayer = document.querySelector(".leaflet-control-layers-selector[name=\"Townlands\"]");
        const isHeatmapActive =
            (tenanciesLayer && tenanciesLayer.checked) ||
            (evictionsLayer && evictionsLayer.checked) ||
            (emigrationsLayer && emigrationsLayer.checked);
        if (legend) {
            if (isHeatmapActive) {
                legend.style.display = "block";
            } else {
                legend.style.display = "none";
            }
        }
    }
    const layerControls = document.querySelectorAll(".leaflet-control-layers-selector");
    layerControls.forEach(control => {
        control.addEventListener("change", toggleLegend);
    });
    toggleLegend();
});