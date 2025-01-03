import argparse
import csv
import os
import random
from datetime import datetime

from Paradigme_parent import Parente
from psychopy import visual, core, event
from collections import defaultdict
import serial
import random



class IA_image(Parente):
    def __init__(self, file, output, zoom, duration, betweenstimuli, sigma, launching, random):
        self.dossier = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Input', 'Paradigme_IA_IMAGE'))
        self.dossier_image = os.path.join(self.dossier, 'images')
        self.file = file
        self.launching = launching
        self.trigger = "s"
        self.zoom = zoom
        self.duration = duration
        self.betweenstimuli = betweenstimuli
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)
        self.win = visual.Window(
            size=(800, 600),
            fullscr=True,
            color=[-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
            units="norm",
        )
        self.win.winHandle.activate()
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.02), (0, 0.02), (0, 0), (-0.02, 0), (0.02, 0)),
            lineWidth=8,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        event.globalKeys.add(key='escape', func=self.win.close)
        self.global_timer = core.Clock()
        self.onset = None
        self.sigma = sigma
        if random == "True":
            self.random = True
        else:
            self.random = False

    def boucle_dans_la_boucle(self,image):
        image.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        print("début image : " + str(onset))
        while self.global_timer.getTime() < onset + 0.4 :
            pass
        print("fin image : " + str(self.global_timer.getTime()))
        self.win.flip()
        while self.global_timer.getTime() < onset + 0.5 :
            pass

    def une_boucle(self, images):
        print(len(images))
        count = 0 #pour chopper le nom de l'image
        for image in images:
            self.onset = self.global_timer.getTime()
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(self.onset), "Stimulus", self.images[count]])
            while self.global_timer.getTime() < self.onset + self.duration :
                self.boucle_dans_la_boucle(image)
            self.cross_stim.draw()
            self.win.flip()
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(self.global_timer.getTime()), "Croix de fixation", "/"])
            random_gauss = random.gauss(self.betweenstimuli, self.sigma)
            while self.global_timer.getTime() < self.onset + self.duration + random_gauss - 1:
                pass
            self.cross_stim.lineColor = "red"
            self.cross_stim.draw()
            self.win.flip()
            while self.global_timer.getTime() < self.onset + self.duration + random_gauss:
                pass
            self.cross_stim.lineColor = "white"
            count+=1

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def group_by_prefix(self,images):
        groups = defaultdict(list)
        for image in images:
            prefix = image.split("_")[0]
            groups[prefix].append(image)
        return groups

    def ajout_where_nothing(self,images,groups,groupe):
        toinsert = []
        for i in range(len(images)-1):
            actual_prefix = images[i].split("_")[0]
            next_prefix = images[i+1].split("_")[0]
            if i == 0 and actual_prefix != groupe:
                toinsert.append(i)
            else:
                if groupe == actual_prefix or groupe == next_prefix:
                    pass
                else:
                    toinsert.append(i+1)
        for j in reversed(toinsert):
            if len(groups[groupe])== 1:
                images.insert(j,groups[groupe].pop())
                return images
            else:
                images.insert(j, groups[groupe].pop())
        return images


    def shuffle_groups(self,groups):
        images = []
        previous_groupe = ""
        while len(groups)!=0:
            groupe = random.choice(list(groups.keys()))
            if groupe == previous_groupe:
                if len(groups)==1:
                    images = self.ajout_where_nothing(images,groups,groupe)
                    return images
            else:
                x = random.choice(groups[groupe])
                groups[groupe].remove(x)
                if len(groups[groupe]) == 0:
                    groups.pop(groupe)
                images.append(x)
                previous_groupe = groupe

        return images
    def lancement(self):
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'trial_type', 'stim_file'])
        self.images = self.reading(os.path.join(self.dossier,self.file))
        if self.random:
            gr = self.group_by_prefix(self.images)
            self.images =  self.shuffle_groups(gr)
        images_stim = []
        for x in self.images:
            image_path = os.path.join(self.dossier_image, x)
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )
            base_width, base_height = image_stim.size
            image_stim.size = (base_width , base_height)
            image_stim.ori = 0
            images_stim.append(image_stim)
            base_width, base_height = image_stim.size  # Taille par défaut de l'image
            zoom_factor = 0.5 + (0.012 * self.zoom)  # Ajustement du facteur de zoom
            image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + 12:
            pass
        self.global_timer.reset()
        self.une_boucle(images_stim)
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + 20:
            pass
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--output_file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--sigma", type=float, required=True, help="ecart type pour le random")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")



    args = parser.parse_args()
    print(args.file)
    print(args.output_file)
    my_ia = IA_image(args.file, args.output_file, args.zoom, args.duration, args.betweenstimuli, args.sigma,
                     args.launching, args.random)
    my_ia.lancement()
