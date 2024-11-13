import csv
import os
import random
import threading
from datetime import datetime

import argparse

import numpy as np
from psychopy import visual, core, event, sound
import sounddevice as sd
import pygame
import soundfile as sf
import writtingprt as wr
from Paradigme_parent import Parente

class Audition(Parente):
    def __init__(self, duration, output, filepath, betweenstimuli, random, trigger, launching, hauteur,
                 largeur, son, sigma):
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Input', 'Paradigme_Audition'))
        self.dossier_image = os.path.join(self.dossier, 'images')
        self.filepath = os.path.join(self.dossier, filepath)
        self.output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        self.dirname = self.filename[:self.filename.find(".tsv")]
        os.makedirs(self.dirname, exist_ok=True)
        self.record_index=0
        self.sound = son
        self.trigger = trigger
        self.global_timer = core.Clock()
        pygame.mixer.init()
        self.reaction = "None"
        self.fs = 48000
        self.threshold = 1000
        self.sigma = sigma
        self.launching = launching
        self.recorder = None
        self.win = visual.Window(
            size=(800, 600),
            fullscr=True,
            color=[-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
            units="norm",
        )
        self.win.winHandle.activate()
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        self.image_gauche = visual.ImageStim(self.win, pos=(-0.5, 0))
        self.image_droite = visual.ImageStim(self.win, pos=(0.5, 0))
        self.random = random == "True"
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)
        event.globalKeys.add(key='escape', func=self.win.close)

    def reading(self, filename):
        image1 = []
        image2 = []
        with open(filename, "r") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    image1.append(parts[0].strip())
                    image2.append(parts[1].strip())
        return image1, image2

    def record_audio(self):
        recording = sd.rec(int(self.stimuli_duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
        sd.wait()
        start_time = None
        for i, sample in enumerate(recording):
            if np.abs(sample) > self.threshold:
                start_time = i / self.fs
                break
        if start_time is not None:
            print(f"L'utilisateur a commencé à parler à {start_time:.2f} secondes.")
            self.reaction = start_time
        else:
            print("Aucune parole détectée.")
            self.reaction = "None"
        record = os.path.join(self.dirname, f"record{self.record_index}.wav")
        self.record_index += 1
        sf.write(record, recording, self.fs)

    def affichage(self, duration, gauche, droite):
        if droite == "ONEcouter" or gauche == "ONParler":
            stimulus = "A"
        else:
            stimulus = "Silence"
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        wait_time = random.gauss(self.betweenstimuli, self.sigma)
        core.wait(wait_time)
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), "Fixation", "Cross", "None", "None", "None"])
        self.image_droite.image = os.path.join(self.dossier_image, droite+'.PNG')
        self.image_gauche.image = os.path.join(self.dossier_image, gauche+'.PNG')
        self.image_gauche.draw()
        self.image_droite.draw()
        self.rect.draw()
        duration.text = "-"
        duration.height = 0.6
        duration.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        core.wait(2)
        duration.height = 0.2
        duration.text = str(int(self.stimuli_duration))
        self.image_gauche.draw()
        self.image_droite.draw()
        self.rect.draw()
        duration.draw()
        self.win.flip()
        compteur = int(self.stimuli_duration)
        actual_time = self.global_timer.getTime()
        while self.global_timer.getTime() < actual_time + self.stimuli_duration:
            # Calcule le temps restant
            time_remaining = actual_time + self.stimuli_duration - self.global_timer.getTime()
            # Attends seulement le temps restant, mais s'assure que ce soit plus précis
            core.wait(min(time_remaining, 1))  # Attente maximale de 1 seconde ou moins

            # Mise à jour du compteur et affichage
            compteur -= 1
            duration.text = str(compteur)
            self.image_gauche.draw()
            self.image_droite.draw()
            self.rect.draw()
            duration.draw()
            self.win.flip()
        if droite == "ONEcouter":
            sound_path = os.path.join(self.dossier, self.sound)
            audio = pygame.mixer.Sound(sound_path)
            audio.play()
        if gauche == "ONParler":
            audio_thread = threading.Thread(target=self.record_audio)
            audio_thread.start()
        if gauche == "OFFParler" and droite == "ONEcouter":
            cond = "AudC"
        elif gauche == "ONParler" and droite == "ONEcouter":
            cond = "PhAudc"
        else:
            cond = "CondRest"
        for x in range (8):
            image_path = os.path.join(self.dossier_image, 'barre'+str(x)+'.png')
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )

            image_stim.draw()
            self.win.flip()
            core.wait(self.stimuli_duration/7)
        image_path = os.path.join(self.dossier_image, 'barre'+str(8)+'.png')
        image_stim = visual.ImageStim(
            win=self.win,
            image=image_path,
            pos=(0, 0)
        )

        image_stim.draw()
        self.win.flip()
        if gauche == "ONParler":
            audio_thread.join()
        if self.reaction != "None":
            self.reaction = super().float_to_csv(self.reaction)
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), cond, stimulus, self.reaction, gauche, droite])
        self.reaction = "None"
        if droite == "ONEcouter":
            audio.stop()

    def lancement(self):
        print("ici le son")
        print(self.sound)
        super().file_init(self.filename, self.filename_csv, ['onset', 'Cond', 'stimulus', 'time_before_starting_to_answer', 'Image1', 'Image2'])
        gauche, droite = self.reading(self.filepath)
        if self.random:
            combined = list(zip(gauche, droite))
            random.shuffle(combined)
            gauche, droite = zip(*combined)
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts, self.trigger, "center")
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        for gauche, droite in zip(gauche, droite):
            texte_centre = visual.TextStim(self.win, text=str(self.stimuli_duration), pos=(0, 0), color=(-1, -1, -1))
            self.affichage(texte_centre, gauche, droite)
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None", "None"])
        super().the_end3(self.win)
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "Cond")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--instruction", type=float, required=True, help="Durée en secondes de l'instruction")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--file", type=str, required=True, help="Nom du fichier d'input")
    parser.add_argument("--asound", type=str, required=True, help="Son du patient")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--sigma", type=float, required=True, help="écart type pour le random")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")


    args = parser.parse_args()
    audition = Audition(args.duration, args.output_file, args.file, args.betweenstimuli,
                        args.random, args.trigger, args.launching, args.hauteur,
                        args.largeur, args.asound, args.sigma).lancement()
