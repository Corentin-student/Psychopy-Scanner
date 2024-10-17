import csv
import os
import random
from datetime import datetime

import argparse
from psychopy import visual, core, event
from Paradigme_parent import Parente






class Adjectifs(Parente):

    def __init__(self, duration, betweenstimuli, zoom, blocks, entrainement, per_block, filepath, output, port, baudrate,
                 trigger, activation, hauteur, largeur, random, launching):

        self.dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Input', 'Paradigme_Adjectifs'))
        self.words = self.reading( os.path.join(self.dossier, filepath))
        self.entrainement_words = self.reading( os.path.join(self.dossier, 'entrainement.txt'))
        self.me_entrainement = self.entrainement_words.copy()
        self.friend_entrainement = self.entrainement_words.copy()
        self.syllable_entrainement = self.entrainement_words.copy()
        self.me_blocks = self.words.copy()
        self.friend_blocks = self.words.copy()
        self.syllabe_blocks = self.words.copy()
        self.Syllabe_shortcue=""
        self.Me_shortcue=""
        self.Friend_shortcue=""
        self.shown_words = []
        self.order_blocks = []
        self.reaction_time = []
        self.response = []
        self.keys = ["c","q","d","b"]
        self.launching = launching
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.zoom = zoom
        self.filepath = filepath
        self.output = output
        self.number_of_blocks = blocks
        self.entrainement_block = entrainement
        self.per_block = per_block
        self.experience_text = ""
        self.hashmapvaleurs= {"d":"1", "q":"2", "c":"3", "b":"4", "1":"1", "2":"2","3":"3", "4":"4", "&":"1","é":"2","#":"3","'":"4"}
        self.port = port
        self.baudrate = baudrate
        self.trigger = trigger
        self.global_timer = core.Clock()
        self.timer = core.Clock()
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)

        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False

        self.win = visual.Window(size=(800, 600), fullscr=True , units="norm")
        self.win.winHandle.activate()
        self.explication_texts = super().inputs_texts( os.path.join(self.dossier, self.launching))

        event.globalKeys.add(key='escape', func=self.win.close)

        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)

    def reading(self,filename):
        with open(filename, "r", encoding="utf-8") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def lancement(self):
        self.Premier_texte = self.explication_texts[0]

        texte = visual.TextStim(self.win, text=self.Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)
        Deuxieme_texte = self.explication_texts[1]

        texte.text = Deuxieme_texte
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)
        troisieme_texte = self.explication_texts[2]

        texte.text = troisieme_texte
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)

        quatrieme_texte = self.explication_texts[3]

        texte.text = quatrieme_texte
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)

        cinquieme_texte = self.explication_texts[4]

        texte.text = cinquieme_texte
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)

        self.experience_text = self.explication_texts[5]


        self.Me_shortcue = self.explication_texts[6]

        self.Friend_shortcue = self.explication_texts[7]

        self.Syllabe_shortcue = self.explication_texts[8]

        self.entrainement()
        texte.text = self.experience_text
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'duration', 'block_type', 'word', 'key', 'response_time'])
        texte.draw()
        self.win.flip()
        super().proper_waitkey(self.trigger)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()

        self.blocks()
        super().writting_prt(self.filename_csv, "block_type")



    def debut_me(self):
        texte_block = visual.TextStim(self.win, text=self.Me_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_friend(self):
        texte_block = visual.TextStim(self.win, text=self.Friend_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_syllabe(self):
        texte_block = visual.TextStim(self.win, text=self.Syllabe_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass



    def show_1_word(self, mot , block_type):
        texte_5_words = visual.TextStim(self.win, color=[1, 1, 1], wrapWidth=1.5, font="Arial", height=0.1 + (0.004*self.zoom))
        texte_5_words.text = mot
        texte_5_words.draw()
        self.rect.draw()
        self.win.flip()
        onset = self.global_timer.getTime()
        if self.activation:
            super().send_character(self.port, self.baudrate)
        response_time="None"
        k="None"
        self.timer.reset()
        while self.timer.getTime() < self.stimuli_duration:  # Limite de temps de 4 secondes
            if k=="None":
                key = event.getKeys()
                #d=1, q=2, c=3, b=4
                if "d" in key or "q" in key or 'c' in key or "b" in key  or "1" in key or "2" in key or "3" in key or "4" in key or "&" in key or "é" in key or "#" in key or "'" in key:
                    k = self.hashmapvaleurs.get(key[0])
                    response_time=self.timer.getTime()
                    texte_5_words.text=" "
                    texte_5_words.draw()
                    self.win.flip()
        time_long = self.timer.getTime()
        if response_time!="None":
            response_time=super().float_to_csv(response_time)
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), super().float_to_csv(time_long), block_type, mot, k, response_time])


        self.win.flip()


    def show_words(self,count, block_type):
        if count !=0:
            mot=""
            if block_type == "me":
                if self.random :
                    mot = random.choice(self.me_blocks)
                else:
                    mot = self.me_blocks[0]
                self.me_blocks.remove(mot)
            if block_type == "friend":
                if self.random:
                    mot=random.choice(self.friend_blocks)
                else:
                    mot = self.friend_blocks[0]
                self.friend_blocks.remove(mot)
            if block_type == "syllabe":
                if self.random:
                    mot=random.choice(self.syllabe_blocks)
                else:
                    mot = self.syllabe_blocks[0]
                self.syllabe_blocks.remove(mot)
            self.show_1_word(mot, block_type)
            self.shown_words.append(mot)
            self.order_blocks.append(block_type)
            self.show_words(count-1,block_type)


    def write_tsv(self,):
        filename= self.output
        filename = super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['block_type', 'word', 'response', 'response_time'])
            pred = 0
            count = 0
            for i in range(len(self.shown_words)):
                tsv_writer.writerow(
                    [self.order_blocks[i], self.shown_words[i], self.response[i], self.reaction_time[i]])
                count += 1

    def entrainement_show_words(self, count, block_type):
        if count !=0:
            mot=""
            if block_type == "me":
                if self.random:
                    mot = random.choice(self.me_entrainement)
                else:
                    mot = self.me_entrainement[0]
                self.me_entrainement.remove(mot)
            if block_type == "friend":
                if self.random:
                    mot=random.choice(self.friend_entrainement)
                else:
                    mot = self.friend_entrainement[0]
                self.friend_entrainement.remove(mot)
            if block_type == "syllabe":
                if self.random:
                    mot=random.choice(self.syllable_entrainement)
                else:
                    mot = self.syllable_entrainement[0]
                self.syllable_entrainement.remove(mot)
            self.show_1_word(mot, block_type)
            self.entrainement_show_words(count-1,block_type)

    def entrainement(self):
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        number_of_blocks = self.entrainement_block
        choice_block = ["me", "friend", "syllabe"]
        longueur = len(self.entrainement_words) // self.per_block
        hashmap = {"me": longueur, "friend": longueur, "syllabe": longueur}

        for x in range(number_of_blocks):
            if len(choice_block) == 0:
                break
            block = random.choice(choice_block)
            hashmap[block] -= 1
            if hashmap[block] == 0:
                choice_block.remove(block)

            if block == "me":
                self.debut_me()
                self.entrainement_show_words(self.per_block, block)
            elif block == "friend":
                self.debut_friend()
                self.entrainement_show_words(self.per_block, block)
            elif block == "syllabe":
                self.debut_syllabe()
                self.entrainement_show_words(self.per_block, block)

            cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            fixation_duration = self.betweenstimuli
            self.timer.reset()
            while self.timer.getTime() < fixation_duration:
                cross_stim.draw()
                self.win.flip()
            time_long = self.timer.getTime()
            block_type = "Fixation"
            mot = "None"
            key = "None"
            response_time = "None"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), block_type, mot, key, response_time])

    def blocks(self):
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        number_of_blocks = self.number_of_blocks
        choice_block = ["me", "friend", "syllabe"]
        longueur = len(self.words)//self.per_block
        hashmap = {"me": longueur, "friend": longueur, "syllabe": longueur}
        fixation_duration = self.betweenstimuli  # en secondes

        for x in range(number_of_blocks):
            if len(choice_block)==0:
                break
            block = random.choice(choice_block)
            hashmap[block] -= 1
            if hashmap[block] == 0:
                choice_block.remove(block)

            if block == "me":
                self.debut_me()
                self.show_words(self.per_block,block)
            elif block == "friend":
                self.debut_friend()
                self.show_words(self.per_block,block)
            elif block == "syllabe":
                self.debut_syllabe()
                self.show_words(self.per_block,block)

            # Affichage de la croix de fixation pendant 100 secondes
            cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            self.timer.reset()
            while self.timer.getTime() < fixation_duration:
                cross_stim.draw()
                self.win.flip()
            time_long = self.timer.getTime()
            block_type = "Fixation"
            mot = "None"
            key = "None"
            response_time = "None"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), block_type, mot, key, response_time])

    def fin(self):
        super().the_end(self.win)
        self.win.close()
        core.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--zoom", type=float, required=True, help="Le zoom sur les adjectifs")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--blocks", type=int, required=True, help="Nombre de blocks d'adjectifs")
    parser.add_argument("--entrainement", type=int, required=True, help="Nombre de blocks d'entrainement")
    parser.add_argument("--per_block", type=int, required=True, help="Nombre d'adjectifs pas block")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    paradigm = Adjectifs(args.duration, args.betweenstimuli, args.zoom, args.blocks, args.entrainement, args.per_block,
                         args.file, args.output_file, args.port, args.baudrate, args.trigger, args.activation,
                        args.hauteur, args.largeur, args.random, args.launching)
    paradigm.lancement()
    paradigm.fin()


