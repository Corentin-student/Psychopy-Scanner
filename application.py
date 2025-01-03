"Version 1.0"
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import sys
import json
import webbrowser
from waitress import serve

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Aucun fichier sélectionné.', 400
    file = request.files['file']
    if file.filename == '':
        return 'Aucun fichier sélectionné.', 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)  # Sauvegarder le fichier dans le dossier spécifié
        return f'Fichier {file.filename} téléchargé avec succès à {file_path}.', 200
@app.route('/index')
def index():
    return render_template('index2.html')
@app.route('/created_paradigmes')
def created_paradigmes():
    return render_template('existing.html')

@app.route('/api/json-files')
def list_json_files():
    current_directory = os.getcwd()  # Récupère le dossier actuel
    print(f"Dossier actuel : {current_directory}")

    # Afficher les fichiers et dossiers dans le répertoire courant
    print("Contenu actuel du répertoire (équivalent à ls) :")
    for item in os.listdir(current_directory):
        print(f"- {item}")


    path = '_internal/static/jsons'  # Chemin vers le dossier des fichiers JSON
    files = [file.replace('.json', '') for file in os.listdir(path) if file.endswith('.json')]
    return jsonify(files)

@app.route('/about')
def about():
    print("")
    return render_template('about.html')

@app.route('/fr/about')
def about_fr():
    return render_template('about.html')  # Template en français

@app.route('/nl/about')
def about_nl():
    return render_template('about-nl.html')  # Template en néerlandais


@app.route('/get-json-file', methods=['GET'])
def serve_json_file():
    file_name = request.args.get('param_to_file')
    directory_path = '_internal/static/jsons'  # Assurez-vous que ce chemin est correct
    file_path = f"{directory_path}/{file_name}.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500
@app.route('/')
def home():
    return render_template('about.html')

@app.route('/submit_ia_audition', methods=['POST'])
def submit_ia_audition():
    try:
        print("oui?")
        data = request.get_json()
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/IA_audition.py',
            #'Python_scripts\\IA_audition.exe',
            "--file", data.get("filePath"),
            "--output_file", data.get("output_file"),
            "--duration", data.get("duration"),
            "--sigma", data.get("sigma"),
            "--betweenstimuli", data.get("betweenstimuli"),
            "--afterfixation", data.get("afterfixation"),
            "--bip", data.get("bip"),
            "--launching", data.get("launching_text"),
            '--random', str(data.get("random")),
        ], check=True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit_ia_image', methods=['POST'])
def submit_ia_image():
    try:
        data = request.get_json()
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/IA_image.py',
            #'Python_scripts\\IA_image.exe',
            "--file", data.get("filePath"),
            "--output_file", data.get("output_file"),
            '--duration', data.get("duration"),
            "--sigma", data.get("sigma"),
            "--betweenstimuli", data.get("betweenstimuli"),
            "--zoom", data.get("zoom"),
            "--launching", data.get("launching_text"),
            "--random", str(data.get("random"))
        ], check=True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-text', methods=['POST'])
def submit_text():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        words = data.get('words')
        zoom = data.get('zoom')
        file = data.get('filePath')
        launching = data.get('launching_text')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        random = data.get('random')
        fixation = data.get('fixation')
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Text.py',
            #'Python_scripts\\Psychopy_Text.exe',
            '--duration', duration,
            '--words', words,
            '--file', file,
            '--launching', launching,
            '--port', port,
            '--fixation', fixation,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--random', str(random),
            '--largeur', largeur,
            '--output_file', output_file,
            '--zoom', zoom
        ], check = True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-emo-voice', methods=['POST'])
