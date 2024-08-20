import csv
import random

import argparse
from psychopy import visual, core, event
from Paradigme_parent import Parente


class launch_cyberball(Parente) :
    def __init__(self, phase1, transition, exclusion, minimum, maximum) :

        self.win = visual.Window(units="norm", fullscr=True)

        # Chargement des self.images
        self.image1 = visual.ImageStim(win=self.win, image='Cyberball/Banque_personnage/waiting.png', pos=[0, 0.5])
        self.image2 = visual.ImageStim(win=self.win, image='Cyberball/Banque_personnage/waiting.png', pos=[-0.5, -0.5])
        self.image3 = visual.ImageStim(win=self.win, image='Cyberball/Banque_personnage/waiting.png', pos=[0.5, -0.5])

        self.photo1 = visual.ImageStim(win=self.win, image='Cyberball/Homme2.jpg', pos=[0.3, 0.8], size=0.2)
        self.photo2 = visual.ImageStim(win=self.win, image='Cyberball/Femme2.jpg', pos=[-0.8, -0.8], size=0.2)
        self.photo3 = visual.ImageStim(win=self.win, image='Cyberball/Homme1.jpg', pos=[0.8, -0.8], size=0.2)

        self.text1 = visual.TextStim(win=self.win, text="Player_1", pos=[0, 0.8], color=(-1, -1, -1))
        self.text2 = visual.TextStim(win=self.win, text="Jeanne", pos=[-0.5, -0.8], color=(-1, -1, -1))
        self.text3 = visual.TextStim(win=self.win, text="Paul", pos=[0.5, -0.8], color=(-1, -1, -1))

        # Chargement de l'self.image de la balle
        self.ball = visual.ImageStim(win=self.win, image='Cyberball/Banque_personnage/ball.png', pos=[0, 0], size=0.1)

        self.player1 = {"image" : self.image1, "sens": "gauche", "right": "droite", "left": "gauche"}
        self.player2 = {"image" : self.image2, "sens": "droite"}
        self.player3 = {"image" : self.image3, "sens": "gauche"}
        self.players = [self.player1, self.player2, self.player3]
        event.globalKeys.add(key='escape', func=self.win.close)
        self.timer = core.Clock()
        self.period_timer = core.Clock()
        self.global_timer = core.Clock()
        self.proba = [0.52, 0.48, 0.48]
        self.phase1 = phase1
        self.transition = transition
        self.exclusion = exclusion
        self.minimum = minimum
        self.maximum = maximum
        self.onset = []
        self.duration = []
        self.phase = []

    def write_tsv(self, filename="output1.tsv"):
        filename = super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'phase', 'duration'])
            type_stimuli = []
            for x in range(len(self.stimuli)):
                if self.pas_un_stimuli(self.stimuli[x]):
                    type_stimuli.append("Noise")
                else:
                    type_stimuli.append("Stimuli")
            for i in range(len(self.stimuli_apparition)):
                tsv_writer.writerow([self.stimuli_apparition[i], self.stimuli_times[i], self.stimuli[i], type_stimuli[i]])

# Fonction pour dessiner tous les éléments
    def draw_all(self):
        self.image1.draw()
        self.image2.draw()
        self.image3.draw()
        self.photo1.draw()
        self.photo2.draw()
        self.photo3.draw()
        self.text1.draw()
        self.text2.draw()
        self.text3.draw()

