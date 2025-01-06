import os


def get_file_names(directory):
    # Vérifie si le chemin est valide
    if not os.path.exists(directory):
        print(f"Le dossier {directory} n'existe pas.")
        return []

    # Récupère tous les fichiers dans le dossier
    file_names = []
    for file_name in os.listdir(directory):
        # Vérifie si c'est un fichier (et non un dossier)
        if os.path.isfile(os.path.join(directory, file_name)):
            file_names.append(file_name)

    return file_names


def print_differences(list1, list2):
    # Trouve les éléments qui sont dans list1 mais pas dans list2
    diff_list1 = [item for item in list1 if item not in list2]

    # Trouve les éléments qui sont dans list2 mais pas dans list1
    diff_list2 = [item for item in list2 if item not in list1]

    # Affiche les différences
    print("Éléments dans list1 mais pas dans list2 :", diff_list1)
    print("Éléments dans list2 mais pas dans list1 :", diff_list2)


# Exemple d'utilisation
directory_path = "Stimuli"
file_list = get_file_names(directory_path)
file_list2 = get_file_names("newstimuli")

print_differences(file_list, file_list2)

# Affiche la liste des fichiers
print(len(file_list))
print(len(file_list2))
