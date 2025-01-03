import sys
import unittest
import os
import json
from unittest.mock import Mock, patch

from application import app  # Remplacez 'app' par le module contenant votre application Flask

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Configure l'application pour les tests
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

        # Configurer le dossier des fichiers de test
        self.upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(self.upload_folder, exist_ok=True)

    def tearDown(self):
        # Nettoyer les fichiers de test
        for file in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, file)
            os.remove(file_path)
        os.rmdir(self.upload_folder)

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a href="#" onclick="changeMainContent(\'long_text\')">Adjectifs positifs/négatifs</a>', response.get_data(as_text=True))
        #ça check le bon fonctionnement de la rédiction plus que ça soit la bonne page

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a href="#" onclick="changeMainContent(\'long_text\')">Adjectifs positifs/négatifs</a>', response.get_data(as_text=True))
        #ça check le bon fonctionnement de la rédiction plus que ça soit la bonne page

    def test_fr_about_route(self):
        response = self.client.get('/fr/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a href="#" onclick="changeMainContent(\'long_text\')">Adjectifs positifs/négatifs</a>', response.get_data(as_text=True))
        # ça check le bon fonctionnement de la rédiction plus que ça soit la bonne page

    def test_nl_about_route(self):
        response = self.client.get('/nl/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<span>Naam poort</span>', response.get_data(as_text=True))
        # ça check le bon fonctionnement de la rédiction plus que ça soit la bonne page


    def test_created_route(self):
        response = self.client.get('/created_paradigmes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1 class="header-center">Création de Paradigme</h1>', response.get_data(as_text=True))
        # ça check le bon fonctionnement de la rédiction plus que ça soit la bonne page
    def test_index_route(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1 class="header-center">Création de Paradigme</h1>', response.get_data(as_text=True))


    def test_list_json_files(self):
        # Créer un fichier JSON fictif
        os.makedirs('_internal/static/jsons', exist_ok=True)
        test_json_file = '_internal/static/jsons/test.json'
        with open(test_json_file, 'w') as f:
            json.dump({"test": "data"}, f)

        response = self.client.get('/api/json-files')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test', response.data)

        # Nettoyer
        os.remove(test_json_file)

    @patch('application.subprocess.run')
    def test_submit_ia_audition (self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload= {
            "filePath": "path/to/file",
            "output_file": "path/to/output",
            "duration": "3",
            "sigma": "0.2",
            "betweenstimuli": "2",
            "afterfixation": "1",
            "bip" : "2",
            "launching_text": "path/to/launching_file",
            'random': "True",
        }

        response = self.client.post('/submit_ia_audition', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
             sys.executable, 'Python_scripts/IA_audition.py',
             "--file", "path/to/file",
             "--output_file", "path/to/output",
             "--duration", "3",
             "--sigma", "0.2",
             "--betweenstimuli", "2",
             "--afterfixation", "1",
             "--bip", "2",
             "--launching", "path/to/launching_file",
             '--random', "True"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_ia_audition_false(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            "filePath": "path/to/file",
            "output_file": "path/to/output",
            "duration": "3",
            "sigma": "0.2",
            "betweenstimuli": "2",
            "afterfixation": "1",
            "bipf": "2",
            "launching_text": "path/to/launching_file",
            'random': "True",
        }

        response = self.client.post('/submit_ia_audition', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/IA_audition.py',
                "--file", "path/to/file",
                "--output_file", "path/to/output",
                "--duration", "3",
                "--sigma", "0.2",
                "--betweenstimuli", "2",
                "--afterfixation", "1",
                "--bip", "2",
                "--launching", "path/to/launching_file",
                '--random', "True"
            ], check=True)

            try:
                mock_run.assert_called_once_with([
                    sys.executable, 'Python_scripts/IA_audition.py',
                    "--file", "path/to/file",
                    "--output_file", "path/to/output",
                    "--duration", "3",
                    "--sigma", "0.2",
                    "--betweenstimuli", "2",
                    "--afterfixation", "1",
                    "--bip", "2",
                    "--launching", "path/to/launching_file",
                    '--random', "True"
                ], check=True)
            except AssertionError as e:
                print("Test échoue correctement avec une erreur:", e)

                #check que ça renvoie une erreur lorsqu'il y a une erreur dans le nom d'un argument

    @patch('application.subprocess.run')
    def test_submit_ia_image(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            "filePath": "path/to/file",
            "output_file": "path/to/output",
            'duration': "0.1",
            "sigma": "0",
            "betweenstimuli": "12",
            "zoom": "80",
            "launching_text": "path/to/launching_file",
            "random": "False"
        }

        response = self.client.post('/submit_ia_image', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/IA_image.py',
            "--file", "path/to/file",
            "--output_file", "path/to/output",
            '--duration', "0.1",
            "--sigma", "0",
            "--betweenstimuli", "12",
            "--zoom", "80",
            "--launching", "path/to/launching_file",
            "--random", "False"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_ia_image_false(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            "filePath": "path/to/file",
            "output_file": "path/to/output",
            'duration': "0.12",
            "sigma": "0",
            "betweenstimuli": "12",
            "zoom": "80",
            "launching_text": "path/to/launching_file",
            "random": "False"
        }

        response = self.client.post('/submit_ia_image', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/IA_image.py',
                "--file", "path/to/file",
                "--output_file", "path/to/output",
                '--duration', "0.1",
                "--sigma", "0",
                "--betweenstimuli", "12",
                "--zoom", "80",
                "--launching", "path/to/launching_file",
                "--random", "False"
            ], check=True)

            try:
                mock_run.assert_called_once_with([
                    sys.executable, 'Python_scripts/IA_image.py',
                    "--file", "path/to/file",
                    "--output_file", "path/to/output",
                    '--duration', "0.1",
                    "--sigma", "0",
                    "--betweenstimuli", "12",
                    "--zoom", "80",
                    "--launching", "path/to/launching_file",
                    "--random", "False"
                ], check=True)
            except AssertionError as e:
                print("Test échoue correctement avec une erreur:", e)

    @patch('application.subprocess.run')
    def test_submit_text(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "8",
            'words': "",
            'filePath': "another_file",
            'launching_text': "path/to/launching_file",
            'port': "COM3",
            'fixation': "2",
            'activation': "True",
            'baudrate': "9600",
            'trigger': "q",
            'hauteur': "150",
            'random': "False",
            'largeur': "50",
            'output_file': "path/to/output",
            'zoom': "34"
        }

        response = self.client.post('/submit-text', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Text.py',
            '--duration', "8",
            '--words', "",
            '--file', "another_file",
            '--launching', "path/to/launching_file",
            '--port', "COM3",
            '--fixation', "2",
            '--activation', "True",
            '--baudrate', "9600",
            '--trigger', "q",
            '--hauteur', "150",
            '--random', "False",
            '--largeur', "50",
            '--output_file', "path/to/output",
            '--zoom', "34"
        ], check=True)

    @patch('application.subprocess.run')
    def test_submit_text_false(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "8",
            'words': "",
            'filePath': "another_file",
            'launching_text': "path/to/launching_file",
            'port': "COM3",
            'fixation': "2",
            'activation': "True",
            'baudrate': "9600",
            'trigger': "q",
            'hauteur': "150",
            'random': "False",
            'largeur': "50",
        }

        response = self.client.post('/submit-text', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):

            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_Text.py',
                '--duration', "8",
                '--words', "",
                '--file', "another_file",
                '--launching', "path/to/launching_file",
                '--port', "COM3",
                '--fixation', "2",
                '--activation', "True",
                '--baudrate', "9600",
                '--trigger', "q",
                '--hauteur', "150",
                '--random', "False",
                '--largeur', "50",
                '--output_file', "path/to/output",
                '--zoom', "34"
            ], check=True)
        try:
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_Text.py',
                '--duration', "8",
                '--words', "",
                '--file', "another_file",
                '--launching', "path/to/launching_file",
                '--port', "COM3",
                '--fixation', "2",
                '--activation', "True",
                '--baudrate', "9600",
                '--trigger', "q",
                '--hauteur', "150",
                '--random', "False",
                '--largeur', "50",
                '--output_file', "path/to/output",
                '--zoom', "34"
            ], check=True)
        except AssertionError as e:
            print("Une erreur a été trouvée comme prévu")
        #check de mettre moins d'arguement dans le payload que dans le mock_run



    @patch('application.subprocess.run')
    def test_submit_emo_voices(self, mock_run):
        mock_run.return_value = Mock(check = True)
        payload = {
            'duration': "0.001",
            'filePath': "my_input_file",
            'port': "",
            'activation': "False",
            'baudrate': "7854",
            'trigger': "s",
            'launching_text': "path/to/launching_file",
            'hauteur': "0",
            'largeur': "0",
            'random': "True",
            'betweenstimuli': "1",
            'output_file': "path/to/output"
        }

        response = self.client.post('/submit-emo-voice', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
             sys.executable, 'Python_scripts/Psychopy_EMO_VOICES.py',
             '--duration', "0.001",
             '--file', "my_input_file",
             '--port', "",
             '--activation', "False",
             '--baudrate', "7854",
             '--trigger', "s",
             '--launching', "path/to/launching_file",
             '--hauteur', "0",
             '--largeur', "0",
             '--random', "True",
             '--betweenstimuli', "1",
             '--output_file', "path/to/output"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_emo_voices_false(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "0.001",
            'filePath': "my_input_file",
            'port': "",
            'activation': "False",
            'baudrate': "7854",
            'trigger': "s",
            'launching_text': "path/to/launching_file",
            'hauteur': "0",
            'largeur': "0",
            'random': "True",
            'betweenstimuli': "1",
            'output_file': "path/to/output"
        }

        response = self.client.post('/submit-emo-voice', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_EMO_VOICES.py',
                '--duration', "0.001",
                '--file', "my_input_file",
                '--port', "",
                '--activation', "False",
                '--baudrate', "7854",
                '--trigger', "s",
                '--launching', "path/to/launching_file",
                '--hauteur', "0",
                '--largeur', "0",
                '--random', "True",
                '--betweenstimuli', "1",
                '--output_file', "path/to/output"
                "--zoom", "0"
            ], check=True)

        try :
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_EMO_VOICES.py',
                '--duration', "0.001",
                '--file', "my_input_file",
                '--port', "",
                '--activation', "False",
                '--baudrate', "7854",
                '--trigger', "s",
                '--launching', "path/to/launching_file",
                '--hauteur', "0",
                '--largeur', "0",
                '--random', "True",
                '--betweenstimuli', "1",
                '--output_file', "path/to/output"
                                 "--zoom", "0"
            ], check=True)

        except AssertionError as e:
            print("Une erreur a bien été trouvé")

    @patch('application.subprocess.run')
    def test_submit_cyberball(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            'premiere_phase': "50",
            'exclusion': "45",
            'transition': "120",
            'minimum': "30",
            'patient_name': "123",
            'launching_text': "path/to/launching_file",
            'maximum': "1.4",
            'trigger': "s",
            'output_file': "path/to/output",
            'filePath': "a_file"
        }

        response = self.client.post('/submit-cyberball', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Cyberball.py',
            '--premiere_phase', "50",
            '--exclusion', "45",
            '--transition', "120",
            '--minimum', "30",
            '--patient_name', "123",
            '--launching', "path/to/launching_file",
            '--maximum', "1.4",
            '--trigger', "s",
            '--output_file', "useless", #hardcodé dans l'application peut importe la valeur qu'on rentre de base pour cet argument
            '--filePath', "a_file"], check=True)

    @patch('application.subprocess.run')
    def test_submit_cyberball_false(self, mock_run):
        mock_run.return_value = Mock(check=True)
        payload = {
            'premiere_phase': "50",
            'exclusion': "45",
            'transition': "120",
            'minimum': "30",
            'patient_name': "123",
            'launching_text': "path/to/launching_file",
            'maximum': "1.4",
            'trigger': "s",
            'output_file': "path/to/output",
            'filePath': "a_file"
        }

        response = self.client.post('/submit-cyberball', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_Cyberball.py',
                '--premiere_phase', "50",
                '--exclusion', "45",
                '--transition', "120",
                '--minimum', "30",
                '--patient_name', "123",
                '--launching', "path/to/launching_file",
                '--maximum', "1.4",
                '--filePath', "a_file"], check=True)
            #check en mettant moins d'argument

            try:
                mock_run.assert_called_once_with([
                    sys.executable, 'Python_scripts/Psychopy_Cyberball.py',
                    '--premiere_phase', "50",
                    '--exclusion', "45",
                    '--transition', "120",
                    '--minimum', "30",
                    '--patient_name', "123",
                    '--launching', "path/to/launching_file",
                    '--maximum', "1.4",
                    '--filePath', "a_file"], check=True)
            except AssertionError:
                print ("Une erreur a bien été trouvée")

    @patch('application.subprocess.run')
    def test_submit_emo_face(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "0",
            'filePath': "az",
            'port': "Terminal",
            'activation': "False",
            'baudrate': "/",
            'trigger': "A",
            'hauteur': "234",
            'sigma': "0",
            'launching_text': "path/to/launching_file",
            'zoom': "0",
            'random': "anything", #étant donné que c'est un string qui est attendu on est pas obligé de mettre true or false
            'largeur': "190",
            'betweenstimuli': "1",
            'output_file': "an_output"
        }

        response = self.client.post('/submit-emo-faces', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_EMO_FACE.py',
            '--duration', "0",
            '--file', "az",
            '--port', "Terminal",
            '--activation', "False",
            '--baudrate', "/",
            '--trigger', "A",
            '--hauteur', "234",
            '--sigma', "0",
            '--launching', "path/to/launching_file",
            '--zoom', "0",
            '--random', "anything",
            '--largeur', "190",
            '--betweenstimuli', "1",
            '--output_file', "an_output",
        ],check = True)

    @patch('application.subprocess.run')
    def test_submit_emo_face_false(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "0",
            'filePath': "azerty",
            'port': "Terminal",
            'activation': "False",
            'baudrate': "/",
            'trigger': "A",
            'hauteur': "234",
            'sigma': "0",
            'launching_text': "path/to/launching_file",
            'zoom': "0",
            'random': "anything",
            # étant donné que c'est un string qui est attendu on est pas obligé de mettre true or false
            'largeur': "190",
            'betweenstimuli': "1",
            'output_file': "an_output"
        }

        response = self.client.post('/submit-emo-faces', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_EMO_FACE.py',
                '--duration', "0",
                '--file', "az",
                '--port', "Terminal",
                '--activation', "False",
                '--baudrate', "/",
                '--trigger', "A",
                '--hauteur', "234",
                '--sigma', "0",
                '--launching', "path/to/launching_file",
                '--zoom', "0",
                '--random', "anything",
                '--largeur', "190",
                '--betweenstimuli', "1",
                '--output_file', "an_output",
            ], check=True)

            try:
                mock_run.assert_called_once_with([
                    sys.executable, 'Python_scripts/Psychopy_EMO_FACE.py',
                    '--duration', "0",
                    '--file', "az",
                    '--port', "Terminal",
                    '--activation', "False",
                    '--baudrate', "/",
                    '--trigger', "A",
                    '--hauteur', "234",
                    '--sigma', "0",
                    '--launching', "path/to/launching_file",
                    '--zoom', "0",
                    '--random', "anything",
                    '--largeur', "190",
                    '--betweenstimuli', "1",
                    '--output_file', "an_output",
                ], check=True)
            except AssertionError:
                print("Une erreur a bien été trouvé car l'argument file n'a pas la même valeur ")

    @patch('application.subprocess.run')
    def test_submit_adjectifs(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "8",
            'filePath': "a_file.txt",
            'port': "COM1",
            'activation': "False",
            'random': "True",
            'baudrate': "745",
            'trigger': "2",
            'launching_text': "path/to/launching_file",
            'hauteur': "0",
            'largeur': "0",
            'blocks': "4",
            'zoom': "90",
            'entrainement': "path/to/entrainement_file",
            'per_block': "2",
            'betweenstimuli': "4",
            'output_file': "PatientID"
        }

        response = self.client.post('/submit-adjectifs', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Adjectifs.py',
            '--duration', "8",
            '--file', "a_file.txt",
            '--port', "COM1",
            '--activation', "False",
            '--random', "True",
            '--baudrate', "745",
            '--trigger', "2",
            '--launching', "path/to/launching_file",
            '--hauteur', "0",
            '--largeur', "0",
            '--blocks', "4",
            '--zoom', "90",
            '--entrainement', "path/to/entrainement_file",
            '--per_block', "2",
            '--betweenstimuli', "4",
            '--output_file', "PatientID"
            ], check = True)

    @patch('application.subprocess.run')
    def test_submit_stroop(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "8",
            'filePath': "a_file.txt",
            'port': "COM1",
            'activation': "True",
            'baudrate': "758",
            'trigger': "p",
            'launching_text': "path/to/launching_file",
            'hauteur': "450",
            'largeur': "200",
            'random': "True",
            'sigma': "0",
            'zoom': "70",
            'choice': "?",
            'betweenstimuli': "2",
            'output_file': "PatientID"
        }

        response = self.client.post('/submit-stroop', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Stroop.py',
            '--duration', "8",
            '--file', "a_file.txt",
            '--port', "COM1",
            '--activation', "True",
            '--baudrate', "758",
            '--trigger', "p",
            '--launching', "path/to/launching_file",
            '--hauteur', "450",
            '--largeur', "200",
            '--random', "True",
            '--sigma', "0",
            '--zoom', "70",
            '--choice', "?",
            '--betweenstimuli', "2",
            '--output_file', "PatientID"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_localizer(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': '120',
            'blocks': '10',
            'per_blocks': '5',
            'port': 'COM3',
            'activation': 'True',
            'baudrate': '9600',
            'trigger': 't',
            'hauteur': '200',
            'launching_text': 'path/to/launching_file',
            'zoom': '25',
            'fileName': 'data.txt',
            'largeur': '150',
            'random': 'True',
            'betweenstimuli': '10',
            'betweenblocks': '2',
            'output_file': 'Name'}

        response = self.client.post('/submit-localizer', json=payload)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_LOCALIZER.py',
            '--duration', '120',
            '--blocks', '10',
            '--per_block', '5',
            '--port', 'COM3',
            '--activation', 'True',
            '--baudrate', '9600',
            '--trigger', 't',
            '--hauteur', '200',
            '--launching', 'path/to/launching_file',
            '--zoom', '25',
            '--file', 'data.txt',
            '--largeur', '150',
            '--random', 'True',
            '--betweenstimuli', '10',
            '--betweenblocks', '2',
            '--output_file', 'Name'
            ], check= True)

    @patch('application.subprocess.run')
    def test_submit_priming(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "5",
            'blocks': "4",
            'port': "",
            'activation': "True",
            'fileName': "path/to/file",
            'baudrate': "",
            'trigger': "s",
            'hauteur': "",
            'launching_text': "path/to/launching",
            'zoom': "10",
            'largeur': "0",
            'random': "True",
            'betweenstimuli': "5",
            'betweenblocks': "2",
            'output_file': "output/path"}

        response = self.client.post('/submit-priming', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Priming.py',
            '--duration', "5",
            '--blocks', "4",
            '--port', "",
            '--activation', "True",
            '--file', "path/to/file",
            '--baudrate', "",
            '--trigger', "s",
            '--hauteur', "",
            '--launching', "path/to/launching",
            '--zoom', "10",
            '--largeur', "0",
            '--random', "True",
            '--betweenstimuli', "5",
            '--betweenblocks', "2",
            '--output_file', "output/path"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_videos(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'duration': "8",
            'filePath': "file",
            'output_file': "an_outputfile",
            'port': "COM3",
            'activation': "True",
            'baudrate': "863",
            'trigger': "g",
            'hauteur': "150",
            'launching_text': "path/to/launching",
            'random': "True",
            'sigma': "0.5",
            'largeur': "150",
            'betweenstimuli': "4",
            'zoom': "45"
        }

        response = self.client.post('/submit-videos', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Video.py',
            '--duration', "8",
            '--file', "file",
            '--output_file', "an_outputfile",
            '--port', "COM3",
            '--activation', "True",
            '--baudrate', "863",
            '--trigger', "g",
            '--hauteur', "150",
            '--launching', "path/to/launching",
            '--random', "True",
            '--sigma', "0.5",
            '--largeur', "150",
            '--betweenstimuli', "4",
            '--zoom', "45"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_audition(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'instruction':"path/to/slides",
            'duration': "2",
            'activation': "False",
            'trigger': "w",
            'hauteur':"42",
            'launching_text': "path/to/launching",
            'fileName': "path/to/file",
            'ASound': "A.wav",
            'largeur': "35",
            'random': "False",
            'sigma': "0",
            'betweenstimuli': "4",
            'output_file': "An_id"
        }
        response = self.client.post('/submit-audition', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_Audition.py',
            '--instruction', "path/to/slides",
            '--duration', "2",
            '--activation', "False",
            '--trigger', "w",
            '--hauteur', "42",
            '--launching', "path/to/launching",
            '--file', "path/to/file",
            '--asound', "A.wav",
            '--largeur', "35",
            '--random', "False",
            '--sigma', "0",
            '--betweenstimuli', "4",
            '--output_file', "An_id"
            ], check=True)

    @patch('application.subprocess.run')
    def test_submit_everything(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = {
            'data': "liste_of_stimuli",
            'instructions': "path/to/slides",
            'mot_fin': "path/to/file",
            'output_file': "an_Patient_ID"
        }

        response = self.client.post('/submit-table', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})
        data_arg = json.dumps("liste_of_stimuli")
        mock_run.assert_called_once_with([
            sys.executable, 'Python_scripts/Psychopy_everything.py',
            '--data', data_arg,
            '--instructions', "path/to/slides",
            '--mot_fin', "path/to/file",
            '--output_file', "an_Patient_ID"
            ], check = True)



    @patch('application.subprocess.run')
    def test_submit_images(self, mock_run):
            # Configurez mock_run pour simuler un appel réussi
            mock_run.return_value = Mock(check=True)
            payload = {
                'duration': '120',
                'filePath': 'path/to/file',
                'port': 'COM3',
                'launching_text': 'Starting',
                'activation': '1',
                'baudrate': '9600',
                'trigger': '5',
                'hauteur': '1920',
                'largeur': '1080',
                'random': '1',
                'sigma': '0.5',
                'output_file': 'output/path',
                'betweenstimuli': '2',
                'zoom': '1.5',
            }
            response = self.client.post('/submit-images', json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})

            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_Image.py',
                '--duration', '120',
                '--file', 'path/to/file',
                '--port', 'COM3',
                '--launching', 'Starting',
                '--activation', '1',
                '--baudrate', '9600',
                '--trigger', '5',
                '--hauteur', '1920',
                '--largeur', '1080',
                '--random', '1',
                '--sigma', '0.5',
                '--output_file', 'output/path',
                '--betweenstimuli', '2',
                '--zoom', '1.5',
            ], check=True)
            #check que les bons arguments sont envoyé au programme python



    @patch('application.subprocess.run')
    def test_submit_images_false(self, mock_run):
        # Configurez mock_run pour simuler un appel réussi
        mock_run.return_value = Mock(check=True)
        payload = ""
        response = self.client.post('/submit-images', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json, {'status': 'success', 'message': 'Données reçues et script exécuté'})
        #vérifie avec un string à la place d'un json que ça présente bien une erreur

        with self.assertRaises(AssertionError):
            mock_run.assert_called_once_with([
                sys.executable, 'Python_scripts/Psychopy_Image.py',
                '--duration', '120',
                '--file', 'path/to/file',
                '--port', 'COM3',
                '--launching', 'Starting',
                '--activation', '1',
                '--baudrate', '9600',
                '--trigger', '5',
                '--hauteur', '1920',
                '--largeur', '1080',
                '--random', '1',
                '--sigma', '0.5',
                '--output_file', 'output/path',
                '--betweenstimuli', '2',
                '--zoom', '1.5',
            ], check=True)

            try:
                mock_run.assert_called_once_with([
                    sys.executable, 'Python_scripts/Psychopy_Image.py',
                    '--duration', '120',
                    '--file', 'path/to/file',
                    '--port', 'COM3',
                    '--launching', 'Starting',
                    '--activation', '1',
                    '--baudrate', '9600',
                    '--trigger', '5',
                    '--hauteur', '1920',
                    '--largeur', '1080',
                    '--random', '1',
                    '--sigma', '0.5',
                    '--output_file', 'output/path',
                    '--betweenstimuli', '2',
                    '--zoom', '1.5',
                ], check=True)
            except AssertionError as e:
                print("Test échoue correctement avec une erreur:", e)

        # check que si des mauvais arguements sont envoyés au programme python ça ne fonctionne pas
    def test_keep_datas(self):
        payload = {
            "filename": "test_paradigm",
            "data": {"key": "value"},
            "instructions": "test instructions",
            "mot_fin": "fin"
        }
        response = self.client.post(
            '/keep-datas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(decoded_response["message"], "Données reçues et script exécuté")
        #vérification fonctionnement de keep_datas

        # Vérifier si le fichier JSON est créé
        file_path = "_internal/static/jsons/test_paradigm.json"
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
