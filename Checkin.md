# AUDIT COMPLET - Psychopy Scanner + Plan de Refonte IONS

## Contexte
Plateforme de recherche en neurosciences comportementales (fMRI) construite avec Flask + PsychoPy. L'objectif est de la rendre **universellement deployable** (peu importe le site/labo), avec **branding IONS**, et d'**ameliorer la creation de paradigmes**.

---

## 1. ETAT DES LIEUX - QUI A FAIT QUOI

### Commits de Corentin (FIABLE - derniere contribution: 14 fev 2025)
- Toute l'architecture de base: Flask app, 14 paradigmes, UI FR/NL
- Systeme de creation/sauvegarde de paradigmes custom (Psychopy_everything.py)
- Paradigmes: Text, Image, Video, Audition, EMO_FACE, EMO_VOICES, Stroop, Adjectifs, Cyberball, LOCALIZER, Priming, IA_audition, IA_image
- UI complete avec sidebar, gestion patient, port serie, langues FR/NL
- Classe parent `Parente` (heritage OOP pour tous les paradigmes)
- Systeme d'output TSV/CSV/TXT + generation PRT (BrainVoyager)

### Commits de "sweedens" (A VERIFIER - dec 2025 a fev 2026)
- `test commit` / `Delete Input/test.txt` - commits de test
- `Amelioration systeme output + ebauche nouveau paradigm stress` - modifications output + Psychopy_Stress.py
- `modification gestion output` - dernier commit (fev 2026)
- **Psychopy_Stress.py**: INCOMPLET - contient des placeholders ("a remplacer par de vraies figures"), 576 lignes mais beaucoup de code non fonctionnel
- **Route /submit-stress**: COMMENTEE dans application.py (lignes 591-615)
- **Modification serial**: `ser.write(b't')` hardcode a la place de `ser.write(char.encode())` - specifique a un setup (Ron a St-Luc)

---

## 2. CE QUI FONCTIONNE (valide par Corentin)

| Composant | Status | Notes |
|-----------|--------|-------|
| Flask API (18 routes actives) | OK | Toutes les routes sauf /submit-stress |
| 13 paradigmes pre-construits | OK | Text, Image, Video, Audition, EMO_FACE, EMO_VOICES, Stroop, Adjectifs, Cyberball, LOCALIZER, Priming, IA_audition, IA_image |
| Paradigme custom (everything) | OK | Creation libre via tableau de stimuli |
| UI Web FR | OK | Interface complete |
| UI Web NL | OK | Traduction neerlandaise |
| Systeme output TSV/CSV/TXT | OK | Auto-numbering des runs |
| Generation PRT | OK | Pour BrainVoyager |
| Sauvegarde/chargement JSON | OK | Paradigmes personnalises |
| Communication port serie | OK | Trigger scanner fMRI |

## 3. CE QUI NE FONCTIONNE PAS / EST INCOMPLET

| Composant | Status | Detail |
|-----------|--------|--------|
| **Psychopy_Stress.py** | INCOMPLET | Placeholders, pas de vrais stimuli de rotation mentale, logique MIST partielle |
| **Route /submit-stress** | COMMENTEE | Pas accessible depuis l'UI |
| **Stress dans l'UI** | ABSENT | Pas de lien sidebar, pas de formulaire |
| **ser.write(b't')** | HARDCODE | Devrait utiliser le parametre `char` dynamique |

---

## 4. PROBLEMES CRITIQUES POUR L'UNIVERSALITE

### 4.1 Chemins et config hardcodes
- `locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")` - **CRASH sur Windows anglais/neerlandais/allemand** (`Paradigme_parent.py:12`)
- `ser.write(b't')` hardcode au lieu du parametre configurable (`Paradigme_parent.py:137`)
- Port serie et baudrate sans valeur par defaut robuste
- `application.py:661` - `serve()` apres `app.run()` = le serve() n'est jamais atteint (code mort)

### 4.2 Dependance OS
- **PyWin32** dans requirements = Windows-only
- `Psychtoolbox` problematique sur certains OS
- Pas de gestion d'erreur si PsychoPy n'arrive pas a ouvrir une fenetre (ecran non connecte, resolution incompatible)
- Resolution fenetre hardcodee `800x600` dans tous les paradigmes

