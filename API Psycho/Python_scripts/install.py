import subprocess
import sys

requirements_path = 'requirements.txt'

def install_requirements(requirements_file):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("Tous les packages ont été installés avec succès.")
    except subprocess.CalledProcessError as e:
        print("Une erreur est survenue lors de l'installation des packages.")
        print(e)

install_requirements(requirements_path)
