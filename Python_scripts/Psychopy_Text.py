import argparse
import os
import random
from datetime import datetime

import serial
from psychopy import visual, core, event
import csv
from Paradigme_parent import Parente


class PsychoPyParadigm(Parente):
    def __init__(self, duration, words, zoom, file, output, port, baudrate, trigger, activation,
                 hauteur, largeur, random, fixation, launching):
        self.duration = int(duration)
        self.words = words
        self.zoom = zoom
        self.file = file
        self.stimuli_times = []
        self.stimuli_apparition = []
        self.stimuli = []
        self.global_timer= core.Clock()
        self.launching = launching
        self.output=output
        self.port = port
        self.fixation = fixation
        self.baudrate = baudrate
        self.trigger = trigger
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Input', 'Paradigme_mots'))
        self.win = visual.Window(size=(800, 600), fullscr=True, color=[-1, -1, -1], units="norm")
        self.win.winHandle.activate()
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False

        self.rect_width = largeur
        self.rect_height = hauteur


    def affichage_mots(self, win, text_stim, words, display_time):
        for word in words:
            text_stim.setText(word)
            text_stim.draw()
            self.rect.draw()
            win.flip()
            onset = self.global_timer.getTime()
            if self.activation and words != [":; $+", " #^=-", ":?$µ", "###"]:
                super().send_character(self.port,self.baudrate)
            while self.global_timer.getTime() < onset + display_time:
                pass
            stimuli = word
            trial_type = "Stimuli"
            super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), stimuli, trial_type])

    def reading(self, filename):
        filename = os.path.join(self.dossier, filename)
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste


    def words_psychopy(self):
        self.rect = visual.Rect(self.win, width=self.rect_width, height=self.rect_height, fillColor='white',
                                lineColor='white')
        self.rect.pos = (self.win.size[0] / 2 - self.rect_width / 2, self.win.size[1] / 2 - self.rect_height / 2)
        event.globalKeys.add(key='escape', func=self.win.close)
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts,self.trigger)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        text_stim = visual.TextStim(self.win, text='', color=[1, 1, 1],
                                    font='Arial', height = 0.1 + (0.004*self.zoom))
        nothinkinglist = [":; $+", " #^=-", ":?$µ", "###"]
        if self.random:
            random.shuffle(self.words)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + self.fixation:
            pass
        stimuli = "None"
        trial_type = "Fixation"
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), stimuli, trial_type])
        self.affichage_mots(self.win, text_stim, nothinkinglist, self.duration)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + self.fixation:
            pass
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), stimuli, trial_type])
        self.affichage_mots(self.win, text_stim, self.words, self.duration)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + self.fixation:
            pass
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), stimuli, trial_type])
        self.affichage_mots(self.win, text_stim, nothinkinglist, self.duration)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + self.fixation:
            pass
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), stimuli, trial_type])
        super().the_end(self.win)
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None"])
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")
        self.win.close()

    def pas_un_stimuli(self, stimuli):
        alphabet = ";:/.,?#@&|£$[]=~"
        for char in alphabet:
            if char in stimuli:
                return True
        return False

    def run(self):
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'stimuli', 'trial_type'])
        if self.file:
            self.words = self.reading(self.file)
        else:
            self.words = [word.strip() for word in self.words.split(',')]
        self.words_psychopy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--fixation", type=float, required=True, help="Durée entre les blocks")
    parser.add_argument("--words", type=str, required=True, help="Liste de mots pour le paradigme")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    paradigm = PsychoPyParadigm(args.duration, args.words, args.zoom, args.file,args.output_file,args.port,
                                args.baudrate, args.trigger, args.activation,
                                args.hauteur, args.largeur, args.random, args.fixation, args.launching)
    paradigm.run()
