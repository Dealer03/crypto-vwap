function sortTable(columnIndex) {
    let table, rows, switching, i, x, y, shouldSwitch, ascending;
    table = document.getElementById("transactionTable");
    switching = true;
    ascending = true; // Default sorting order is ascending
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];
            // Compare values based on sorting order
            if (ascending) {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            } else {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        } else {
            if (ascending) {
                // If no switching occurred and it's the first pass, switch to descending order
                ascending = false;
                switching = true;
            }
        }
    }
}