def submit_emo_voice():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        launching = data.get('launching_text')
        baudrate = data.get('baudrate')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        trigger = data.get('trigger')
        random = data.get('random')
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_EMO_VOICES.py',
            #'Python_scripts\\Psychopy_EMO_VOICES.exe',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--launching', launching,
            '--hauteur', hauteur,
            '--largeur', largeur,
            '--random', str(random),
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ], check=True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-cyberball', methods=['POST'])
def submit_cyberball():
    try:
        """try:
                subprocess.run([
                    'powershell', '-Command', 'Start-Process',
                    'Python_scripts\\Psychopy_Cyberball.py',
                    '-ArgumentList',
                    f'"--premiere_phase", "{premiere_phase}", "--exclusion",'
                    f' "{exclusion}", "--transition", "{transition}", "--minimum", "{minimum}",'
                    f' "--patient_name", "{patient_name}", "--launching", "{launching}",'
                    f' "--maximum", "{maximum}", "--trigger", "{trigger}",'
                    f' "--output_file", "{output_file}", "--filePath", "{filePath}"',
                    '-Verb', 'RunAs'
                ])
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.stderr.decode('utf-8')}")
    
            return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})"""
        data = request.get_json()
        premiere_phase = data.get("premiere_phase")
        exclusion = data.get("exclusion")
        transition = data.get("transition")
        minimum = data.get("minimum")
        maximum = data.get("maximum")
        trigger = data.get("trigger")
        launching = data.get("launching_text")
        patient_name = data.get("patient_name")
        output_file = "useless"
        filePath = data.get("filePath")
        print("ça passe")
        print(data)

        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Cyberball.py',
            '--premiere_phase', premiere_phase,
            '--exclusion', exclusion,
            '--transition', transition,
            '--minimum', minimum,
            '--patient_name', patient_name,
            '--launching', launching,
            '--maximum', maximum,
            '--trigger', trigger,
            '--output_file', output_file,
            '--filePath', filePath,
        ], check=True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
        """
        try:
            subprocess.run([
                'powershell', '-Command', 'Start-Process',
                'Python_scripts\\Psychopy_Cyberball.exe',
                '-ArgumentList',
                f'"--premiere_phase", "{premiere_phase}", "--exclusion",'
                f' "{exclusion}", "--transition", "{transition}", "--minimum", "{minimum}",'
                f' "--patient_name", "{patient_name}", "--launching", "{launching}",'
                f' "--maximum", "{maximum}", "--trigger", "{trigger}",'
                f' "--output_file", "{output_file}", "--filePath", "{filePath}"',
                '-Verb', 'RunAs'
            ])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode('utf-8')}")
        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
        """
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})






@app.route('/submit-emo-faces', methods=['POST'])
def submit_emo_faces():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        hauteur = data.get('hauteur')
        zoom = data.get('zoom')
        launching = data.get('launching_text')
        largeur = data.get('largeur')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        random = data.get('random')
        sigma = data.get('sigma')
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_EMO_FACE.py',
            #'Python_scripts\\Psychopy_EMO_FACE.exe',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--sigma', sigma,
            '--launching', launching,
            '--zoom', zoom,
            '--random', str(random),
            '--largeur', largeur,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ], check = True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-adjectifs', methods=['POST'])
def submit_adjectifs():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        activation = data.get('activation')
        random = data.get('random')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        blocks = data.get('blocks')
        zoom = data.get('zoom')
        entrainement = data.get('entrainement')
        per_block = data.get('per_block')
        print("working here?")
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Adjectifs.py',
            #'Python_scripts\\Psychopy_Adjectifs.exe',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--activation', str(activation),
            '--random', str(random),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--launching', launching,
            '--hauteur', hauteur,
            '--largeur', largeur,
            '--blocks', blocks,
            '--zoom', zoom,
            '--entrainement', entrainement,
            '--per_block', per_block,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ], check = True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-stroop', methods=['POST'])
def submit_stroop():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        zoom = data.get('zoom')
        choice = data.get('choice')
        activation = data.get('activation')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        random = data.get('random')
        sigma = data.get('sigma')
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Stroop.py',
            #'Python_scripts\\Psychopy_Stroop.exe',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--launching', launching,
            '--hauteur', hauteur,
            '--largeur', largeur,
            '--random', str(random),
            '--sigma', sigma,
            '--zoom', zoom,
            '--choice', choice,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ], check = True)
        print("working here?")

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-localizer', methods=['POST'])
def submit_localizer():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        blocks = data.get('blocks')
        per_block = data.get('per_blocks')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        zoom = data.get('zoom')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        betweenblocks = data.get('betweenblocks')
        random = data.get('random')
        file = data.get('fileName')

        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_LOCALIZER.py',
            #'Python_scripts\\Psychopy_LOCALIZER.exe',
            '--duration', duration,
            '--blocks', blocks,
            '--per_block', per_block,
            '--port', port,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--launching', launching,
            '--zoom', zoom,
            '--file', file,
            '--largeur', largeur,
            '--random', str(random),
            '--betweenstimuli', betweenstimuli,
            '--betweenblocks', betweenblocks,
            '--output_file', output_file,
        ], check = True)
        print("working here?")

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-priming', methods=['POST'])
def submit_priming():
    try:
        print("working heere?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        blocks = data.get('blocks')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        zoom = data.get('zoom')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        betweenblocks = data.get('betweenblocks')
        random = data.get('random')
        file = data.get('fileName')
        print('in priming')
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Priming.py',
            #'Python_scripts\\Psychopy_Priming.exe',
            '--duration', duration,
            '--blocks', blocks,
            '--port', port,
            '--activation', str(activation),
            '--file', file,
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--launching', launching,
            '--zoom', zoom,
            '--largeur', largeur,
            '--random', str(random),
            '--betweenstimuli', betweenstimuli,
            '--betweenblocks', betweenblocks,
            '--output_file', output_file,
        ], check = True)
        print("working here?")

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-images', methods=['POST'])
def submit_images():
    try:
        print("ooo?")
        print("'oo")
        data = request.get_json()
        print(data)
        duration = data.get('duration')
        file = data.get('filePath')
        zoom = data.get('zoom')
        print("oop")
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        random = data.get('random')
        sigma = data.get('sigma')
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Image.py',
            #'Python_scripts\\Psychopy_Image.exe',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--launching', launching,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--largeur', largeur,
            '--random', str(random),
            '--sigma', sigma,
            '--output_file', output_file,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ], check = True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-videos', methods=['POST'])
