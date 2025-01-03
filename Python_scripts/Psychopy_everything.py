import os
import threading

import argparse
import json
import numpy as np
from psychopy import visual, core
import sounddevice as sd
import pygame
import soundfile as sf
import gc
from Paradigme_parent import Parente
from multiprocessing.pool import ThreadPool



class Psychopy_everything (Parente):

    def __init__(self, datas, launching_text, ending_text, output_file):
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
        self.fs = 44100
        self.threshold = 1000
        self.datas = datas
        self.images = []
        self.images_stim = []
        self.videos = []
        self.pool = ThreadPool(processes=2)
        self.audios = []
        self.enregistrement_thread = None
        self.audio_thread = None
        self.enregistrements = []
        self.fixations = []
        self.all = {}
        self.single_type_infos = {}
        self.multiple_type_infos = []
        self.movie_stim = None
        self.launching = launching_text
        self.ending_text = ending_text
        self.output_file = output_file
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output_file)
        self.dirname = self.filename[:self.filename.find(".tsv")]
        os.makedirs(self.dirname, exist_ok=True)
        self.record_index = 0


    def show_croix(self):
        single_type_infos = self.fixations.pop(0)
        self.cross_stim.draw()
        return single_type_infos

    def show_image(self):
        toshow = self.images_stim.pop(0)
        infos = self.images.pop(0)
        toshow.draw()
        return infos

    def show_video(self):
        single_type_infos = self.videos.pop(0)
        video_path = os.path.join(self.dossier,single_type_infos['Stimulus'])
        zoom = 0.7 + (0.012 * float(single_type_infos["Zoom"]))
        self.movie_stim = visual.MovieStim(
            win=self.win,
            filename=video_path,
            pos=(0, 0),
            size=zoom,
            opacity=1.0,
            flipVert=False,
            flipHoriz=False,
            loop=False,
            units='norm',
        )
        return single_type_infos

    def launch_enregistrement(self, single_type_infos):
        stimuli_duration = int(float(single_type_infos['Duree']))
        recording = sd.rec(int(stimuli_duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
        sd.wait()
        start_time = None
        for i, sample in enumerate(recording):
            if np.abs(sample) > self.threshold:
                start_time = i / self.fs
                break
        if start_time is not None:
            print(f"L'utilisateur a commencé à parler à {start_time:.2f} secondes.")
            self.reaction = start_time
            single_type_infos["Reaction"] = start_time
        else:
            print("Aucune parole détectée.")
            self.reaction = "/"
        record = os.path.join(self.dirname, f"record{self.record_index}.wav")
        self.record_index += 1
        sf.write(record, recording, self.fs)
    def show_enregistrement(self, need_image=True):
        single_type_infos = self.enregistrements.pop(0)
        self.enregistrement_thread= threading.Thread(target=self.launch_enregistrement, args=(single_type_infos,))
        self.enregistrement_thread.start()
        if need_image:
            image_path = os.path.join(self.dossier, "ONParler.PNG")
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )
            image_stim.draw()
        return single_type_infos


    def show_audio(self, need_image=True):
        single_type_infos = self.audios.pop(0)
        self.multiple_type_infos.append(single_type_infos)
        if need_image:
            image_path = os.path.join(self.dossier, "ONEcouter.PNG")
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )
            image_stim.draw()
        sound_path = os.path.join(self.dossier, single_type_infos["Stimulus"])
        audio = pygame.mixer.Sound(sound_path)
        audio.play()
        return single_type_infos

    def show_good_type(self, type):
        if type == "Image":
            self.multiple_type_infos.append(self.show_image())
        elif type == "Video":
            self.multiple_type_infos.append(self.show_video())
        elif type == "Audio":
            self.show_audio()
        elif type == "Croix de Fixation":
            self.multiple_type_infos.append(self.show_croix())
        else:
            self.multiple_type_infos.append(self.show_enregistrement())
        self.onset = self.global_timer.getTime()

        if self.movie_stim is not None:
            self.movie_stim.play()
        else:
            self.win.flip()
        while self.global_timer.getTime() < self.onset + float(self.multiple_type_infos[0]["Duree"]) or pygame.mixer.get_busy():
            if self.movie_stim is not None:
                self.movie_stim.draw()
                self.win.flip()
            pass
        for x in self.multiple_type_infos:
            super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.onset), x["Type"], x["Angle"], x["Zoom"], x["Reaction"], x["Stimulus"]])


        if self.movie_stim is not None:
            self.movie_stim.stop()
            self.movie_stim.setAutoDraw(False)
            self.movie_stim.seek(0)
            del self.movie_stim
            self.win.flip(clearBuffer=True)
            core.wait(0.1)
            gc.collect()
            self.movie_stim = None
        self.multiple_type_infos=[]


    def show_multiple_types (self, types):
        for type in types:
            if type == "Image":
                self.multiple_type_infos.append(self.show_image())
            elif type == "Video":
                self.multiple_type_infos.append(self.show_video())
            elif type == "Audio":
                self.audio_thread = threading.Thread(target=self.show_audio, args=(False,))
                self.audio_thread.start()
            else:
                self.multiple_type_infos.append(self.show_enregistrement(False))
        self.onset = self.global_timer.getTime()
        self.win.flip()
        while self.global_timer.getTime() < self.onset + float(self.multiple_type_infos[0]["Duree"]) or pygame.mixer.get_busy():
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

        self.multiple_type_infos = []
        if self.enregistrement_thread == None:
            for x in self.multiple_type_infos:
                super().write_tsv_csv(self.filename, self.filename_csv,
                                      [super().float_to_csv(self.onset), x["Type"],
                                       x["Angle"], x["Zoom"], x["Reaction"], x["Stimulus"]])
        else:
            self.enregistrement_thread.join()
            for x in self.multiple_type_infos:
                super().write_tsv_csv(self.filename, self.filename_csv,
                                      [super().float_to_csv(self.onset), x["Type"],
                                       x["Angle"], x["Zoom"], x["Reaction"], x["Stimulus"]])

    def lancement(self):
        super().file_init(self.filename, self.filename_csv,
                      ['onset', 'trial_type', 'angle','zoom', 'Reaction_time', 'stim_file'])
        texts = super().inputs_texts(os.path.join(self.dossier,self.launching))
        super().launching_texts(self.win, texts,"s")
        super().wait_for_trigger("s")
        for x in self.all:
            nbr = self.all[x].count(",")
            if nbr == 0:
                self.show_good_type(self.all[x])
            else:
                types = self.all[x].split(",")
                for i in range(len(types)):
                    types[i] = types[i].strip()
                self.show_multiple_types(types)
        super().write_tsv_csv(self.filename, self.filename_csv,
                              [super().float_to_csv(self.global_timer.getTime()), "END", "None", "None", "None", "None",
                               "None"])
        super().adding_duration(self.filename, self.filename_csv)
        super().the_end_file(self.win, self.ending_text)
        super().writting_prt(self.filename_csv, "trial_type")
        self.win.close()
    def preprocess(self):
        count = -1
        timer = -1.0
        for x in self.datas:
            x["Reaction"] = "/"
            if x["Apparition"] == timer:
                if x["Type"] == "Image":
                    image_path = os.path.join(self.dossier, x["Stimulus"])
                    image_stim = visual.ImageStim(
                        win=self.win,
                        image=image_path,
                        pos=(0, 0)
                    )
                    base_width, base_height = image_stim.size
                    zoom_factor = 0.5 + (0.012 * x['Zoom'])
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
                    self.enregistrements.append(x)
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
                    zoom_factor = 0.5 + (0.012 * float(x['Zoom']))
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
                    self.enregistrements.append(x)
                elif x["Type"] == "Croix de Fixation":
                    self.all[count] = "Croix de Fixation"
                    self.fixations.append(x)
            timer = x["Apparition"]




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--data", type=str, required=True, help="")
    parser.add_argument("--instructions",  type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--mot_fin",  type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")

    args = parser.parse_args()
    data = json.loads(args.data)
    E = Psychopy_everything(data, args.instructions, args.mot_fin, args.output_file)
    E.preprocess()
    E.lancement()

