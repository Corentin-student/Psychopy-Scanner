document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/json-files')
    .then(response => response.json())
    .then(files => {
        const sidenav = document.querySelector('.sidenav');
        sidenav.innerHTML = '<h2 class="h2-sidenav">Paradigme</h2>';  // Reset and keep the header

        files.forEach(file => {
            const link = document.createElement('a');
            link.href = "#";
            link.textContent = file;
            link.onclick = function() { get_table(file); };
            sidenav.appendChild(link);
        });
    })
    .catch(error => console.error('Failed to load JSON file names:', error));

});

function get_table(file_name){
    fetch('static/jsons/' + file_name + '.json')
    .then(response => response.json())
    .then(jsonData => {
        const tableBody = document.getElementById('table-body');

        // Vider le contenu actuel du tableau
        tableBody.innerHTML = '';

        jsonData.forEach(item => {
            const row = `<tr>
                <td>${item.Apparition}</td>
                <td>${item.Duree}</td>
                <td>${item.Type}</td>
                <td>${item.Stimulus}</td>
                <td>${item.Angle}</td>
                <td><button class="supress" onclick="removeRow(this)">Supprimer</button></td>
            </tr>`;

            tableBody.innerHTML += row;
        });

        window.removeRow = function(button) {
            button.closest('tr').remove();
        };
        highlightDuplicateTimings();
    })
    .catch(error => {
        console.error('Error loading the JSON file:', error);
    });
}

function highlightDuplicateTimings() {
    const rows = document.querySelectorAll("#table-body tr");
    const timingCounts = {};
    rows.forEach(row => {
        const timing = row.cells[0].textContent.trim();
        if (timingCounts[timing]) {
            timingCounts[timing].push(row);
        } else {
            timingCounts[timing] = [row];
        }
    });

    Object.values(timingCounts).forEach(group => {
        if (group.length > 1) {
            group.forEach(row => row.classList.add("highlight"));
        }
    });
}

function launching(){
    var table = document.querySelector('.stimulus-table');
    var data = [];
    var keys = ['Apparition', 'Duree', 'Type', 'Stimulus', 'Angle'];
    for (var i = 1, row; row = table.rows[i]; i++) {
        var rowData = {};
        for (var j = 0, col; col = row.cells[j]; j++) {
            if (j < row.cells.length - 1) { // Ne pas inclure la dernière colonne 'Enlever'
                var key = keys[j]; // Utiliser les clés prédéfinies
                console.log("okkk")
                console.log(key)
                console.log("je capte pas")
                var value = col.textContent.trim();
                if (key === 'Apparition' || key === 'Duree') {
                    value = value.endsWith('s') ? value.slice(0, -1) : value; // Enlève le 's' à la fin si présent
                }
                rowData[key] = value;
            }
        }
        data.push(rowData);
    }
    console.log(data);

    fetch('/submit-table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // Conversion directe du tableau en chaîne JSON
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
