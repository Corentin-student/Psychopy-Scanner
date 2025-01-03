function changeMainContent(section) {
    const mainContent = document.getElementById('main-content');
    let newContent = '';

    const links = document.querySelectorAll('.sidenav a');
    links.forEach(link => {
        link.classList.remove('active');
    });

    const activeLink = document.querySelector(`.sidenav a[onclick="changeMainContent('${section}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    switch(section) {
        case 'home':
            newContent = `
                <h2>Paradigme pour les mots défilants</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée croix de Fixation</h3>
                        <input type="text" id="text-fixation" placeholder="par exemple: 4" >
                    </div>
                    <div class="input-container">
                        <h3>Liste de mots pour le paradigme</h3>
                        <input type="text" id="words" placeholder="par exemple: Pomme, voiture, matin,...">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom" type="text" placeholder="par exemple: 30">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-text" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitText()">Submit</button>
                    </div>
                </div>
            `;
            break;
        case 'about':
            newContent = `
                <h2>Paradigme pour les images statiques défilantes</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-image" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-image').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-image" type="text" placeholder="par exemple: 100">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-image" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-image" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitImages()">Submit</button>
                    </div>
                </div>
            `;
            break;
        case 'contact':
            newContent = `
                <h2>Paradigme pour les stimuli vidéo</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-video" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-video" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-video').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-video" type="text" placeholder="par exemple: 50">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-video" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-video" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitVideos()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'long_text':
            newContent = `
                <h2>Paradigme pour les adjectifs positifs/négatifs</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-adjectifs" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée croix de fixation</h3>
                        <input type="text" id="betweenstimuli-adjectifs" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-adjectifs').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-adjectifs" type="text" placeholder="par exemple: 50">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Nombre de blocks d'entrainement</h3>
                        <input type="text" id="number_of_blocks-entrainement" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Nombre de blocks</h3>
                        <input type="text" id="number_of_blocks" placeholder="par exemple: 30">
                    </div>
                    <div class="input-container">
                        <h3>Nombre de stimuli par block</h3>
                        <input type="text" id="number_per_blocks-adjectifs" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-adj" value="option1" style=" height: 50px">
                    </div>
                </div>
                <div class= "input-group">
                    <div class="input-container">
                        <button class="submit" onclick="submitAdjectifs()">Submit</button>
                    </div>
                </div>
            `;
            break;


        case 'emo_faces_nav':
            newContent = `
                <h2>Paradigme pour les visages avec des émotions</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-emo-face" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-emo-face" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Zoom</h3>
                        <input type="text" id="zoom-emo-face" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-emo-face').click()">Choisir un fichier</button>
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-emo-face" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-emo-face" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitFaces()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'emo_voice_nav':
            newContent = `
                <h2>Paradigme pour les voix avec intonation</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-emo-voice" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-emo-voice" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-emo-voice').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-emo-voice" value="option1" style=" height: 50px">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <button class="submit" onclick="submitVoices()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'stroop':
            newContent = `
                <h2>Paradigme pour les mots de couleurs</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-stroop" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-stroop" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-stroop').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-stroop" type="text" placeholder="par exemple: 50">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Choisir la langue</h3>
                        <select id="choice" name="choix">
                            <option value="Anglais">Anglais</option>
                            <option value="Dannois">Dannois</option>
                            <option value="Francais">Français</option>
                        </select>
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-stroop" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-stroop" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitStroop()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'localizer':
            newContent = `
                <h2>Paradigme pour les blocks d'images</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-localizer" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-localizer" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Nombre de blocks</h3>
                        <input type="text" id="number_of_blocks-localizer" placeholder="par exemple: 3">
                    </div>
                    <div class="input-container">
                        <h3>Nombre de stimuli par block</h3>
                        <input type="text" id="number_per_block-localizer" placeholder="par exemple: 5">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée entre les blocks</h3>
                        <input type="text" id="betweenblocks-localizer" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-loca" type="text" placeholder="par exemple: 50">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-local" value="Option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-localizer').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitLocalizer()">Submit</button>
                    </div>
                </div>
            `;
            break;


        case 'cyberball':
            newContent = `
                <h2>Cyberball (paramètre pour l'ordinateur)</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Nom du patient</h3>
                        <input type="text" id="patient_name" placeholder="par exemple: Paul">
                    </div>
                    <div class="input-container">
                        <h3>Durée de la première phase</h3>
                        <input type="text" id="phase1-cyberball" placeholder="par exemple: 120">
                    </div>
                    <div class="input-container">
                        <h3>Durée phase d'exclusion</h3>
                        <input type="text" id="exclusion-cyberball" placeholder="par exemple: 120">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner la photo du patient</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-cyberball').click()">Choisir un fichier</button>
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée phase de Transition</h3>
                        <input type="text" id="transition-cyberball" placeholder="par exemple: 60">
                    </div>
                    <div class="input-container">
                        <h3>Temps de réaction minimum</h3>
                        <input type="text" id="minimum-reaction" placeholder="par exemple: 0.8">
                    </div>
                    <div class="input-container">
                        <h3>Temps de réaction maximum</h3>
                        <input type="text" id="maximum-reaction" placeholder="par exemple: 2.5">
                    </div>
    
                    <div class="input-container">
                        <h3> </h3>
                        <button class="submit" onclick="submitCyberball()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'repetition_priming':
            newContent = `
                <h2>Paradigme de repetition priming</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-priming" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-priming" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Nombre de blocks</h3>
                        <input type="text" id="number_of_blocks-priming" placeholder="par exemple: 3">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-priming').click()">Choisir un fichier</button>
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée entre les blocks</h3>
                        <input type="text" id="betweenblocks-priming" placeholder="par exemple: 5">
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-priming" type="text" placeholder="par exemple: 50">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-priming" value="Option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitpriming()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'Audition':
            newContent = `
                <h2>Paradigme utilisant les cordes vocales</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des instructions</h3>
                        <input type="text" id="instruction-audition" placeholder="par exemple: 2">
                    </div>
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-audition" placeholder="par exemple: 3">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-audition" placeholder="par exemple: 7">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-audition" value="Option1" style=" height: 50px">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-audition" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-audition').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner le son pré-enregistré</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-audition1').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitAudition()">Submit</button>
                    </div>
                </div>
            `;
            break;
        case 'ia-audition':
            newContent = `
                <h2>Paradigme pour l'audition avec l'IA</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes d'attente après le Beep</h3>
                        <input type="text" id="bip-ia-audition" placeholder="par exemple: 1">
                    </div>
                    <div class="input-container">
                        <h3>Durée en secondes container stimulus</h3>
                        <input type="text" id="duration-ia-audition" placeholder="par exemple: 9">
                    </div>
                    <div class="input-container">
                        <h3>Durée en secondes container croix</h3>
                        <input type="text" id="fixation-ia-audition" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-ia-audition" value="option1" style=" height: 50px">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-ia-audition" type="text" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3>Durée en secondes d'attente après la croix</h3>
                        <input type="text" id="after-fixation-ia-audition" placeholder="par exemple: 0.5">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-ia-audition').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitIaAudition()">Submit</button>
                    </div>
                </div>
            `;
            break;

        case 'ia-image':
            newContent = `
                <h2>Paradigme pour les images avec l'IA</h2>
                <div class="input-group">
                    <div class="input-container">
                        <h3>Durée en secondes des stimuli</h3>
                        <input type="text" id="duration-ia-image" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Durée entre les stimuli</h3>
                        <input type="text" id="betweenstimuli-ia-image" placeholder="par exemple: 4">
                    </div>
                    <div class="input-container">
                        <h3>Pourcentage de zoom</h3>
                        <input id="zoom-ia-image" type="text" placeholder="par exemple: 50">
                    </div>
                    <div class="input-container">
                        <h3> Écart type </h3>
                        <input id="sigma-ia-image" type="text" placeholder="par exemple: 0.5">
                    </div>
                </div>
                <div class="input-group">
                    <div class="input-container">
                        <h3> Ordre aléatoire </h3>
                        <input  type="checkbox" id="random-ia-image" value="option1" style=" height: 50px">
                    </div>
                    <div class="input-container">
                        <h3>Sélectionner un paradigme déjà existant</h3>
                        <button class="button-choice" onclick="document.getElementById('fileinput-ia-image').click()">Choisir un fichier</button>
                    </div>
                    <div class="input-container">
                        <h3></h3>
                        <button class="submit" onclick="submitIaImage()">Submit</button>
                    </div>
                </div>
            `;
            break;



        default:
            newContent = `
                <h2>Bienvenue</h2>
                <p>Cliquez sur les éléments de la barre latérale pour changer ce contenu.</p>
            `;
    }

    mainContent.innerHTML = newContent;
    }


function ParadigmCreation() {
    location.href = '/index';
}

function ParadigmCreated() {
    location.href = '/created_paradigmes';
}

function openPopup(name) {
    document.getElementById(name).style.display = 'flex';
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

function submitPopup() {
    var input = document.getElementById('patientInput').value;
    document.getElementById('patientName').textContent = input; // Met à jour le nom du patient
    document.getElementById('popupOverlay').style.display = 'none'; // Ferme la pop-up
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

function submitText() {
    const duration = document.getElementById('duration').value || 'Non spécifié';
    const words = document.getElementById('words').value || 'Non spécifié';
    const zoom = document.getElementById('zoom').value || 'Non spécifié';
    const fixation = document.getElementById('text-fixation').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput');
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-text").checked;


    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }

    if (!fileName && words=='Non spécifié'){
        alert('Veuillez sélectionner un fichier ou entrer des mots avant de soumettre.');
        return;
    }

    // Envoyer les données au serveur
    fetch('/submit-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            fixation: fixation,
            words: words,
            zoom: zoom,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            activation: activation,
            random: random,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitVoices(){
    const duration = document.getElementById('duration-emo-voice').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-emo-voice').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-emo-voice');
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-emo-voice").checked;

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }

    if (!fileName){
        alert('Veuillez sélectionner un fichier ou entrer des mots avant de soumettre.');
        return;
    }

    // Envoyer les données au serveur
    fetch('/submit-emo-voice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            activation: activation,
            baudrate: baudrate,
            trigger: trigger,
            random: random,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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


function submitIaAudition() {
    const fileInput = document.getElementById('fileinput-ia-audition');
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();
    const duration = document.getElementById('duration-ia-audition').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('fixation-ia-audition').value || 'Non spécifié';
    const afterfixation = document.getElementById('after-fixation-ia-audition').value || 'Non spécifié';
    const bip = document.getElementById('bip-ia-audition').value || 'Non spécifié';
    const sigma = document.getElementById("sigma-ia-audition").value || 'Non spécifié';
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const random = document.getElementById("random-ia-audition").checked;

    fetch('/submit_ia_audition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                duration : duration,
                betweenstimuli : betweenstimuli,
                afterfixation : afterfixation,
                bip : bip,
                filePath: fileName,
                random: random,
                output_file: output_file,
                sigma: sigma,
                launching_text: launching_text
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

function submitIaImage() {
    const fileInput = document.getElementById('fileinput-ia-image');
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniq
    const duration = document.getElementById('duration-ia-image').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-ia-image').value || 'Non spécifié';
    const zoom = document.getElementById('zoom-ia-image').value || 'Non spécifié';
    const sigma = document.getElementById("sigma-ia-image").value || 'Non spécifié';
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const random = document.getElementById("random-ia-image").checked;


    fetch('/submit_ia_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filePath: fileName,
                output_file: output_file,
                duration : duration,
                sigma : sigma,
                random: random,
                betweenstimuli : betweenstimuli,
                zoom : zoom,
                launching_text: launching_text
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


function submitFaces() {
    const duration = document.getElementById('duration-emo-face').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-emo-face').value || 'Non spécifié';
    const zoom = document.getElementById('zoom-emo-face').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-emo-face');
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-emo-face").checked;
    const sigma = document.getElementById("sigma-emo-face").value || 'Non spécifié';


    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }
    if (!fileName){
        alert('Veuillez sélectionner un fichier ou entrer des mots avant de soumettre.');
        return;
    }


    // Envoyer les données au serveur
    fetch('/submit-emo-faces', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            zoom: zoom,
            activation: activation,
            random: random,
            baudrate: baudrate,
            sigma: sigma,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitStroop(){
    const duration = document.getElementById('duration-stroop').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-stroop').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-stroop');
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const zoom = document.getElementById('zoom-stroop').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    const choice = document.getElementById('choice').value || 'Non spécifié';
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-stroop").checked;
    const sigma = document.getElementById("sigma-stroop").value || 'Non spécifié';


    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }

    if (!fileName){
        alert('Veuillez sélectionner un fichier ou entrer des mots avant de soumettre.');
        return;
    }

    // Envoyer les données au serveur
    fetch('/submit-stroop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            zoom: zoom,
            choice: choice,
            output_file: output_file,
            launching_text: launching_text,
            port: port,
            activation: activation,
            random: random,
            sigma: sigma,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitLocalizer(){
    const duration = document.getElementById('duration-localizer').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-localizer').value || 'Non spécifié';
    const betweenblocks = document.getElementById('betweenblocks-localizer').value || 'Non spécifié';
    const zoom = document.getElementById('zoom-loca').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const blocks = document.getElementById("number_of_blocks-localizer").value || 'Non spécifié';
    const per_blocks = document.getElementById("number_per_block-localizer").value || 'Non spécifié';
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-local").checked;
    const fileInput = document.getElementById('fileinput-localizer');
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }


    // Envoyer les données au serveur
    fetch('/submit-localizer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            betweenblocks: betweenblocks,
            port: port,
            activation: activation,
            launching_text: launching_text,
            random: random,
            baudrate: baudrate,
            fileName: fileName,
            trigger: trigger,
            blocks: blocks,
            zoom: zoom,
            per_blocks: per_blocks,
            output_file: output_file,
            hauteur: hauteur,
            largeur: largeur
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

function submitAudition(){
    const instruction = document.getElementById('instruction-audition').value || 'Non spécifié';
    const duration = document.getElementById('duration-audition').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-audition').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-audition").checked;
    const fileInput = document.getElementById('fileinput-audition');
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const fileInput1 = document.getElementById('fileinput-audition1');
    let fileName1 = fileInput1.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const sigma = document.getElementById('sigma-audition').value || 'Non spécifié';

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }


    // Envoyer les données au serveur
    fetch('/submit-audition', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            instruction: instruction,
            duration: duration,
            betweenstimuli: betweenstimuli,
            port: port,
            activation: activation,
            launching_text: launching_text,
            random: random,
            sigma: sigma,
            baudrate: baudrate,
            fileName: fileName,
            ASound: fileName1,
            trigger: trigger,
            output_file: output_file,
            hauteur: hauteur,
            largeur: largeur
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


function submitpriming(){
    const duration = document.getElementById('duration-priming').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-priming').value || 'Non spécifié';
    const betweenblocks = document.getElementById('betweenblocks-priming').value || 'Non spécifié';
    const zoom = document.getElementById('zoom-priming').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const blocks = document.getElementById("number_of_blocks-priming").value || 'Non spécifié';
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-priming").checked;
    const fileInput = document.getElementById('fileinput-priming');
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }


    // Envoyer les données au serveur
    fetch('/submit-priming', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            betweenblocks: betweenblocks,
            port: port,
            activation: activation,
            launching_text: launching_text,
            random: random,
            baudrate: baudrate,
            fileName: fileName,
            trigger: trigger,
            blocks: blocks,
            zoom: zoom,
            output_file: output_file,
            hauteur: hauteur,
            largeur: largeur
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


function submitAdjectifs() {
    const duration = document.getElementById('duration-adjectifs').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-adjectifs').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-adjectifs');
    const blocks = document.getElementById("number_of_blocks").value || 'Non spécifié';
    const entrainement_blocks = document.getElementById("number_of_blocks-entrainement").value || 'Non spécifié';
    const per_block = document.getElementById("number_per_blocks-adjectifs").value || 'Non spécifié';
    const zoom = document.getElementById('zoom-adjectifs').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();  // Cela extraira uniquement le nom du fichier.
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-adj").checked;
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }

    if (!fileName){
        alert('Veuillez sélectionner un fichier ou entrer des mots avant de soumettre.');
        return;
    }


    // Envoyer les données au serveur
    fetch('/submit-adjectifs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            blocks: blocks,
            entrainement: entrainement_blocks,
            zoom: zoom,
            per_block: per_block,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            activation: activation,
            random: random,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitCyberball(){
    const premiere_phase = document.getElementById('phase1-cyberball').value || 'Non spécifié';
    const exclusion = document.getElementById('exclusion-cyberball').value || 'Non spécifié';
    const transition = document.getElementById('transition-cyberball').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-cyberball');
    const patient_name = document.getElementById('patient_name').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    const minimum = document.getElementById('minimum-reaction').value || 'Non spécifié';
    const maximum = document.getElementById('maximum-reaction').value ||'Non spécifié';
    let trigger = document.getElementById('resultTrigger').textContent;
    let fileName = fileInput.value.split('\\').pop();
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();

    if (!fileName) {
        alert('Veuillez sélectionner un fichier avant de soumettre.');
        return;  // Arrête l'exécution si aucun fichier n'est sélectionné
    }

    if (trigger == "Patient"){
        trigger = "s"
    }

    fetch('/submit-cyberball', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            premiere_phase: premiere_phase,
            exclusion: exclusion,
            transition: transition,
            minimum: minimum,
            patient_name: patient_name,
            launching_text: launching_text,
            maximum: maximum,
            trigger: trigger,
            output_file: output_file,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitImages(){
    const duration = document.getElementById('duration-image').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-image');
    const zoom = document.getElementById('zoom-image').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-image").checked;
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();
    const sigma = document.getElementById("sigma-image").value || 'Non spécifié';

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();


    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }


    if (!fileName) {
        alert('Veuillez sélectionner un fichier avant de soumettre.');
        return;  // Arrête l'exécution si aucun fichier n'est sélectionné
    }

    // Envoyer les données au serveur
    fetch('/submit-images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            zoom: zoom,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            activation: activation,
            random: random,
            sigma: sigma,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

function submitVideos(){
    const duration = document.getElementById('duration-video').value || 'Non spécifié';
    const betweenstimuli = document.getElementById('betweenstimuli-video').value || 'Non spécifié';
    const fileInput = document.getElementById('fileinput-video');
    const zoom = document.getElementById('zoom-video').value || 'Non spécifié';
    const output_file = document.getElementById('patientName').textContent;
    let fileName = fileInput.value.split('\\').pop();
    const activation = document.getElementById("option1").checked;
    const random = document.getElementById("random-video").checked;
    const sigma = document.getElementById('sigma-video').value || 'Non spécifié';

    let port = document.getElementById('resultPort').textContent.trim();
    let baudrate = document.getElementById('resultBaudrate').textContent;
    let trigger = document.getElementById('resultTrigger').textContent.trim();
    let hauteur = document.getElementById('hauteur').value || '0';
    let largeur = document.getElementById('largeur').value || '0';
    const fileLaunching = document.getElementById('launching_text');
    let launching_text =  fileLaunching.value.split('\\').pop();

    if (baudrate === "" || port === "") {
        baudrate = -1; // Garder les valeurs comme chaîne pour la consistance
        port = 'Patient'; // Remplacer 'Patient' avec une valeur appropriée
    }

    if (trigger === ""){
        trigger = "s"
    }

    if (!fileName) {
        alert('Veuillez sélectionner un fichier avant de soumettre.');
        return;  // Arrête l'exécution si aucun fichier n'est sélectionné
    }

    if (trigger=="Patient"){
        trigger="s"
    }
    // Envoyer les données au serveur
    fetch('/submit-videos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            betweenstimuli: betweenstimuli,
            zoom: zoom,
            output_file: output_file,
            port: port,
            launching_text: launching_text,
            activation: activation,
            random: random,
            sigma: sigma,
            baudrate: baudrate,
            trigger: trigger,
            hauteur: hauteur,
            largeur: largeur,
            filePath: fileName // Envoyer la valeur de l'input de fichier comme un simple string
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

document.addEventListener('DOMContentLoaded', function() {
    const toggleIcon = document.getElementById('lang-icon');
    const langNL = document.getElementById('lang-nl');
    const langFR = document.getElementById('lang-fr');


    if (toggleIcon) {
        toggleIcon.addEventListener('click', function () {
            window.location.href = '/nl/about';
        });
    }

    if (langNL) {
        langNL.addEventListener('click', function () {
            window.location.href = '/nl/about';
        });
    }
})