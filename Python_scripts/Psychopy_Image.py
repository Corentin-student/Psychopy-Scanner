import argparse
import csv
import os
import random
from datetime import datetime

from Paradigme_parent import Parente
from psychopy import visual, core, event
import serial



class static_image(Parente):
    def __init__(self, duration, betweenstimuli, file, zoom, output, port, baudrate, trigger, activation, hauteur,
                 largeur, random, launching, sigma):
        self.duration = duration #args.duration, args.betweenstimuli, args.file, args.zoom, args.port, args.baudrate, args.trigger  ,args.output_file)
        self.betweenstimuli = betweenstimuli
        self.file = file
        self.zoom = zoom
        self.click_times = []
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..', 'Input', 'Paradigme_images_statiques'))
        self.dossier_image = os.path.join(self.dossier,'stim_static')

        self.win = visual.Window(size=(800, 600), fullscr=True, units="norm")
        self.win.winHandle.activate()
        self.mouse = event.Mouse(win=self.win)
        event.globalKeys.add(key='escape', func=self.win.close)
        self.output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)
        self.port = port
        self.global_timer = core.Clock() #Horloge principale
        self.baudrate = baudrate
        self.trigger = trigger
        self.launching = launching
        self.sigma = sigma
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)



    def reading(self, filename):
        filenames = []
        angles = []
        with open(filename, "r") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    filenames.append(parts[0].strip())
                    angles.append(int(parts[1].strip()))
        return filenames, angles

    def static_images_psychopy(self, chemin, duration, betweenstimuli):
        chemin = os.path.join(self.dossier, chemin)
        images, orientation = self.reading(chemin)
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'trial_type', 'angle', 'reaction', 'stim_file'])
        if self.random:
            combined = list(zip(images, orientation))
            random.shuffle(combined)
            liste1_mixed, liste2_mixed = zip(*combined)
            images = list(liste1_mixed)
            orientation = list(liste2_mixed)
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )
        thezoom = 0.7 + (0.012*self.zoom)
        #thezoom = 1 if zoom else 0.5
        stimulus_times = []  # Liste pour enregistrer la durée des stimuli
        stimulus_apparition=[] #Liste pour enregistrer le timing d'apparition des stimuli
        stimuli_liste = [] #Liste pour enregistrer les noms des stimuli, si c'est une croix ce sera Fixation sinon le nom du fichier
        liste_image_win = []
        count = 0
        for image in images:
            image_path = os.path.join(self.dossier_image,image)
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )

            base_width, base_height = image_stim.size  # Taille par défaut de l'image
            zoom_factor = 0.5 + (0.012 * self.zoom)  # Ajustement du facteur de zoom

            # Ajuster la taille en fonction du facteur de zoom
            image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
            image_stim.ori = orientation[count]  # Orientation de l'image
            liste_image_win.append(image_stim)
            stimuli_liste.append(image)
            stimuli_liste.append("Fixation")
            count += 1
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts,self.trigger)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        random_gauss = random.gauss(self.betweenstimuli, self.sigma)
        while self.global_timer.getTime() < onset + random_gauss:
            pass
        trial_type = "Fixation"
        none = "None"
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), trial_type, none, none, none])
        image_count=0
        for image_stim in liste_image_win:
            image_stim.draw()
            self.rect.draw()
            self.win.flip()
            if self.activation:
                super().send_character(self.port,self.baudrate)
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            onset = self.global_timer.getTime()
            while self.global_timer.getTime() < onset + duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris

                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = self.global_timer.getTime() - onset
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiple
            stimuli = images[image_count]
            trial_type = "Stimuli"
            if clicked_time != "None":
                clicked_time = super().float_to_csv(clicked_time)
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), trial_type, image_stim.ori, clicked_time, stimuli])
            cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            random_gauss = random.gauss(self.betweenstimuli, self.sigma)
            while self.global_timer.getTime() < onset + random_gauss:
                pass
            stimuli = "None"
            trial_type = "Fixation"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), trial_type, "None", "None", stimuli])
            image_count+=1
        super().the_end(self.win)
        self.win.close()
        return stimulus_times, stimulus_apparition,stimuli_liste, orientation


    def lancement(self):
        stimulus_times, stimulus_apparition, stimuli, orientation = self.static_images_psychopy(self.file, self.duration, self.betweenstimuli)
        liste_trial=[]
        liste_lm=[]
        count=0
        for x in stimuli:
            if x == "Fixation":
                liste_lm.append(count)
                liste_trial.append("Fixation")
            else:
                liste_trial.append("Stimuli")
            count+=1
        for x in liste_lm:
            stimuli[x] = "None"
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None",
                               "None"])
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--sigma", type=float, required=True, help="ecart type pour le random")
    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    print(args)
    images = static_image(args.duration, args.betweenstimuli, args.file, args.zoom, args.output_file,
                          args.port, args.baudrate, args.trigger, args.activation, args.hauteur,
                          args.largeur, args.random, args.launching, args.sigma)
    images.lancement()