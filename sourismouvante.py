import pyautogui
import time
import math
import keyboard

radius = 100
center_x, center_y = pyautogui.position()
steps = 100

print("Le script tourne. Appuyez sur 'q' pour quitter.")

try:
    while True:
        if keyboard.is_pressed('q'):
            print("Arrêt du script...")
            break
        for angle in range(0, 360, int(360 / steps)):
            if keyboard.is_pressed('q'):
                print("Arrêt du script...")
                break
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            pyautogui.moveTo(x, y, duration=0.001)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nInterruption clavier détectée. Fin du script.")