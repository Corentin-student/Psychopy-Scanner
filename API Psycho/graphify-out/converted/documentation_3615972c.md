<!-- converted from documentation.docx -->

Manuel d'utilisation de l'application de création et d'exécution de paradigmes psychologiques
1. Introduction rapide
Cette application a été conçue pour simplifier la création, la personnalisation et l'exécution de paradigmes psychologiques destinés à des expériences en clinique et en recherche. Ce manuel explique comment utiliser l'interface et configurer les paradigmes, sans avoir besoin de connaître les aspects techniques de l'installation ou du lancement de l'application.
2. Présentation générale de l'interface
L'application est divisée en trois principales sections accessibles depuis la barre de navigation :
Paradigmes prédéfinis : lancer rapidement des paradigmes standards.
Création de paradigme : construire un nouveau paradigme sur mesure.
Paradigmes créés : retrouver et exécuter les paradigmes personnalisés.
3. Utiliser un paradigme prédéfini
Accéder
Cliquer sur Paradigmes principaux.
Étapes
Sélectionner un paradigme dans la barre latérale.
Remplir l'intégralité des paramètres demandés :
Exemple : durée des stimuli, durée de fixation croisée, liste des stimuli, zoom, etc.
Sélectionner obligatoirement :
Un fichier d’instructions : contient les slides expliquant au patient ce qu’il devra faire.
Un fichier contenant les stimuli : contient les éléments qui seront présentés lors du paradigme (images, vidéos ou sons).
Important :
➔ Si un paramètre requis est manquant, mal renseigné, ou si un fichier obligatoire n'est pas sélectionné, le paradigme crashera brutalement dès son lancement.
➔ Aucun message d'erreur n’indiquera précisément la cause : le crash sera immédiat si la configuration est incorrecte.
Cliquer sur "Submit" pour envoyer la configuration et démarrer l'expérience.

Remarque essentielle
Les dossiers correspondant à chaque paradigme sont déjà créés avec un nom cohérent par rapport au paradigme qu'ils représentent.
Il est indispensable d’utiliser ces dossiers existants sans en changer le nom.
➔ Par exemple, pour le paradigme EMO FACE :
Le fichier d’instructions et le fichier contenant les stimuli doivent être placés dans le dossier nommé Paradigme_EMO_FACE.
À l’intérieur de ce dossier, vous trouverez généralement un sous-dossier prévu pour accueillir les stimuli (images, vidéos ou sons).
Tous les dossiers des paradigmes se trouvent dans le répertoire principal Input.
Attention :
➔ Si vous déplacez les fichiers dans un mauvais dossier ou si vous modifiez le nom d’un dossier, le paradigme ne pourra pas se lancer et plantera immédiatement.
Un exemple d’organisation correcte est présenté dans l’image ci-dessous :









4. Créer un nouveau paradigme personnalisé
Accéder
Cliquer sur Création de Paradigme.
Principe
Construire visuellement un scénario expérimental en ajoutant des stimuli successifs.
Étapes
A. Utiliser les boutons pour ajouter :
Instructions (fichiers de slides de début et de fin).
Images, vidéos, sons, enregistrements vocaux, croix de fixation.
B. Pour chaque stimulus, spécifier :
Moment d'apparition (en secondes).
Durée d'affichage.
(Optionnel) Angle de rotation pour les images.
C. Les stimuli apparaissent dans un tableau avec possibilité de :
Supprimer des entrées.
Visualiser les stimuli en concurrence (stimuli qui se chevauchent).
D. Une fois le paradigme complété :
Vérifier que la timeline est continue (sans trous dans le temps).
Donner un nom au paradigme et sauvegarder.
Remarques essentielles
Il est obligatoire de sélectionner :
Un fichier d’instructions (slides expliquant le paradigme au patient).
Un fichier de fin (slide de remerciement ou d'indication de fin d'expérience).
Important :
➔ Si aucun fichier d’instruction ou de fin n'est renseigné, le paradigme ne pourra pas être lancé ou crashera brutalement dès le lancement.
➔ Aucun message d'erreur n’indiquera la cause : le crash sera immédiat.
Attention – différence importante par rapport aux paradigmes existants :
Pour les paradigmes créés manuellement via cette section,
il n’est pas nécessaire de placer les stimuli dans un dossier spécifique ou portant un nom particulier.
Les fichiers de stimuli peuvent être sélectionnés librement depuis leur emplacement actuel sur votre ordinateur.

5. Utiliser un paradigme créé
Accéder : Cliquer sur Paradigmes Créés.
Étapes :
Choisir un paradigme dans la barre latérale (les paradigmes sauvegardés apparaissent automatiquement).
Visualiser la structure du paradigme (tableau des stimuli).
(Optionnel) Mélanger l'ordre des stimuli avec un bouton dédié.
Cliquer sur Submit pour lancer l'expérience.

6. Sortie de l'application
À la fin de chaque session, plusieurs fichiers de sortie sont automatiquement générés :
Fichiers CSV et TSV :
Contiennent la liste des stimuli présentés.
Enregistrent les timings d’apparition, les réponses éventuelles du patient et d'autres métadonnées utiles.
Fichier PRT :
Format spécial compatible avec BrainVoyager pour l’analyse en imagerie cérébrale.
Ce fichier reprend la chronologie des stimuli pour permettre une corrélation fine avec les données d'imagerie.
Dossiers audios :
Générés pour les paradigmes incluant l’enregistrement de la voix.
Tous les enregistrements audios sont regroupés dans un dossier spécifique lié à la session (nommé avec la date et l'identifiant du patient).
Fichier texte (.txt) :
Un fichier .txt est également généré à chaque session.
Il précise quel paradigme a été lancé ainsi que tous les paramètres utilisés (durées, options cochées, fichiers sélectionnés, etc.).
Ce fichier permet d’avoir une trace écrite complète de la configuration de l'expérience, ce qui facilite les vérifications ou analyses ultérieures.

