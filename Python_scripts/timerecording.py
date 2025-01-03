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
    def __init__(self):
        self.dossier = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Input', 'Paradigme_IA_IMAGE'))
        self.dossier_image = os.path.join(self.dossier, 'images')
        self.trigger = "s"
        self.duration = 1
        self.betweenstimuli = 1
        self.filename, self.filename_csv = super().preprocessing_tsv_csv("test_image")
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
        self.sigma = 0
        if random == "True":
            self.random = True
        else:
            self.random = False
        self.dossier = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Input', 'Paradigme_EMO_VOICES'))
        self.image_stim = visual.ImageStim(
            win=self.win,
            image=os.path.join(self.dossier, 'oreille.png'),
            pos=(0, 0)
        )
        self.clock= core.Clock()
        super().file_init(self.filename, self.filename_csv,
                          ['onset'])

    def lancement(self):
        self.clock.reset()
        for x in range (10):
            onset = self.clock.getTime()

            self.image_stim.draw()
            self.win.flip()
            while self.clock.getTime() < onset + 1:
                pass
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset)])

x = IA_image().lancement()