### 4.3 Securite
- **Path traversal** sur `/get-json-file` - le parametre `param_to_file` n'est pas sanitise (`application.py:64-66`)
- **Path traversal** sur `/upload` - pas de validation du nom de fichier
- **Path traversal** sur `/keep-datas` - injection dans le nom de fichier JSON
- Pas de CORS, pas d'authentification
- `subprocess.run` avec des parametres utilisateur non valides

### 4.4 Architecture
- **Duplication massive de code**: chaque route dans `application.py` fait exactement la meme chose (extraire JSON + subprocess.run) - ~600 lignes pour ce qui pourrait etre ~50 lignes
- **Duplication JS**: `prime.js` (1546 lignes) et `prime-nl.js` (1545 lignes) sont quasi-identiques - seuls les textes changent
- **Duplication HTML**: `prime.html`/`prime-nl.html`, `creating.html`/`creating-nl.html`, `existing.html`/`existing-nl.html` - 6 fichiers pour 3
- **Pas de fichier de config centralise**: chaque parametre est disperse entre JS, HTML, et Python
- **Pas de gestion d'erreurs cote client**: les erreurs subprocess disparaissent silencieusement
- **Pas de logging**: aucun systeme de log, juste des `print()`

### 4.5 UX / Creation de paradigmes
- L'UI de creation custom (`creating.html`) est basique: tableau HTML editable manuellement
- Pas de preview/visualisation avant lancement
- Pas de validation des parametres avant soumission
- Pas de drag & drop pour ordonner les stimuli
- Pas d'import/export de paradigmes entre sites
- Le formulaire de chaque paradigme est genere en HTML brut dans le JS (1500+ lignes de strings HTML dans des switch/case)

---

## 4bis. ENSEIGNEMENTS DU MEMOIRE DE CORENTIN WARZEE (2024-2025)

**Source**: Memoire de master UCLouvain - "Building a GUI to streamline paradigm creation and presentation in psychology"
**Superviseurs**: Benoit Macq, Laurence Dricot | **Readers**: Nicolas Delinte, Sebastien Jodogne, Ron Kupers

### Pipeline de donnees confirme
Le TSV/CSV n'est PAS le format final d'analyse. Le pipeline est :
```
Paradigme PsychoPy → TSV/CSV (intermediaire) → PRT (writtingprt.py) → BrainVoyager
```
Le **PRT** est le format qui compte pour l'analyse fMRI (design matrix → GLM → beta coefficients).
BIDS n'est pas utilise dans leur workflow - ils utilisent BrainVoyager, pas fMRIPrep/SPM.

### Problemes documentes par Corentin

1. **Installation = point bloquant majeur** (p.48)
   - "Each installation required someone with advanced computer skills"
   - "The people who had to run the application had to go through the code editor to launch it"
   - → Confirme la necessite absolue du LOT 5 (installeur)

2. **PyInstaller a echoue pour un executable unique** (p.48-49)
   - Flask + PsychoPy ne peuvent pas coexister dans un seul .exe
   - Solution de Corentin : executables SEPARES par paradigme (~1h30 de compilation chacun)
   - → Le LOT 5 doit prendre en compte cette contrainte technique. Strategie probable : Flask en .exe + paradigmes en .exe separes, ou bien approche embedded Python

3. **Videos avec fond bleu = crash PsychoPy** (p.49)
   - Contournement : re-encoder les videos au bon format
   - → Ajouter une validation/conversion automatique des stimuli video dans le LOT 3

4. **Synchronisation audio fragile** (p.49-50)
   - Threads pour son + enregistrement vocal : "encoding results were occasionally incomplete, with crucial data lost"
   - → Bug connu, a surveiller lors du refactoring

5. **Timing pas au sample pres mais onset enregistre correctement** (p.54)
   - Les videos ont des delais de chargement reels
   - Mais "the tool's ability to accurately record the moments of onset" est fiable
   - → Le timing d'affichage peut varier, mais les donnees de sortie (onset reel) sont correctes

