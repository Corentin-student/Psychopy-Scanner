var Holes = {};

function openPopup(value) {
    document.getElementById(value).style.display = "block"; // Affiche l'overlay
}

function closePopup(value) {
    document.getElementById(value).style.display = "none"; // Cache l'overlay
}

function ParadigmCreated() {
    location.href = '/created_paradigmes';
}

function PrimeParadigm() {
    location.href = '/';
}

function addingFiles(){
    console.log("on regarde ce qui se passe")
    let instru = document.getElementById("fileinput-Instructions").value;
    let end = document.getElementById("fileinput-End").value;
    instru = instru.split('\\').pop();
    end = end.split("\\").pop();
    document.getElementById("instruction_txt").textContent = instru;
    document.getElementById("end_txt").textContent = end;
    document.getElementById("visible-group").style.visibility = "visible";

}

function fermerTousOverlays() {
    var overlays = document.querySelectorAll('.overlay-index');
    overlays.forEach(function(overlay) {
        if (overlay.style.display !== 'none') {
            overlay.style.display = 'none';
        }
    });
}

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        fermerTousOverlays();
    }
});

function submit(name) {
    let angleStimulus;
    let zoom;
    if (name === "Image"){
        angleStimulus = document.getElementById("angle-Image").value || 0;
        zoom = document.getElementById("zoom-image").value || 0;

    }
    else if (name ==="Video"){
        zoom = document.getElementById("zoom-video").value || 0;
        angleStimulus = "/";
    }
    else{
        angleStimulus = "/";
        zoom = "/";
    }
    const timingApparitionInput = document.getElementById("apparition-"+name).value;
    const timingApparition = parseFloat(timingApparitionInput);
    const dureeInput = document.getElementById("duration-"+name).value;
    const dureeStimulus = parseFloat(dureeInput);
    let fileInput
    let fileName
    if (name === "Enregistrement"){
        fileName = "/";
    }else {
        fileInput = document.getElementById("fileinput-"+name);
        fileName = fileInput.value.split('\\').pop();
    }

    if (timingApparitionInput === "" || isNaN(timingApparition) || fileName === "") {
        alert("Veuillez remplir le timing d'apparition ou/et le fichier d'image qui sera utilisé");
        return;
    }

    const isDurationNaN = isNaN(dureeStimulus);
    const rows = document.querySelectorAll("#table-body tr");
    let isOverlap = false;
    rows.forEach(row => {
        const rowTiming = parseFloat(row.cells[0].textContent.slice(0, -1));
        const rowDuration = parseFloat(row.cells[1].textContent.slice(0, -1));
        const rowEnd = rowTiming + rowDuration;
        if ((timingApparition >= rowTiming && timingApparition < rowEnd) && !(timingApparition === rowTiming && dureeStimulus === rowDuration)) {
            isOverlap = true;
        }
    });

    if (isOverlap) {
        alert("Un stimulus est déjà en cours à ce moment ou il y a un chevauchement sans correspondance de durée.");
        return;
    }

    let newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${timingApparition.toFixed(3)}s</td>
        <td>${isDurationNaN ? 'Indéfini' : `${dureeStimulus.toFixed(3)}s`}</td>
        <td>${name}</td>
        <td>${fileName}</td>
        <td>${angleStimulus}</td>
        <td>${zoom}</td>
        <td><button class="supress" onclick="handleCloseClick(this)">Supprimer</button></td>
    `;

    let inserted = false;
    for (let i = 0; i < rows.length; i++) {
        let rowTiming = parseFloat(rows[i].cells[0].textContent.slice(0, -1)); // Retire le 's' à la fin
        if (timingApparition < rowTiming) {
            document.getElementById("table-body").insertBefore(newRow, rows[i]);
            inserted = true;
            break;
        }
    }
    if (!inserted) {
        document.getElementById("table-body").appendChild(newRow);
    }
    highlightDuplicateTimings();
    document.getElementById("apparition-"+name).value = "";
    document.getElementById("duration-"+name).value = "";
}


function fillHoles(){
    for (const [key, value] of Object.entries(Holes)) {
        var truevalue = value-key;
        document.getElementById("apparition-Fixation").value = key;
        document.getElementById("duration-Fixation").value = truevalue;
        console.log(key, value);
        fixation();
    }
}
function fixation(){
    const timingApparitionInput = document.getElementById("apparition-Fixation").value;
    const timingApparition = parseFloat(timingApparitionInput);
    const dureeInput = document.getElementById("duration-Fixation").value;
    const dureeStimulus = parseFloat(dureeInput);

    const rows = document.querySelectorAll("#table-body tr");
    let isOverlap = false;
    rows.forEach(row => {
        const rowTiming = parseFloat(row.cells[0].textContent.slice(0, -1));
        const rowDuration = parseFloat(row.cells[1].textContent.slice(0, -1));
        const rowEnd = rowTiming + rowDuration;
        if ((timingApparition >= rowTiming && timingApparition < rowEnd) && !(timingApparition === rowTiming && dureeStimulus === rowDuration)) {
            isOverlap = true;
        }
    });

    if (isOverlap) {
        alert("Un stimulus est déjà en cours à ce moment ou il y a un chevauchement sans correspondance de durée.");
        return;
    }


    let newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${timingApparition.toFixed(3)}s</td>
        <td>${dureeStimulus.toFixed(3)}s</td>
        <td>Croix de Fixation</td>
        <td>/</td>
        <td>/</td>
        <td>/</td>
        <td><button class="supress" onclick="handleCloseClick(this)">Supprimer</button></td>
    `;
    let inserted = false;
    for (let i = 0; i < rows.length; i++) {
        let rowTiming = parseFloat(rows[i].cells[0].textContent.slice(0, -1)); // Retire le 's' à la fin
        if (timingApparition < rowTiming) {
            document.getElementById("table-body").insertBefore(newRow, rows[i]);
            inserted = true;
            break;
        }
    }
    if (!inserted) {
        document.getElementById("table-body").appendChild(newRow);
    }
    highlightDuplicateTimings();
    document.getElementById("apparition-Fixation").value = "";
    document.getElementById("duration-Fixation").value = "";
}



