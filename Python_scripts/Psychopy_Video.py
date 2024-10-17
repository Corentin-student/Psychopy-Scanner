import argparse
import copy
import csv
import os
import random
import time
from datetime import datetime

from psychopy import visual, core, event, logging
import serial
from Paradigme_parent import Parente
import gc  # Garbage Collector
import sys




class VideoPsycho(Parente):
    def __init__(self, duration, betweenstimuli, file, zoom, output, port, baudrate, trigger, activation,
                 hauteur, largeur, random, launching, sigma):
        self.duration = duration
        self.betweenstimuli = betweenstimuli
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)

        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..', 'Input', 'Paradigme_video'))
        self.dossier_files = os.path.join(self.dossier,'newstimuli')
        self.file = os.path.join(self.dossier,file)

        self.zoom = zoom
        self.output = output
        self.port = port
        self.launching = launching
        self.baudrate = baudrate
        self.trigger = trigger
        self.sigma = sigma
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False
        self.win = visual.Window(
            size=(800,600),
            fullscr=True,
            color=[-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
            units="norm",
        )
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)


    def reading(self, filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def play_video_psychopy(self, chemin, duration, between_stimuli, zoom, trigger):
        self.win.winHandle.activate()
        apparition_stimuli = []
        longueur_stimuli = []
        stimuli_liste = []
        super().file_init(self.filename, self.filename_csv,['onset', 'duration', 'trial_type', 'stim_file'])
        videos = self.reading(chemin)
        if self.random:
            random.shuffle(videos)
        file = copy.copy(videos)
        videos = [os.path.join(self.dossier_files, v) for v in videos]

        # Ajouter la gestion de l'échappement pour fermer proprement la fenêtre
        event.globalKeys.add(key='escape', func=self.win.close)

        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )

        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)

        global_timer = core.Clock()
        timer = core.Clock()
        thezoom = 0.7 + (0.012 * self.zoom)

        for x, video_path in enumerate(videos):
            try:
                print(x)
                print(video_path)
                cross_stim.draw()
                self.win.flip()
                timer.reset()
                apparition = global_timer.getTime()
                random_gaussian = random.gauss(self.betweenstimuli, self.sigma)
                while timer.getTime() < random_gaussian:
                    pass
                longueur = timer.getTime()
                stimuli = "Fixation"
                super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(apparition), super().float_to_csv(longueur), stimuli, "None"])
                movie_stim = visual.MovieStim(
                    win=self.win,
                    filename=video_path,
                    pos=(0, 0),
                    size=thezoom,
                    opacity=1.0,
                    flipVert=False,
                    flipHoriz=False,
                    loop=False,
                    units='norm',
                )

                timer.reset()

                apparition = global_timer.getTime()
                if self.activation:
                    super().send_character(self.port, self.baudrate)
                movie_stim.play()

                while timer.getTime() < duration:
                    self.rect.draw()
                    movie_stim.draw()
                    self.win.flip()
                longueur = timer.getTime()
                stimuli = file[x]
                super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(apparition), super().float_to_csv(longueur), "Stimuli", stimuli])


                if movie_stim is not None:
                    movie_stim.stop()
                    movie_stim.setAutoDraw(False)
                    movie_stim.seek(0)
                    del movie_stim
                    self.win.flip(clearBuffer=True)
                    core.wait(0.1)
                    gc.collect()

            except Exception as e:
                print("#############################################")
                print(f"Erreur rencontrée : {e}")
                print("#############################################")
                pass


        apparition = global_timer.getTime()
        cross_stim.draw()
        self.win.flip()
        timer.reset()
        while timer.getTime() < between_stimuli:
            pass
        longueur = timer.getTime()
        stimuli = "Fixation"
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(apparition), super().float_to_csv(longueur), stimuli, "None"])

        super().the_end(self.win)
        super().writting_prt(self.filename_csv, "trial_type")
        self.win.close()

        return longueur_stimuli, apparition_stimuli, stimuli_liste


    def lancement(self):
        self.play_video_psychopy(self.file, self.duration, self.betweenstimuli, self.zoom, self.trigger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--sigma", type=float, required=True, help="ecart type pour le random")



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")


    args = parser.parse_args()
    print(args)
    videos= VideoPsycho(args.duration, args.betweenstimuli, args.file, args.zoom,
                         args.output_file, args.port, args.baudrate, args.trigger, args.activation,
                        args.hauteur, args.largeur, args.random, args.launching, args.sigma)
    videos.lancement()