import argparse
import os
from psychopy import visual, core, event
import pygame
from Paradigme_parent import Parente
import random


class IA_audition(Parente):
    def __init__(self, bip, file, output, duration, betweenstimuli, afterfixation, bip_duration,sigma, launching, random,
                 hauteur, largeur, port, baudrate, trigger, activation):
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Input', 'Paradigme_IA_AUDITION'))
        self.dossier_audios = os.path.join(self.dossier, 'audios')
        self.file = file
        self.launching = launching
        self.trigger = trigger
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
        self.mouse = event.Mouse(win=self.win)
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
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        self.port = port
        self.baudrate = baudrate
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)


    def close_program(self):
        self.win.close()
        core.quit()

    def une_boucle(self, sound_name):
        if event.getKeys(keyList=["escape"]):
            self.close_program()
        audio = pygame.mixer.Sound(self.bip)
        audio.play()
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Beep", "None", "None", "None"])
        while pygame.mixer.get_busy():
            pass
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset),"Blank", "None", "None", "None"])
        while self.global_timer.getTime() < onset + self.bip_duration:
            pass
        sound = os.path.join(self.dossier_audios, sound_name)
        audio = pygame.mixer.Sound(sound)
        audio.play()
        self.rect.draw()
        self.mouse.getPressed()  # vide le buffer, afin de pas avoir un click fait avant le stimulus
        event.getKeys()  # vide le buffer, afin de pas avoir un click fait avant le stimulus
        self.win.flip()
        if self.activation :
            super().send_character(self.port, self.baudrate)
        onset = self.global_timer.getTime()  # début audio
        clicked = False
        clicked_time = "None"
        key = "None"
        while pygame.mixer.get_busy():
            button = self.mouse.getPressed()
            keys = event.getKeys()
            if not clicked:
                if any(button):
                    clicked_time = self.global_timer.getTime() - onset
                    print("Clic détecté à :", clicked_time, "secondes")
                    clicked = True
                    key = "click"
                if keys:
                    if self.trigger in keys:
                        pass
                    elif "escape" in keys:
                        self.win.close()
                        break
                    else:
                        clicked_time = self.global_timer.getTime() - onset
                        print("Touche détecté à :", clicked_time, "secondes")
                        clicked = True
                        key = keys[0]
        if clicked_time != "None":
            clicked_time = super().float_to_csv(clicked_time)
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Stimulus",key, clicked_time, sound_name])
        self.win.flip()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "Fin_stimulus", "None", "None", "None"])
        while self.global_timer.getTime() < onset + self.duration:
            pass
        sound = os.path.join(self.dossier_audios, self.croix)
        audio = pygame.mixer.Sound(sound)
        audio.play()
        onset = self.global_timer.getTime()
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(onset), "Croix de Fixation", "None", "None",  "None"])
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
                          ['onset', 'trial_type', 'key', 'reaction_time', 'stim_file'])
        self.sounds = self.reading(os.path.join(self.dossier, self.file))
        if self.random:
            random.shuffle(self.sounds)
        self.global_timer.reset()
        texts = super().inputs_texts(os.path.join(self.dossier, self.launching))
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)
        self.cross_stim.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + 12:
            pass
        self.global_timer.reset()
        for x in range(len(self.sounds)):
            self.une_boucle(self.sounds[x])
        onset = self.global_timer.getTime()
        while self.global_timer.getTime() < onset + 20:
            pass
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None", "None"])
        super().the_end(self.win)
        super().adding_duration(self.filename, self.filename_csv)
        super().writting_prt(self.filename_csv, "trial_type")



if __name__ == "__main__":
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
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")


    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")


    args = parser.parse_args()
    audition = IA_audition("bip.mp3", args.file, args.output_file, args.duration, args.betweenstimuli,
                           args.afterfixation, args.bip, args.sigma, args.launching, args.random,
                           args.hauteur, args.largeur, args.port, args.baudrate, args.trigger, args.activation)
    audition.lancement()