6. **Tests existants** (p.52)
   - Tests.py couvre 91% de Tests.py et 88% de application.py
   - Tests : routes Flask, gestion JSON, mock des subprocess, cas d'erreur
   - → Base de tests existante a preserver et etendre lors du refactoring

### Limitations identifiees par Corentin (chapitre 11, p.54)
- Delais de chargement variables selon le type de stimulus (images < audio < videos)
- Synchronisation recording + stimuli complexe
- L'important n'est pas la precision d'affichage au ms pres mais l'enregistrement fiable des onsets reels

---

## 5. PLAN DE TRAVAIL - DEVIS PAR LOT

### LOT 1: ~~Refactoring Architecture + i18n~~ (RETIRE DU DEVIS)
*Note interne : sans ce lot, chaque modif ulterieure (Lot 4 surtout) sera ~2x plus longue a cause de la duplication FR/NL et des 600 lignes de routes dupliquees. A ressortir si pression sur les delais.*

---

### LOT 2: Universalite / Portabilite Windows (Priorite HAUTE)
**Objectif**: L'app tourne sur n'importe quel poste Windows sans config manuelle (Mac hors scope)

1. **Fichier de configuration centralise** (`config.yaml` ou `config.json`)
   - Locale, chemins, port serie par defaut, resolution ecran, langue par defaut
   - Fichiers: `application.py`, `Paradigme_parent.py`, tous les paradigmes

2. **Fix locale crash**
   - Remplacer `locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")` par une detection automatique avec fallback
   - Fichier: `Paradigme_parent.py:12`

3. **Fix serial dynamique**
   - Restaurer `ser.write(char.encode())` au lieu de `ser.write(b't')` hardcode
   - Fichier: `Paradigme_parent.py:137`

4. **Fix serveur**
   - `app.run()` bloque, donc `serve()` n'est jamais appele - choisir l'un ou l'autre
   - Fichier: `application.py:658-661`

5. **Resolution ecran adaptative**
   - Detecter la resolution ecran au lieu de hardcoder 800x600
   - Fichiers: tous les `Psychopy_*.py`

6. **Requirements Windows propres**
   - Verrouiller les versions, retirer les deps inutiles
   - Fichier: `requirements.txt`

**Estimation**: ~2-3 jours de dev (Mac retire du scope)

---

### LOT 3: Constructeur de Paradigmes par Regles (Priorite HAUTE)
**Objectif**: Creer un facilitateur PsychoPy - l'utilisateur definit des REGLES, pas des stimuli un par un

**Probleme actuel**: L'editeur custom (`creating.html`) force l'utilisateur a placer chaque stimulus manuellement dans un tableau (apparition, duree, type, fichier...). Pour un paradigme de 200 trials, c'est inutilisable.

**Vision**: Un constructeur de regles ou l'utilisateur definit le PATTERN de son paradigme, et le systeme genere la sequence complete.

#### Concept: "Rule Builder"

1. **Definition de blocs par regles**
   - L'utilisateur definit un bloc type : "Stimulus [image/texte/son/video] pendant X sec → Croix de fixation pendant Y sec"
   - Parametres du bloc : duree stimulus, duree fixation, jitter (sigma), type de reponse attendue (clic, touche, aucune)
   - Repetitions : "Repeter ce bloc N fois" ou "Parcourir toute la liste de stimuli"
   - Exemple concret :
     ```
     BLOC "Faces emotionnelles" :
       1. Croix de fixation : 2s (jitter sigma=0.3)
       2. Image du dossier /Paradigme_EMO_FACE/ : 4s
       3. Ecran de reponse : jusqu'a reponse (max 3s)
       → Parcourir tous les fichiers du dossier, ordre aleatoire
       → 3 repetitions du set complet
     ```

2. **Enchainement de blocs**
   - Possibilite de combiner plusieurs blocs dans un paradigme
   - Exemple : Bloc instructions → Bloc entrainement (5 trials) → Bloc principal (100 trials) → Ecran fin
   - Pauses configurables entre blocs

3. **Sources de stimuli intelligentes**
   - "Tous les fichiers du dossier X" (auto-detection images/sons/videos)
   - "Liste depuis fichier .txt/.csv"
   - "Liste manuelle" (saisie directe)
   - Filtres : par extension, par pattern de nom