# Animation de la balle du centre à self.image1, puis à self.image2
    def move_ball(self, ball, start_pos, end_pos, duration=2.0):
        steps = 60
        for i in range(steps):
            new_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * (i / float(steps)),
                start_pos[1]+0.2 + (end_pos[1] - start_pos[1]) * (i / float(steps))
            ]
            ball.pos = new_pos
            self.draw_all()
            ball.draw()
            self.win.flip()
            core.wait(duration / steps)

    def ball_receptie(self, player):
        path = "Cyberball/Banque_personnage/"
        player["image"].image = path+"lancement_"+player["sens"]+".png"
        self.draw_all()
        self.win.flip()
        core.wait(0.3)
        player["image"].image = path+"lancer_"+player["sens"]+".png"
        self.draw_all()
        self.win.flip()
        core.wait(0.2)
        player["image"].image = path+"waiting.png"

    def reception (self, player):
        path = "Cyberball/Banque_personnage/"
        player["image"].image = path+"waiting_ball.png"
        self.draw_all()
        self.win.flip()


    def lancement(self):
        texte = visual.TextStim(self.win, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
        Sans_point = ("En attente de tous les participants")
        Premier_texte = ("En attente de tous les participants.")
        Deuxieme_texte = ("En attente de tous les participants..")
        Troisieme_texte = ("En attente de tous les participants...")
        self.global_timer.reset()
        while self.global_timer.getTime() < 10:
            texte.text = Sans_point
            texte.draw()
            self.win.flip()
            self.timer.reset()
            while self.timer.getTime() < 0.5:
                pass
            texte.text = Premier_texte
            texte.draw()
            self.win.flip()
            self.timer.reset()
            while self.timer.getTime() < 0.5:
                pass
            texte.text = Deuxieme_texte
            texte.draw()
            self.win.flip()
            self.timer.reset()
            while self.timer.getTime() < 0.5:
                pass
            texte.text = Troisieme_texte
            texte.draw()
            self.win.flip()
            self.timer.reset()
            while self.timer.getTime() < 0.5:
                pass
        self.game()





    def lancer(self,sens, depart, arrive):
        self.move_ball(self.ball, depart.pos, arrive.pos, duration=0.5)
        self.ball_receptie(arrive)
        core.wait(0.3)


    def game (self):
        self.move_ball(self.ball, [0, -0.3], [0, -0.3], duration=3)
        filtered_list = [x for x in self.players if x != self.player1]
        choice = random.choice(filtered_list)
        self.move_ball(self.ball, [0, -0.3], choice["image"].pos, duration=0.3)
        self.period_timer.reset()
        self.onset.append(self.global_timer.getTime())
        self.phase.append("Phase Normale")
        while self.period_timer.getTime() < self.phase1:
            if choice == self.player1:
                choice = self.joueur(choice["image"].pos)
            elif choice == "None":
                choice = random.choice(filtered_list)
                core.wait(0.4)
                self.move_ball(self.ball, [0, -0.3], choice["image"].pos, duration=0.3)
            else:
                choice = self.ordinateur(choice)
        self.duration.append(self.period_timer.getTime())
        self.proba = [0.35, 0.65, 0.65]
        self.phase.append("Phase de transition 1")
        self.period_timer.reset()
        self.onset.append(self.global_timer.getTime())
        while self.period_timer.getTime() < (self.transition/2):
            if choice == self.player1:
                choice = self.joueur(choice["image"].pos)
            elif choice == "None":
                choice = random.choice(filtered_list)
                core.wait(0.4)
                self.move_ball(self.ball, [0, -0.3], choice["image"].pos, duration=0.3)
            else:
                choice = self.ordinateur(choice)
        self.duration.append(self.period_timer.getTime())
        self.proba = [0.15, 0.85, 0.85]
        self.phase.append("Phase de transition 2")
        self.period_timer.reset()
        self.onset.append(self.global_timer.getTime())
        while self.period_timer.getTime() < (self.transition/2):
            if choice == self.player1:
                choice = self.joueur(choice["image"].pos)
            elif choice == "None":
                choice = random.choice(filtered_list)
                core.wait(0.4)
                self.move_ball(self.ball, [0, -0.3], choice["image"].pos, duration=0.3)
            else:
                choice = self.ordinateur(choice)
        self.duration.append(self.period_timer.getTime())
        self.proba = [0, 1, 1]
        self.phase.append("Phase d'exclusion")
        self.period_timer.reset()
        self.onset.append(self.global_timer.getTime())
        while self.period_timer.getTime() < self.exclusion:
            if choice == self.player1:
                choice = self.joueur(choice["image"].pos)
            elif choice == "None":
                choice = random.choice(filtered_list)
                core.wait(0.4)
                self.move_ball(self.ball, [0, -0.3], choice["image"].pos, duration=0.3)
            else:
                choice = self.ordinateur(choice)
        self.duration.append(self.period_timer.getTime())
        print(self.onset)
        print(self.duration)
        print(self.phase)

    def ordinateur (self,player):
        self.reception(player)
        self.timer.reset()
        next = player
        while self.timer.getTime() < random.uniform(self.minimum, self.maximum):
            if next == player :
                #filtered_list = [x for x in self.players if x != player]
                other_list = self.players.copy()
                probas = self.proba.copy()
                i = other_list.index(player)
                del probas[i]
                del other_list[i]
                #next= random.choice (filtered_list)
                next = random.choices(other_list, weights=probas, k=1)[0]
        self.ball_receptie(player)
        self.move_ball(self.ball, player["image"].pos, next["image"].pos, duration=0.3)
        return next



    def joueur (self, position):
        self.reception(self.player1)
        next = "None"
        self.timer.reset()
        d=0
        while self.timer.getTime() < 4:
            key = event.getKeys()
            if key == ['right']:
                self.player1["sens"] = "droite"
                next = self.player3
                d=1
                key = ""
                break
            elif key == ['left']:
                self.player1["sens"] = "gauche"
                next = self.player2
                d=1
                key = ""
                break
        self.ball_receptie(self.player1)
        if d==1:
            self.move_ball(self.ball, self.player1["image"].pos, next["image"].pos, duration=0.3)
        else:
            self.move_ball(self.ball, self.player1["image"].pos, [0, -0.3], duration=0.5)
        return next


if __name__ == "__main__":
    """
    print("walilou")
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--premiere_phase", type=int, required=True, help="Durée en secondes de la première phase")
    parser.add_argument("--exclusion", type=int, required=True, help="Durée en secondes de la phase d'exclusion")
    parser.add_argument("--transition", type=int, required=True, help="Durée en secondes des transitions")
    parser.add_argument("--minimum", type=int, required=True, help="Durée en secondes du temps de réaction minimum")
    parser.add_argument("--maximum", type=int, required=True, help="Durée en secondes du temps de réaction maximum")
    parser.add_argument("--filePath", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument('--port', type=str, required=True, help="Port")
    parser.add_argument('--baudrate', type=int, required=True, help="Speed port")
    parser.add_argument('--trigger', type=str, required=True, help="caractère pour lancer le programme")
    print("ok on comprends ?")
    args = parser.parse_args()
    print (args.maximum)
    print("okkkkkkklmm")"""

    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--premiere_phase", type=int, required=True, help="Durée en secondes de la première phase")
    parser.add_argument("--exclusion", type=int, required=True, help="Durée en secondes de la phase d'exclusion")
    parser.add_argument("--transition", type=int, required=True, help="Durée en secondes des transitions")
    parser.add_argument("--minimum", type=float, required=True, help="Durée en secondes du temps de réaction minimum")
    parser.add_argument("--maximum", type=float, required=True, help="Durée en secondes du temps de réaction maximum")

    parser.add_argument("--filePath", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument('--port', type=str, required=True, help="Port")
    parser.add_argument('--baudrate', type=int, required=True, help="Speed port")
    parser.add_argument('--trigger', type=str, required=True, help="caractère pour lancer le programme")
    args = parser.parse_args()




    phase1=120
    transition = 60
    exclusion = 120
    minimum = 0.7
    maximum = 3
    C=launch_cyberball(args.premiere_phase,args.transition,args.exclusion,args.minimum,args.maximum)
    C.lancement()

random_float_between_bounds = random.uniform(0.3, 2.5)
