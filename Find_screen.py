import numpy as np
# from PIL import ImageGrab
from grabscreen import grab_screen
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
    # processed_image = cv2.Canny(processed_image, threshold1=100, threshold2=200)
    game_vertices = np.array([[0, 700], [70,40], [450,40], [550,700] ])
    balls_vertices = np.array([[820,255], [860,255], [860,295], [820,295]])
    score_vertices = np.array([ [655,315], [875,315], [875,360], [675,360] ])
    processed_image = roi(original_image, [game_vertices, balls_vertices, score_vertices])
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    return processed_image


def find_ball(image):
    ball_template = cv2.imread("Pictures\BallTemplate.png",0)
    w, h = ball_template.shape[::-1]

    res = cv2.matchTemplate(image, ball_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    location = np.where(res >= threshold)
    return location, w, h

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

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
    is_key_pressed = False
    while True:
        #screen = np.array(ImageGrab.grab(bbox=(0,40,900,700)))
        screen = grab_screen(region=(0, 40, 900, 700))
        new_screen = process_image(screen)
        ball_location, width, height = find_ball(new_screen)
        ball_x = 0
        ball_y = 0
        number_of_points = 0
        for point in zip(*ball_location[::-1]):
            ball_x += point[0]
            ball_y += point[1]
            number_of_points += 1
        if is_key_pressed:
            ReleaseKey(Z)
            ReleaseKey(Slash)
            is_key_pressed = False
        if number_of_points != 0:
            ball_x = int(ball_x/number_of_points)
            ball_y = int(ball_y/number_of_points)
            cv2.rectangle(new_screen, (ball_x, ball_y), (ball_x + width, ball_y + height), (255,255,255),5)

            if ball_y >= 550:
                if ball_x >= 180 and ball_x <= 275:
                    PressKey(Z)
                    is_key_pressed = True
                elif ball_x <= 350:
                    PressKey(Slash)
                    is_key_pressed = True
                elif ball_x > 465:
                    PressKey(Space)
                    time.sleep(1)
                    ReleaseKey(Space)




        time_since_last_loop = time.time() - last_time
        print("Loop took {} seconds".format(time_since_last_loop))


        last_time = time.time()
        cv2.imshow("window", new_screen)
        if cv2.waitKey(25) & 0xfFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()
