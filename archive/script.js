// Global map variable
let map = null;

// Navigation functionality
document.addEventListener("DOMContentLoaded", () => {
  const navLinks = document.querySelectorAll(".nav-links a");

  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();

      // Remove active class from all links and pages
      navLinks.forEach((l) => l.classList.remove("active"));
      document
        .querySelectorAll(".page")
        .forEach((p) => p.classList.remove("active"));

      // Add active class to clicked link and corresponding page
      link.classList.add("active");
      const pageId = link.getAttribute("data-page");
      document.getElementById(pageId).classList.add("active");

      // Initialize map if map page is active
      if (pageId === "map-page") {
        // Small delay to ensure container is visible
        setTimeout(initMap, 100);
      }
    });
  });
});

// Map initialization
function initMap() {
  // Check if map already exists
  if (map !== null) {
    map.remove();
    map = null;
  }

  // Get map container
  const mapContainer = document.getElementById("map");
  if (!mapContainer) {
    console.error("Map container not found");
    return;
  }

  try {
    // Initialize the map centered on Tinahely
    map = L.map("map", {
      center: [52.7989, -6.4624],
      zoom: 14, // Increased zoom level to show town detail
      minZoom: 6,
      maxZoom: 18,
    });

    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // Add marker for Tinahely
    const marker = L.marker([52.7989, -6.4624])
      .addTo(map)
      .bindPopup(
        `
                <div style="text-align: center;">
                    <h3 style="margin-bottom: 5px;">Tinahely</h3>
                    <p style="margin: 5px 0;">Historical Estate Records</p>
                    <p style="margin: 5px 0;">County Wicklow</p>
                </div>
            `
      )
      .openPopup();

    // Force a map resize after initialization
    setTimeout(() => {
      map.invalidateSize();
    }, 100);
  } catch (error) {
    console.error("Error initializing map:", error);
  }
}
