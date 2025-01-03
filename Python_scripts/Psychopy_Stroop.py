import os
import random

import argparse
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from psychopy import visual, core, event
from Paradigme_parent import Parente


class Colors(Parente):
    def __init__(self, duration, betweenstimuli, zoom, langage, filepath, output, port, baudrate, trigger, activation,
                 hauteur, largeur, random, launching, sigma):
        self.win = visual.Window(size=(800, 600), fullscr=True, color="black", units="norm")
        self.win.winHandle.activate()
        event.globalKeys.add(key='escape', func=self.win.close)
        self.fs = 44100  # fréquence d'échantillonnage
        self.stimuli_duration = duration  # durée de l'enregistrement en secondes
        self.betweenstimuli = betweenstimuli
        self.zoom = zoom
        self.sigma = sigma
        self.filepath = filepath
        self.output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        self.dirname = self.filename[:self.filename.find(".tsv")]
        os.makedirs(self.dirname, exist_ok=True)
        self.threshold = 1000  # seuil pour détecter le début de la parole (à ajuster selon votre micro/environnement)
        self.global_timer = core.Clock()
        self.patient_id = output
        self.launching = launching
        self.langue = langage
        self.port = port
        self.record_index = 0
        self.baudrate = baudrate
        self.trigger = trigger
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Input', 'Paradigme_Couleur'))
        self.dossier_colors = os.path.join(self.dossier, 'colors')

        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random =="True":
            self.random = True
        else:
            self.random = False
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)


        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )


    def reading(self,filename):
        words = []
        colors = []
        stimuli = []
        with open(filename, "r", encoding="utf-8") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    words.append(parts[0].strip())
                    colors.append(parts[1].strip())
        for x in range(len(words)):
            mot = words[x]+"_"+colors[x]
            stimuli.append(mot)
        return words, colors, stimuli

    def reconnaissance(self,chemin):
        recognizer = sr.Recognizer()

        audio_file = chemin

        # Utilisation de SpeechRecognition pour convertir l'audio en texte
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                if self.langue == "Francais":
                    text = recognizer.recognize_google(audio_data, language="fr-FR")
                elif self.langue == "Anglais":
                    text = recognizer.recognize_google(audio_data, language="en-US")
                elif self.langue == "Dannois":
                    text = recognizer.recognize_google(audio_data, language="da-DK")
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition n'a pas pu comprendre l'audio")
                return "None/pas reconnu"
            except sr.RequestError as e:
                print(f"Erreur lors de la demande à Google Speech Recognition; {e}")
                return "None/pas reconnu"

    def lancement(self):
        super().file_init(self.filename,self.filename_csv, ['onset', 'stimuli', 'trial_type', 'response','time_before_starting_to_answer'] )
        texts= super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts,self.trigger)
        words, colors, stimuli_names=self.reading(os.path.join(self.dossier, self.filepath))
        if self.random:
            combined = list(zip(words, colors, stimuli_names))
            random.shuffle(combined)
            words_shuffled, colors_shuffled, stimuli_names_shuffled = zip(*combined)
            words = list(words_shuffled)
            colors= list(colors_shuffled)
            stimuli_names = list(stimuli_names_shuffled)
        text_stim = visual.TextStim(self.win, wrapWidth=1.5, font="Arial", height=0.1 + (0.005*self.zoom))
        count=0
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        for mot in words:
            self.cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            random_gauss = random.gauss(self.betweenstimuli, self.sigma)
            while self.global_timer.getTime() < onset + random_gauss:
                pass
            stimuli = "Cross"
            reaction = "None"
            trial = "Fixation"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), stimuli, trial, reaction, reaction])
            text_stim.text=mot
            text_stim.color=colors[count]
            text_stim.draw()
            self.rect.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            recording = sd.rec(int(self.stimuli_duration *self.fs), samplerate=self.fs, channels=1, dtype='int16')
            if self.activation:
                super().send_character(self.port,self.baudrate)
            sd.wait()
            stimuli = stimuli_names[count]
            trial = "Stimuli"
            start_time = None
            for i, sample in enumerate(recording):
                if np.abs(sample) > self.threshold:
                    start_time = i / self.fs
                    break
            if start_time is not None:
                print(f"L'utilisateur a commencé à parler à {start_time:.2f} secondes.")
            else:
                start_time="None"
                print("Aucune parole détectée.")
            reaction = start_time
            record = os.path.join(self.dirname, f"record{self.record_index}.wav")
            self.record_index += 1
            sf.write(record, recording, self.fs)
            if reaction != "None":
                super().float_to_csv(reaction)
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), stimuli, trial, self.reconnaissance(record), reaction])
            count+=1

        super().the_end(self.win)
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None",
                               "None"])
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")
        self.win.close()
        core.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--choice", type=str, required=True, help="Choix de la langue")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--sigma", type=float, required=True, help="ecart type pour le random")



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    colors = Colors(args.duration, args.betweenstimuli, args.zoom, args.choice, args.file, args.output_file,
                    args.port, args.baudrate, args.trigger, args.activation,
                        args.hauteur, args.largeur, args.random, args.launching, args.sigma).lancement()