function checkingHoles(){
    // Obtenir toutes les lignes existantes dans le tableau
    let rows = document.querySelectorAll("#table-body tr");
    let lastEnd = 0; // Pour suivre la fin du dernier événement traité
    let discontinuities = []; // Stocker les messages des discontinuités détectées
    let timingMap = {}; // Objet pour stocker les correspondances


    if (rows.length > 0) {
        let firstRowTiming = parseFloat(rows[0].cells[0].textContent.slice(0, -1)); // Temps d'apparition de la première ligne

        // Vérifier si le premier événement commence à 0, sinon ajouter une discontinuité
        if (firstRowTiming !== 0) {
            timingMap[0] = firstRowTiming;
            discontinuities.push(`Discontinuité détectée entre 0s et ${firstRowTiming}s`);
        }
    }

    for (let i = 0; i < rows.length; i++) {
        let rowTiming = parseFloat(rows[i].cells[0].textContent.slice(0, -1)); // Temps d'apparition
        let rowDuration = parseFloat(rows[i].cells[1].textContent.slice(0, -1)); // Durée de l'événement
        let rowEnd = rowTiming + rowDuration; // Fin de l'événement

        // Vérifier s'il y a un trou entre la fin du dernier événement et le début de l'événement courant
        if (lastEnd < rowTiming && i > 0) {
            if (!timingMap.hasOwnProperty(lastEnd)) {
                timingMap[lastEnd] = rowTiming;
                discontinuities.push(`Discontinuité détectée entre ${lastEnd}s et ${rowTiming}s`);
            }
        }

        lastEnd = rowEnd; // Mettre à jour la fin du dernier événement traité
    }
    console.log(timingMap);

    // Afficher les discontinuités détectées
    if (discontinuities.length > 0) {
        console.log(discontinuities.join('\n'));
    } else {
        console.log("Aucune discontinuité détectée.");
    }
    return timingMap;
}
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Erreur lors du téléchargement du fichier:', error));
    }
}

function validateFloatInput(input) {
    const value = input.value;
    if (!/^\d*\.?\d*$/.test(value)) {
        input.value = value.slice(0, -1);
    }
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


function SubmitParadigme() {
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
    const instructions = document.getElementById("instruction_txt").textContent;
    const mot_fin = document.getElementById("end_txt").textContent;
    const filename = document.getElementById("paradigme_name").value;
    const background = document.getElementById("background-color").value;
    fetch('/keep-datas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            data: data,
            filename: filename,
            instructions: instructions,
            mot_fin: mot_fin,
            background: background
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });



}

function submitTable() {

    Holes = checkingHoles();
    if (Object.keys(Holes).length === 0) {
        openPopup("overlay-filename")
    }
    else {
        openPopup("overlay-Holes")
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleIcon = document.getElementById('lang-icon');
    const langNL = document.getElementById('lang-nl');
    const langFR = document.getElementById('lang-fr');


    if (toggleIcon) {
        toggleIcon.addEventListener('click', function () {
            window.location.href = '/nl/index';
        });
    }

    if (langNL) {
        langNL.addEventListener('click', function () {
            window.location.href = '/nl/index';
        });
    }
})