def submit_videos():
    try:
        print("wtf ????")
        data = request.get_json()
        print(data)
        duration = data.get('duration')
        file = data.get('filePath')
        zoom = data.get('zoom')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        random = data.get('random')
        sigma = data.get('sigma')
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Video.py',
            #'Python_scripts\\Psychopy_Video.exe',
            '--duration', duration,
            '--file', file,
            '--output_file', output_file,
            '--port', port,
            '--activation', str(activation),
            '--baudrate', str(baudrate),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--launching', launching,
            '--random', str(random),
            '--sigma', sigma,
            '--largeur', largeur,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ], check = True)

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-audition', methods=['POST'])
def submit_audition():
    try:
        print("working hddere?")
        data = request.get_json()
        print(data)
        instruction = data.get('instruction')
        duration = data.get('duration')
        print("ok")
        betweenstimuli = data.get('betweenstimuli')
        print("non")
        output_file = data.get('output_file')
        activation = data.get('activation')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        hauteur = data.get('hauteur')
        largeur = data.get('largeur')
        launching = data.get('launching_text')
        random = data.get('random')
        file = data.get('fileName')
        asound = data.get('ASound')
        sigma = data.get('sigma')

        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Audition.py',
            #'Python_scripts\\Psychopy_Audition.exe',
            '--instruction', instruction,
            '--duration', duration,
            '--activation', str(activation),
            '--trigger', trigger,
            '--hauteur', hauteur,
            '--launching', launching,
            '--file', file,
            '--asound', asound,
            '--largeur', largeur,
            '--random', str(random),
            '--sigma', sigma,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ], check = True)
        print("working here?")

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-table', methods=['POST'])
def submit_table():
    print("ici ?")
    data = request.get_json()
    print(data)
    json_data = json.dumps(data)
    print(json_data)
    stimuli = json.dumps(data.get("data"))
    current_directory = os.getcwd()  # Récupère le dossier actuel
    print(f"Dossier actuel : {current_directory}")

    # Afficher les fichiers et dossiers dans le répertoire courant
    print("Contenu actuel du répertoire (équivalent à ls) :")
    for item in os.listdir(current_directory):
        print(f"- {item}")
    print("fonctionne?")
    subprocess.run([
        sys.executable, 'Python_scripts/Psychopy_everything.py',
        #'Python_scripts\\Psychopy_everything.exe',
        '--data', stimuli,
        '--instructions', data.get("instructions"),
        '--mot_fin', data.get("mot_fin"),
        '--output_file', data.get("output_file")
    ], check= True)
    return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})

@app.route('/keep-datas', methods=['POST'])
def keep_datas():
    data = request.get_json()
    filename = "_internal/static/jsons/"+data.get("filename")+".json"
    datas = data.get("data")
    print(data)
    print("pas ici")
    print(datas)
    print(filename)
    output_data = {
        "data": datas,
        "instructions": data.get("instructions", ""),  # Valeur par défaut si non présente
        "mot_fin": data.get("mot_fin", "")  # Valeur par défaut si non présente
    }
    print(output_data)
    with open(filename, "w") as json_file:
        json.dump(output_data, json_file, indent=4)

    return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    #app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)
