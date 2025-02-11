document.addEventListener("DOMContentLoaded", function () {
    // Get the search input element
    const searchInput = document.getElementById("searchInput");
    console.log("HELLO WORLD")

    // Add an event listener to the search input
    searchInput.addEventListener("input", function () {
        const searchTerm = this.value.toLowerCase(); // Get the search term and convert to lowercase
        const tableRows = document.querySelectorAll("#tenancies tbody tr"); // Get all table rows

        // Loop through each row and check if the forename matches the search term
        tableRows.forEach(function (row) {
            const forenameCell = row.querySelector("td:nth-child(1)"); // Get the forename cell (first column)
            const forename = forenameCell.textContent.toLowerCase(); // Get the forename text and convert to lowercase

            // Show or hide the row based on whether the forename matches the search term
            if (forename.includes(searchTerm)) {
                row.style.display = ""; // Show the row
            } else {
                row.style.display = "none"; // Hide the row
            }
        });
    });
});

// Modal population
const recordModal = document.getElementById("recordModal");
recordModal.addEventListener("show.bs.modal", function (event) {
    const link = event.relatedTarget;
    console.log("DEBUG");
    const record = {
        id: link.getAttribute("data-id"),
        nli_ref: link.getAttribute("data-nli-ref"),
        forename: link.getAttribute("data-forename"),
        surname: link.getAttribute("data-surname"),
        age: link.getAttribute("data-age"),
        occupation: link.getAttribute("data-occupation"),
        townland: link.getAttribute("data-townland"),
        acres_irish: link.getAttribute("data-acres-irish"),
        tenant_type: link.getAttribute("data-tenant-type")
    };

    document.getElementById("modal-id").textContent = checkNan(record.id);
    document.getElementById("modal-nli-ref").textContent = checkNan(record.nli_ref);
    document.getElementById("modal-forename").textContent = checkNan(record.forename);
    document.getElementById("modal-surname").textContent = checkNan(record.surname);
    document.getElementById("modal-age").textContent = checkNan(record.age)
    document.getElementById("modal-occupation").textContent = checkNan(record.occupation);
    document.getElementById("modal-townland").textContent = checkNan(record.townland);
    document.getElementById("modal-acres-irish").textContent = checkNan(record.acres_irish);
    document.getElementById("modal-tenant-type").textContent = checkNan(record.tenant_type);
});

function checkNan(val) {
    return val === "nan" ? "NA" : val;
}