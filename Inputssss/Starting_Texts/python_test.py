
from psychopy import event, core
import re

timer = core.Clock()
def inputs_texts(chemin):
    with open(chemin, 'r', encoding='utf-8') as file:
        contenu = file.read()
    texts = re.findall(r'\|(.*?)\|', contenu, re.DOTALL)
    return texts

import serial
port = 'COM3'
baudrate = 9600

trigger_char='s'
ser = serial.Serial('COM3', 9600)

def duration_input(timer, duration):
    timer.reset()
    while timer.getTime()<duration:
        trigger = ser.read().decode('utf-8')
        print(f"Trigger received: {trigger}")

duration_input(timer,2)