4. **Regles de timing flexibles**
   - Duree fixe : "toujours 4 secondes"
   - Duree avec jitter : "4s ± 0.5s (gaussien)"
   - Duree adaptative : "jusqu'a reponse du sujet (max Xs)"
   - Duree du media : "duree naturelle de la video/du son"

5. **Regles de reponse**
   - Aucune reponse attendue (affichage passif)
   - Touche clavier (quelle(s) touche(s))
   - Clic souris
   - Enregistrement vocal
   - Timeout configurable

6. **Preview et validation**
   - Resume textuel : "Ce paradigme contient 3 blocs, 156 trials, duree estimee ~12min"
   - Timeline schematique (barre visuelle des blocs)
   - Verification : fichiers existent ? durees coherentes ?

7. **Import/Export**
   - Export de la config de regles en JSON (partageable entre labos)
   - Import depuis JSON
   - Templates pre-faits : "Block design classique", "Event-related", "Mixed design"

#### Ce que ca remplace
- Le tableau manuel actuel dans `creating.html` → devient un mode "avance" optionnel
- Les 13 paradigmes pre-construits restent disponibles tels quels dans la sidebar
- Le rule builder genere un JSON compatible avec `Psychopy_everything.py` (ou un nouveau runner)

**Estimation**: ~8-10 jours de dev (plus ambitieux mais beaucoup plus de valeur)

---

### LOT 4: Refonte Visuelle UI + Integration Branding (Priorite HAUTE)
**Objectif**: Moderniser l'interface, la rendre professionnelle et prete a recevoir le branding IONS

**Note**: Le branding IONS (logo, couleurs, charte) est fait par le client. Ce lot couvre la refonte technique/visuelle de l'UI et l'integration du branding fourni.

1. **Modernisation de l'interface**
   - Refonte du layout : header, sidebar, contenu principal (actuellement tres basique/brut)
   - Design responsive propre (les media queries actuelles sont minimales)
   - Formulaires paradigmes : champs mieux organises, labels clairs, groupes logiques
   - Feedback utilisateur : etats de chargement, messages d'erreur clairs, confirmations
   - Remplacement des formulaires HTML bruts dans le JS (1500+ lignes de strings) par un systeme de templates
   - Fichiers: `style.css`, `style_index.css`, templates HTML, JS

2. **Integration du branding IONS (fourni par le client)**
   - Slot logo dans le header (remplacement de "Ion's Psychopy")
   - Palette de couleurs parametrable (variables CSS) pour appliquer facilement la charte IONS
   - Favicon configurable
   - Footer avec version + credits
   - Fichiers: `style.css`, templates HTML

3. **Page d'accueil**
   - Ecran d'accueil avec logo au lieu d'atterrir directement sur les paradigmes
   - Choix de langue au premier lancement
   - Resume rapide : combien de paradigmes disponibles, dernier patient, etc.

**Estimation**: ~3-4 jours de dev (hors creation du branding, fait par le client)

---

### LOT 5: Installeur Facile Windows (Priorite HAUTE)
**Objectif**: Un utilisateur non-technique installe l'app en 2 clics, sans toucher a Python/pip/terminal

**Probleme actuel**: Pour lancer l'app il faut : installer Python, pip install des 40+ packages (certains compilent en C), lancer `python application.py` depuis le terminal. Inacceptable pour un chercheur non-dev.

1. **Installeur Windows (.exe / .msi)**
   - **Attention** : Corentin a deja tente PyInstaller (memoire p.48-49). Flask + PsychoPy ne fonctionnent PAS dans un seul .exe. Sa solution : executables SEPARES par paradigme (~1h30 de compilation chacun)
   - Strategie recommandee : **Flask en .exe** (serveur web) + **chaque paradigme en .exe separe** (PsychoPy), le tout dans un installeur unique (NSIS, Inno Setup, ou .msi)
   - Alternative a explorer : Python embarque (embedded Python) avec pip pre-installe, evite la compilation PyInstaller
   - Auto-lancement du navigateur web a l'ouverture
   - Icone IONS sur le raccourci
   - Fichiers: nouveau script de build, `application.py` (adaptation entry point)

