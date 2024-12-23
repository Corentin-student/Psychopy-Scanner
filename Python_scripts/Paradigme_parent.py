import csv
import os
import re
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime
from psychopy import event, visual, core
import writtingprt as  wr
import serial


class Parente(ABC):
    def preprocessing_tsv_csv(self, filename):
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..', 'Fichiers_output'))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        current_date = datetime.now().strftime("%Y-%m-%d")
        run_number = 1
        filename_prefix = f"{current_date}_{filename.split('.')[0]}"
        existing_files = [f for f in os.listdir(output_dir) if f.startswith(filename_prefix) and 'run' in f]
        if existing_files:
            runs = [int(f.split('run')[-1].split('.')[0]) for f in existing_files if 'run' in f]
            if runs:
                run_number = max(runs) + 1
        filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.tsv")
        filename_csv = os.path.join(output_dir, f"{filename_prefix}_csv_run{run_number}.csv")
        return filename, filename_csv

    def preprocessing_tsv(self, filename):
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..' 'Fichiers_output'))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        current_date = datetime.now().strftime("%Y-%m-%d")
        run_number = 1
        filename_prefix = f"{current_date}_{filename.split('.')[0]}"
        existing_files = [f for f in os.listdir(output_dir) if f.startswith(filename_prefix) and 'run' in f]
        if existing_files:
            runs = [int(f.split('run')[-1].split('.')[0]) for f in existing_files if 'run' in f]
            if runs:
                run_number = max(runs) + 1
        filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.tsv")
        return filename

    def inputs_texts(self,chemin):
        with open(chemin, 'r', encoding='utf-8') as file:
            contenu = file.read()
        texts = re.findall(r'\*(.*?)\*', contenu, re.DOTALL)
        return texts

    def wait_for_trigger(self, trigger='s'):
        event.waitKeys(keyList=[trigger])

    def proper_waitkey(self, trigger='s'):
        donottake = trigger
        while True:
            keys = event.waitKeys()
            if donottake not in keys:  # Condition pour quitter la boucle
                break

    def launching_texts(self,win,textes,trigger, align="left"):
        y=0
        for x in range (len(textes)-1):
            self.Premier_texte = textes[x]
            texte = visual.TextStim(win, text=self.Premier_texte, color=[1, 1, 1], alignText=align, wrapWidth=1.5,
                                    font='Arial')
            texte.draw()
            win.flip()
            self.proper_waitkey(trigger)
            y=x+1
        text_after= visual.TextStim(win, text=textes[y], alignText="center", wrapWidth=1.5, font="Arial")
        text_after.draw()
        win.flip()

    def the_end (self, win):
        texte = visual.TextStim(win, text="End/Fin/Ende", color=[1, 1, 1], alignText="center", wrapWidth=1.5, font='Arial')
        texte.draw()
        win.flip()
        core.wait(5)

    def the_end2 (self, win):
        texte = visual.TextStim(win, text="Merci beaucoup d'avoir réalisé cette tâche. \n \n Ne bougez pas, on vous parle dans quelques secondes. ",
                                color=[1, 1, 1], alignText="center", wrapWidth=1.5, font='Arial')
        texte.draw()
        win.flip()
        core.wait(4)

    def the_end3 (self, win):
        line = visual.ShapeStim(
            win,
            vertices=[(0, 1), (0, -1)],
            lineWidth=5,
            lineColor='white',
            closeShape=False
        )

        text_fr = visual.TextStim(win, pos=(0.5, 0), text="Merci beaucoup d'avoir réalisé \n cette tâche. \n \n Ne bougez pas, \n on vous parle dans quelques \n secondes. ",
                                color=[1, 1, 1], alignText="center", wrapWidth=1.5, font='Arial')
        text_nl = visual.TextStim(win, pos=(-0.5, 0), text="Hartelijk dank voor het voltooien \n  van deze taak. \n \n Beweeg je niet, \n we spreken je over een paar \n seconden.",
                                  color=[1, 1, 1], alignText="center", wrapWidth=1.5, font='Arial')
        line.draw()
        text_fr.draw()
        text_nl.draw()
        win.flip()
        core.wait(4)
    def send_character(self, port, baud_rate):
        char = "t"
        try:
            print(port)
            with serial.Serial(port=port, baudrate=baud_rate, timeout=1) as ser:
                print(f"Connexion ouverte sur {port}. Envoi de '{char}'...")
                #ser.write(char.encode())
                ser.write(b'H')
                time.sleep(0.5)
                ser.write(b'L')
                print("Pin 2 activé puis désactivé")


        except serial.SerialException as e:
            print(f"Erreur d'ouverture ou d'utilisation du port série : {e}")

    def file_init(self, filename, filename_csv, columns):
        with open(filename, mode='w', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter=';')
            csv_writer.writerow(columns)

        with open(filename_csv, mode='w', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter=';')
            csv_writer.writerow(columns)

    def write_tsv_csv(self, filename, filename_csv, rows):
        with open(filename, mode='a', newline='', encoding='utf-8') as file1:
            csv_writer = csv.writer(file1, delimiter=';')
            csv_writer.writerow(rows)

        with open(filename_csv, mode='a', newline='', encoding='utf-8') as file1:
            csv_writer = csv.writer(file1, delimiter=';')
            csv_writer.writerow(rows)
    def float_to_csv(self, value):
        return str(value).replace('.', ',')

    def adding_duration (self, input, input2):
        self.adding_duration1(input)
        self.adding_duration1(input2)
    def adding_duration1(self,input_file):
        with open(input_file, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            rows = list(reader)

        for row in rows:
            row['onset'] = float(row['onset'].replace(',', '.')) * 1000  # Transformer en millisecondes
            row['onset'] = round(row['onset'])  # Arrondir les onsets

        durations = []
        for i in range(len(rows) - 1):
            onset_current = rows[i]['onset']
            onset_next = rows[i + 1]['onset']
            duration = onset_next - onset_current
            durations.append(duration)
        durations.append(None)
        for i, row in enumerate(rows):
            row['duration'] = durations[i]
        rows.pop()

        with open(input_file, mode='w', newline='') as csvfile:
            fieldnames = reader.fieldnames + ['duration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
    def writting_prt(self, filename, col="trial_type"):
        instance = wr.writtingprt()
        basics = {}
        basics["filename"] = filename
        basics["result"] = instance.analyze_trial_types(filename, col)
        basics["result"] = instance.adjust_onsets_to_start_at_zero(basics["result"])
        file = filename.split(".csv")[0]+".prt"
        instance.create_experiment_file(file, basics)