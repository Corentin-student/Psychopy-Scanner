import csv
import os
import random
import threading
from datetime import datetime

import argparse
import json
import numpy as np
from psychopy import visual, core, event, sound
import sounddevice as sd
import pygame
import soundfile as sf
import writtingprt as wr
import gc  # Garbage Collector
from Paradigme_parent import Parente


class Psychopy_everything (Parente):

    def __init__(self, datas):
        self.win = visual.Window(
            size=(800, 600),
            fullscr=True,
            color=[-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
            units="norm",
        )
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..', 'uploads'))
        self.global_timer = core.Clock()
        pygame.mixer.init()
        self.fs = 48000
        self.threshold = 1000
        self.datas = datas
        self.images = []
        self.images_stim = []
        self.videos = []
        self.audios = []
        self.fixations = []
        self.all = {}
        self.single_type_infos = {}
        self.movie_stim = None

    def show_croix(self):
        self.single_type_infos = self.fixations.pop(0)
        self.cross_stim.draw()


    def show_image(self):
        toshow = self.images_stim.pop(0)
        infos = self.images.pop(0)
        toshow.draw()
        return infos

    def show_video(self):
        self.single_type_infos = self.videos.pop(0)
        video_path = os.path.join(self.dossier,self.single_type_infos['Stimulus'])
        print(video_path)
        self.movie_stim = visual.MovieStim(
            win=self.win,
            filename=video_path,
            pos=(0, 0),
            size=0.7 + (0.012 *100),
            opacity=1.0,
            flipVert=False,
            flipHoriz=False,
            loop=False,
            units='norm',
        )

    def enregistrement(self):
        """recording = sd.rec(int(self.stimuli_duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
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
        sf.write(record, recording, self.fs)"""


    def show_audio(self, need_image=True):
        print("le son ?")
        self.single_type_infos = self.audios.pop(0)
        if need_image:
            image_path = os.path.join(self.dossier, "ONEcouter.PNG")
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )
            image_stim.draw()
        sound_path = os.path.join(self.dossier, self.single_type_infos["Stimulus"])
        audio = pygame.mixer.Sound(sound_path)
        audio.play()
        print("il se joue")

    def show_enregistrement(self):
        pass

    def show_good_type(self, type):
        if type == "Image":
            self.single_type_infos = self.show_image()
            print(self.single_type_infos)
        elif type == "Video":
            print("ici les infos")
            self.show_video()
        elif type == "Audio":
            self.show_audio()
        elif type == "Croix de Fixation":
            self.show_croix()
        else:
            self.show_enregistrement()
        onset = self.global_timer.getTime()

        if self.movie_stim is not None:
            self.movie_stim.play()
        else:
            self.win.flip()

        while self.global_timer.getTime() < onset + float(self.single_type_infos["Duree"]):
            if self.movie_stim is not None:
                self.movie_stim.draw()
                self.win.flip()
            pass

        if self.movie_stim is not None:
            self.movie_stim.stop()
            self.movie_stim.setAutoDraw(False)
            self.movie_stim.seek(0)
            del self.movie_stim
            self.win.flip(clearBuffer=True)
            core.wait(0.1)
            gc.collect()
            self.movie_stim = None

    def show_multiple_types (self, types):
        print("whutttttt?")
        for type in types:
            print(type)
            if type == "Image":
                self.single_type_infos = self.show_image()
            elif type == "Video":
                self.show_video()
            elif type == "Audio":
                print("type audio")
                audio_thread = threading.Thread(target=self.show_audio(need_image=False))
                audio_thread.start()
            else:
                self.show_enregistrement()
        onset = self.global_timer.getTime()
        self.win.flip()
        while self.global_timer.getTime() < onset + float(self.single_type_infos["Duree"]):
            if self.movie_stim is not None:
                self.movie_stim.draw()
                self.win.flip()
            pass

    def lancement(self):
        for x in self.all:
            print(self.all[x].count(","))
            nbr = self.all[x].count(",")
            if nbr == 0:
                self.show_good_type(self.all[x])
            else:
                print("ok ////////////////////?")
                types = self.all[x].split(",")
                for i in range(len(types)):
                    types[i] = types[i].strip()
                    print(x)
                self.show_multiple_types(types)

    def preprocess(self):
        count = -1
        timer = -1.0
        for x in self.datas:
            if x["Apparition"] == timer:
                if x["Type"] == "Image":
                    image_path = os.path.join(self.dossier, x["Stimulus"])
                    image_stim = visual.ImageStim(
                        win=self.win,
                        image=image_path,
                        pos=(0, 0)
                    )
                    base_width, base_height = image_stim.size
                    zoom_factor = 0.5 + (0.012 * 0.5)
                    image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
                    image_stim.ori = int(x["Angle"])
                    self.images_stim.append(image_stim)
                    self.images.append(x)
                    self.all[count] = self.all[count]+", Image"
                elif x["Type"] == "Video":
                    self.all[count] = self.all[count]+", Video"
                    self.videos.append(x)
                elif x["Type"] == "Audio":
                    self.all[count] = self.all[count]+", Audio"
                    self.audios.append(x)
                elif x["Type"] == "Enregistrement":
                    self.all[count] = self.all[count]+", Enregistrement"
            else :
                count+=1
                if x["Type"] == "Image":
                    image_path = os.path.join(self.dossier, x["Stimulus"])

                    image_stim = visual.ImageStim(
                        win=self.win,
                        image=image_path,
                        pos=(0, 0)
                    )
                    base_width, base_height = image_stim.size
                    zoom_factor = 0.5 + (0.012 * 0.5)
                    image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
                    image_stim.ori = int(x["Angle"])
                    self.images_stim.append(image_stim)
                    self.images.append(x)
                    self.all[count] = "Image"
                elif x["Type"] == "Video":
                    self.all[count] = "Video"
                    self.videos.append(x)
                elif x["Type"] == "Audio":
                    self.all[count] = "Audio"
                    self.audios.append(x)
                elif x["Type"] == "Enregistrement":
                    self.all[count] = "Enregistrement"
                elif x["Type"] == "Croix de Fixation":
                    self.all[count] = "Croix de Fixation"
                    self.fixations.append(x)
            timer = x["Apparition"]
        print(self.all)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--data", type=str, required=True, help="")

    args = parser.parse_args()
    print (args.data)
    data = json.loads(args.data)
    E = Psychopy_everything(data)
    E.preprocess()
    E.lancement()

