import numpy as np
from PIL import ImageGrab
import cv2
import time
from keypressinput import PressKey, ReleaseKey, Z, Slash, Space, F2, F3
import pyautogui # Unused, but for an unknown reason makes the opened window ignore Window's scaling to remain the same size as the window it monitors

def roi(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)


    game_vertices = np.array([[0, 700], [70,40], [450,40], [550,700] ])
    balls_vertices = np.array([[820,255], [860,255], [860,295], [820,295]])
    score_vertices = np.array([ [655,315], [875,315], [875,360], [675,360] ])
    processed_image = roi(processed_image, [game_vertices, balls_vertices, score_vertices])
    return processed_image




# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

# PressKey(Space)
# time.sleep(1)
# ReleaseKey(Space)
# PressKey(Z)
# time.sleep(1)
# ReleaseKey(Z)
# PressKey(Slash)
# time.sleep(1)
# ReleaseKey(Slash)

def main():
    last_time = time.time()
    while(True):
        screen = np.array(ImageGrab.grab(bbox=(0,40,900,700)))
        new_screen = process_image(screen)

        print("Loop took {} seconds".format(time.time() - last_time))
        last_time = time.time()
        cv2.imshow("window", new_screen)
        if cv2.waitKey(25) & 0xfFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()