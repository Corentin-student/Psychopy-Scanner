import os


def renommer_fichiers_avec_ouverture(dossier: str, prefixe: str):
    try:
        fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]

        for index, fichier in enumerate(fichiers, start=1):
            chemin_original = os.path.join(dossier, fichier)
            nom_original, extension = os.path.splitext(fichier)
            nouveau_nom = f"{prefixe}.{index:02d}.{nom_original}{extension}"
            chemin_nouveau = os.path.join(dossier, nouveau_nom)
            os.rename(chemin_original, chemin_nouveau)
            print(f"Fichier renommé: {fichier} -> {nouveau_nom}")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")


renommer_fichiers_avec_ouverture("parfait", "ACR")