2. **Gestion des dependances problematiques**
   - PsychoPy + Psychtoolbox : gros paquets avec des deps C - tests de packaging
   - PyAudio : necessite PortAudio (inclure les binaires)
   - OpenCV : version headless possible pour reduire la taille
   - PyWin32 : conditionnel Windows only dans le build

4. **Script de build automatise**
   - `build.py` ou Makefile qui produit l'installeur en une commande
   - CI/CD possible (GitHub Actions) pour generer les installeurs automatiquement
   - Versionning automatique

5. **Premier lancement**
   - Detection automatique de la config (port serie, resolution ecran)
   - Wizard de premiere configuration si necessaire
   - Verification que PsychoPy peut ouvrir une fenetre

**Estimation avec risque technique** :
- Windows : ~6-8 jours (Corentin a deja echoue sur le .exe unique, la contrainte Flask+PsychoPy n'a pas change)
- Mac : ~3-5 jours supplementaires MAIS **risque technique eleve** :
  - PsychoPy sur Mac : Gatekeeper, OpenGL deprecated par Apple (Metal), compatibilite Intel vs Apple Silicon (M1/M2/M3)
  - PyInstaller sur Mac : jamais teste dans ce projet, zero retour d'experience
  - Peut etre simple ou etre un mur technique complet - impossible a estimer sans R&D
- **Total installeurs : ~9-13 jours de dev, avec risque de depassement**

**ALERTE RISQUE** : C'est le lot le plus risque du devis. Corentin y a passe du temps significatif (memoire p.48-49) et a du se rabattre sur des .exe separes par paradigme (~1h30 de compilation chacun, 14 paradigmes). Les pistes alternatives (embedded Python, Docker, Electron) n'ont pas ete testees et ne sont pas garanties. Prevoir une phase de R&D/prototypage de 2-3 jours avant de s'engager sur l'estimation finale.

---

### LOT 6: Paradigme Stress (MIST) (Priorite BASSE)
**Objectif**: Finaliser le paradigme de stress inacheve

1. **Completer Psychopy_Stress.py**
   - Vrais stimuli de rotation mentale (generes ou charges)
   - Logique MIST complete (arithmetique + pression temporelle + feedback social)
   - Tests
   - Fichier: `Psychopy_Stress.py`

2. **Decomenter et integrer la route**
   - Fichier: `application.py:591-615`

3. **Ajouter dans l'UI**
   - Lien sidebar + formulaire de parametres
   - Fichiers: `prime.js`, `prime-nl.js`, `prime.html`, `prime-nl.html`

**Estimation**: ~3-4 jours de dev

---

### LOT 7: ~~Structuration Donnees + Regles d'Output~~ (RETIRE DU DEVIS)
*Note interne : le client n'a pas pousse dessus. Le format actuel fonctionne chez Ron, on garde tel quel. Section conservee ci-dessous pour reference future si besoin.*

#### (Reference - non devise)
**Objectif**: Des donnees exploitables immediatement, avec un systeme de regles d'output configurable par site

**Rappel du pipeline** : les TSV/CSV sont des fichiers intermediaires. Le fichier final pour l'analyse fMRI est le **PRT** (genere par `writtingprt.py`), importe dans **BrainVoyager** pour construire la design matrix et le GLM.

**Problemes actuels identifies** :

1. **Format intermediaire non configurable**
   - Separateur decimal virgule (`0,0136...`) - fonctionne chez Ron mais pas universel
   - Le "TSV" utilise `;` au lieu de `\t` (pas un vrai TSV)
   - Pas de moyen de changer le format sans modifier le code

2. **Noms de fichiers avec espaces** : `2026-01-13_Patient ID_run1.tsv`
   - Problematique pour scripts d'analyse et lignes de commande

3. **Chaque paradigme ecrit ses colonnes differemment**
   - Pas d'harmonisation entre paradigmes

4. **Double ecriture TSV + CSV identique**
   - Les deux fichiers ont le meme contenu et le meme separateur (`;`)

5. **Metadonnees informelles** (.txt avec `cle = valeur`)

**Note importante** : le format actuel fonctionne chez Ron. On ne casse RIEN. On ajoute un systeme de profils.

**Plan** :

1. **Systeme de regles/profils d'output configurable**
   - L'admin du site definit son profil d'output via l'UI ou un fichier de config :
     ```
     Profil "Ron - St-Luc" (DEFAUT - retrocompatible) :
       separateur_colonnes: ";"
       separateur_decimal: ","
       formats: [".tsv", ".csv"]
       nommage: "{date}_{patient}_run{run}"
       generer_prt: true
     
     Profil "International" :
       separateur_colonnes: "\t"
       separateur_decimal: "."
       formats: [".tsv"]
       nommage: "{date}_{patient}_task-{paradigme}_run-{run}"
       generer_prt: true
     
     Profil "Excel-friendly" :
       separateur_colonnes: ";"
       separateur_decimal: ","
       formats: [".csv"]
       encodage: "utf-8-bom"
       generer_prt: false
     ```
   - Le profil actuel de Ron = profil par defaut, zero changement pour lui

2. **Nommage configurable**
   - Template avec variables : `{date}`, `{patient}`, `{paradigme}`, `{run}`
   - Option : remplacer espaces par underscores

3. **Colonnes harmonisees (optionnel)**
   - Memes noms de colonnes de base entre paradigmes : `onset`, `duration`, `trial_type`, `stim_file`
   - Colonnes supplementaires specifiques par paradigme

4. **Amelioration PRT**
   - Le PRT est le fichier cle pour BrainVoyager - s'assurer qu'il est genere systematiquement
   - Inclure la generation PRT dans le profil d'output (activable/desactivable)

5. **Metadonnees en JSON sidecar (en plus du .txt actuel)**
   - Garder le .txt pour retrocompatibilite
   - Ajouter un .json optionnel : version app, parametres complets

6. **Profil BIDS (optionnel, pour open source / universalite)**
   - BIDS = Brain Imaging Data Structure, standard international pour les donnees de neuroimagerie
   - Quasi-obligatoire pour : publier sur OpenNeuro, utiliser fMRIPrep, collaborer avec des labos qui utilisent SPM/FSL/AFNI au lieu de BrainVoyager
   - Concretement c'est un profil d'output pre-configure :
     ```
     Profil "BIDS" :
       structure: sub-{patient}/func/
       nommage: "sub-{patient}_task-{paradigme}_run-{run}_events"
       separateur_colonnes: "\t" (tabulation)
       separateur_decimal: "."
       colonnes: onset, duration, trial_type, response_time, stim_file
       sidecar: .json (metadata BIDS-compliant)
       extension: ".tsv"
     ```
   - Les donnees existent deja dans les TSV actuels - c'est un reformatage, pas une refonte
   - Pas utile pour Ron (BrainVoyager + PRT), mais indispensable pour l'adoption open source IONS
   - Ne remplace pas le PRT - les deux coexistent (BIDS pour les labos SPM/FSL, PRT pour BrainVoyager)

**Estimation**: ~2-3 jours de dev (le code d'ecriture existe deja dans Paradigme_parent.py, c'est un refactor de write_tsv_csv() + float_to_csv() avec un dictionnaire de config)

---

### LOT 8: Open Source & Documentation (Priorite MOYENNE)
**Objectif**: Rendre le projet publiable en open source sous le nom IONS

**Contexte** (extrait du mail a Ron) : *"si tu penses que l'outil a une valeur au-delà du labo, on pourrait aussi envisager d'y intégrer le branding de l'IONS et de le rendre disponible plus largement en open source. Cela pourrait donner une belle visibilité à l'institut."*

1. **Nettoyage du repo**
   - Supprimer les fichiers de test, outputs d'exemple, donnees patients
   - `.gitignore` propre (Fichiers_output/, uploads/, *.pyc, __pycache__)
   - Supprimer l'historique git sensible si necessaire (nouveau repo propre)

2. **Documentation**
   - README.md professionnel : description, screenshots, installation, usage
   - Guide utilisateur : comment creer un paradigme, lancer une experience, recuperer les donnees
   - Guide developpeur : architecture, comment ajouter un paradigme
   - CONTRIBUTING.md : comment contribuer

3. **Licence**
   - Choix de licence open source (MIT, GPL, Apache 2.0...)
   - A valider avec Ron/IONS

4. **CI/CD**
   - GitHub Actions : tests automatiques, build installeurs
   - Releases automatiques avec versionning semantique (v1.0.0, v1.1.0...)

5. **Support et maintenance**
   - Modele de support ponctuel (tickets GitHub Issues)
   - Documentation des problemes connus et solutions
   - Template de bug report / feature request

**Estimation**: ~1-2 jours de dev (nettoyage repo + README pro + licence + CI basique. Le memoire sert de base pour la doc dev)

---

## 6. DECISIONS PRISES

- **Branding IONS**: le client fournit la charte (logo, couleurs, police). Le dev integre.
- **Langues**: FR + NL + EN (anglais a ajouter)
- **Stress MIST**: pas prioritaire, on garde pour plus tard
- **OS**: Windows + Mac (pas Linux)
- **Installeur**: indispensable pour que les chercheurs non-dev puissent utiliser l'app

## 7. RESUME DEVIS FINAL

| Lot | Description | Estimation | Priorite |
|-----|-------------|------------|----------|
| 2 | Portabilite Windows | 2-3 jours | HAUTE |
| 3 | Constructeur de Paradigmes par Regles | 8-10 jours | HAUTE |
| 4 | Refonte visuelle UI + integration branding IONS | 3-4 jours | HAUTE |
| 5 | Installeur Windows | 6-8 jours (RISQUE) | HAUTE |
| 8 | Open Source + Documentation | 1-2 jours | HAUTE |

**Lots retires du devis** : 1 (refactoring/i18n), 6 (Stress MIST), 7 (output configurable)

**Total devise** : ~20-27 jours de dev (dont ~6-8 a risque sur installeur)

### Ordre recommande
1. **LOT 2** (portabilite Win) - fix les hardcodes bloquants
2. **LOT 4** (refonte UI + branding IONS)
3. **LOT 3** (constructeur paradigmes par regles) - la plus grosse valeur ajoutee
4. **LOT 5** (installeur Windows) - une fois l'app stable
5. **LOT 8** (open source + docs) - publication finale IONS

### Proposition de phases de livraison

**Phase 1 - Base portable + UI** (Lots 2+4) : ~5-7 jours
→ Livrable : app portable Windows + UI refondue avec branding IONS

**Phase 2 - Creation paradigmes** (Lot 3) : ~8-10 jours
→ Livrable : constructeur de paradigmes par regles

**Phase 3 - Distribution publique** (Lots 5+8) : ~7-10 jours
→ Livrable : installeur Windows + repo open source IONS pret

---

## 8. FICHIERS CRITIQUES A MODIFIER

```
API Psycho/application.py               - Refactoring routes + securite + fix serveur
API Psycho/Python_scripts/Paradigme_parent.py - Fix locale + serial + config
API Psycho/Python_scripts/Psychopy_*.py (x14) - Resolution adaptative
API Psycho/templates/prime.html          - Branding + i18n
API Psycho/templates/creating.html       - Editeur paradigmes
API Psycho/static/prime.js               - Refonte UI + i18n + editeur
API Psycho/static/style.css              - Branding IONS
API Psycho/requirements.txt              - Cross-platform
```

## 9. STACK TECHNIQUE ACTUELLE

**Backend**: Flask 3.0.3, Waitress 3.0.0, PsychoPy, Psychtoolbox 3.0.19
**Frontend**: Vanilla JS, CSS, SweetAlert2, Google Material Symbols
**Data**: Pandas 2.2.2, NumPy 1.26.4, SciPy 1.14.0, Scikit-learn 1.5.1
**Audio**: PyAudio 0.2.14, Pydub 0.25.1, SpeechRecognition 3.10.4, SoundDevice 0.5.0
**Video**: OpenCV 4.10.0, FFpyplayer 4.5.1, Imageio 0.34.2
**Hardware**: Pyserial 3.5, PyWin32 (Windows only), Pyglet 1.4.11
**Total dependencies**: 40+ packages Python
