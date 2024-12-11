import argparse
import os
from psychopy import visual, core, event, sound
import pygame
from Paradigme_parent import Parente
import random



class IA_audition(Parente):
    def __init__(self, bip, file, output, duration, betweenstimuli, afterfixation, bip_duration,sigma, launching, random):
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Input', 'Paradigme_IA_AUDITION'))
        self.dossier_audios = os.path.join(self.dossier, 'audios')
        self.file = file
        self.launching = launching
        self.trigger = "s"
        output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)
        self.fs = 48000
        self.threshold = 1000
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
            lineWidth=5,
            closeShape=False,
            lineColor="white",
            units='height'
        )

        event.globalKeys.add(key='escape', func=self.win.close)
        self.bip = os.path.join(self.dossier_audios, bip)
        self.sounds= self.reading(os.path.join(self.dossier, self.file))
        self.global_timer = core.Clock()
        pygame.mixer.init()
        self.random=False
        self.croix = os.path.join(self.dossier_audios, "croix.mp3")
        self.duration = duration
        self.betweenstimuli = betweenstimuli
        self.afterfixation = afterfixation
        self.bip_duration = bip_duration
        self.sigma = sigma
        image_path = os.path.join(self.dossier_audios, "ONEcouter.PNG")
        self.image_stim = visual.ImageStim(
            win=self.win,
            image=image_path,
            pos=(0, 0)
        )
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.02), (0, 0.02), (0, 0), (-0.02, 0), (0.02, 0)),
            lineWidth=8,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        if random == "True":
            self.random = True
        else:
            self.random = False



    def une_boucle(self, sound):
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Beep", "/"])
        audio = pygame.mixer.Sound(self.bip)
        audio.play()
        while pygame.mixer.get_busy():
            pass
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset),"Blank", "/"])
        while self.global_timer.getTime() < onset + self.bip_duration:
            pass
        onset = self.global_timer.getTime() #début audio
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Stimulus", sound])
        sound = os.path.join(self.dossier_audios, sound)
        audio = pygame.mixer.Sound(sound)
        audio.play()
        while pygame.mixer.get_busy():
            pass
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "Fin_stimulus", "/"])
        while self.global_timer.getTime() < onset + self.duration:
            pass
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Croix de Fixation", "/"])
        sound = os.path.join(self.dossier_audios, self.croix)
        audio = pygame.mixer.Sound(sound)
        audio.play()
        random_gauss = random.gauss(self.betweenstimuli, self.sigma)
        while self.global_timer.getTime()  < onset + random_gauss:
            pass
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + self.afterfixation:
            pass


    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste
    def lancement(self):
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'trial_type', 'stim_file'])
        self.sounds = self.reading(os.path.join(self.dossier, self.file))
        if self.random:
            random.shuffle(self.sounds)
        self.global_timer.reset()
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)
        self.cross_stim.draw()
        self.win.flip()
        for x in range(len(self.sounds)):
            self.une_boucle(self.sounds[x])
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None",
                               "None"])
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")



if __name__ == "__main__":
    print("okkk?")
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--output_file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--afterfixation", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--bip", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--sigma", type=float, required=True, help="ecart type pour le random")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")


    args = parser.parse_args()
    print(args.file)
    print(args.output_file)
    audition = IA_audition("bip.mp3", args.file, args.output_file, args.duration, args.betweenstimuli,
                           args.afterfixation, args.bip, args.sigma, args.launching, args.random)
    audition.lancement()