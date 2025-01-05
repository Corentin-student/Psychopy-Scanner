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


function ParadigmCreation() {
    location.href = '/index';
}

function PrimeParadigm() {
    location.href = '/';
}
function get_table(file_name){
    const url = `/get-json-file?param_to_file=${file_name}`;
    fetch(url)
    .then(response => response.json())
    .then(jsonData => {
        const tableBody = document.getElementById('table-body');
        // Vider le contenu actuel du tableau
        tableBody.innerHTML = '';

        jsonData.data.forEach(item => {
            const row = `<tr>
                <td>${item.Apparition}</td>
                <td>${item.Duree}</td>
                <td>${item.Type}</td>
                <td>${item.Stimulus}</td>
                <td>${item.Angle}</td>
                <td>${item.Zoom}</td>
                <td><button class="supress" onclick="handleCloseClick(this)">Supprimer</button></td>
            </tr>`;

            tableBody.innerHTML += row;
        });
        highlightDuplicateTimings();
        document.getElementById("instruction_txt").textContent = jsonData.instructions;
        document.getElementById("end_txt").textContent = jsonData.mot_fin;
        document.getElementById("visible-group").style.visibility = "visible";
    })
    .catch(error => {
        console.error('Error loading the JSON file:', error);
    });
}

function handleCloseClick(button) { //La fonction sert à enlever une row et mettre à jour les valeurs d'onsets
    const row = button.closest("tr");
    if (row.classList.contains("highlight")) { // On supprime juste la row si c'est un stimulus en concurrence
        row.remove();
        highlightDuplicateTimings();
        return;
    }
    const tableBody = document.querySelector("#table-body");
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const rowIndex = rows.indexOf(row);
    if (rowIndex === -1) return;
    const durationCell = row.cells[1];
    const duration = parseFloat(durationCell.textContent.slice(0, -1));
    row.remove();
    for (let i = rowIndex; i < rows.length; i++) {
        const currentRow = rows[i];
        const onsetCell = currentRow.cells[0];
        const currentOnset = parseFloat(onsetCell.textContent.slice(0, -1));
        const newOnset = currentOnset - duration;
        onsetCell.textContent = `${newOnset.toFixed(3)}s`;
    }
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
        else {
            group.forEach(row => row.classList.remove("highlight"));
        }
    });
}

function openPopup(name) {
    document.getElementById(name).style.display = 'flex';
}
function submitPopup() {
    var input = document.getElementById('patientInput').value;
    document.getElementById('patientName').textContent = input; // Met à jour le nom du patient
    document.getElementById('popupOverlay').style.display = 'none'; // Ferme la pop-up
    alert("okk?")
}


function submitPort(){
    var baudrate = document.getElementById("baudrate").value;
    var port = document.getElementById("port").value;
    var realtrigger = document.getElementById("trigger").value;
    document.getElementById("resultPort").textContent = port;
    document.getElementById("resultBaudrate").textContent = baudrate;
    document.getElementById("resultTrigger").textContent = realtrigger;
    document.getElementById("popupSerial").style.display = 'none';
}


document.getElementById('openPopup').addEventListener('click', function() {
    openPopup('popupOverlay');
});

document.getElementById('serialport').addEventListener('click', function() {
    openPopup('popupSerial');
});

function closePopup(popupId) {
    document.getElementById(popupId).style.display = 'none';
}

function launching(){
    var table = document.querySelector('.stimulus-table');
    var data = [];
    var keys = ['Apparition', 'Duree', 'Type', 'Stimulus', 'Angle', 'Zoom'];
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
    const instructions = document.getElementById("instruction_txt").textContent;
    const mot_fin = document.getElementById("end_txt").textContent;
    const output_file = document.getElementById('patientName').textContent;
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random").checked;


    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';
    if (data.length === 0){
        Swal.fire({
            title: 'Veuillez sélectionner un paradigme contenant au moins un stimulus',
            icon: 'error',
            confirmButtonText: 'OK',
            confirmButtonColor: '#4CAF50', // Couleur verte
        });
        return;
    }

    fetch('/submit-table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            data: data,
            instructions: instructions,
            mot_fin: mot_fin,
            output_file: output_file,
            activation: activation,
            random: random,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            port: port


        }) // Conversion directe du tableau en chaîne JSON
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    Swal.fire({
        title: 'Votre paradigme va se lancer',
        text: "si vous n'avez oublié aucun paramètre",
        icon: 'success',
        confirmButtonText: 'OK',
        confirmButtonColor: '#4CAF50', // Couleur verte
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const toggleIcon = document.getElementById('lang-icon');
    const langNL = document.getElementById('lang-nl');
    const langFR = document.getElementById('lang-fr');


    if (toggleIcon) {
        toggleIcon.addEventListener('click', function () {
            window.location.href = '/nl/created_paradigmes';
        });
    }

    if (langNL) {
        langNL.addEventListener('click', function () {
            window.location.href = '/nl/created_paradigmes';
        });
    }
})
