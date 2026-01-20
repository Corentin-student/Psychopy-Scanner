import cv2
import numpy as np
from psychopy import visual, core, event

win = visual.Window(
    size=(800, 600),
    units="pix",
    fullscr=False,
    waitBlanking=False
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cam_stim = visual.ImageStim(
    win,
    size=(640, 480),
    units="pix"
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = frame.astype(np.float32)
    frame = (frame / 127.5) - 1.0

    frame *= 1.3
    frame = np.clip(frame, -1.0, 1.0)

    frame = np.flipud(frame)

    cam_stim.image = frame
    cam_stim.draw()
    win.flip()

    if 'escape' in event.getKeys():
        break

cap.release()
win.close()
core.quit()
