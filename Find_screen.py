import numpy as np
from PIL import ImageGrab
import cv2
import time
from keypressinput import PressKey, ReleaseKey, Z, Slash, Space, F2, F3
import pyautogui # Unused, but for an unknown reason makes the opened window ignore Window's scaling to remain the same size as the window it monitors


def draw_circles(image, circles):
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (255, 255, 255), 10)


def roi(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def process_image(original_image):
    # ballLower =
    # mask2 = cv2.inRange(image, ballLower, ballUpper)


    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=100, threshold2=200)
    game_vertices = np.array([[0, 700], [70,40], [450,40], [550,700] ])
    balls_vertices = np.array([[820,255], [860,255], [860,295], [820,295]])
    score_vertices = np.array([ [655,315], [875,315], [875,360], [675,360] ])
    processed_image = roi(processed_image, [game_vertices, balls_vertices, score_vertices])

    ball = cv2.HoughCircles(processed_image, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=200, minRadius=0,maxRadius=50)
    # draw_circles(processed_image, ball)

    if ball is not None:
        circles = np.uint16(np.around(ball))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(processed_image, (i[0], i[1]), i[2], (255, 255, 255), 10)
            # draw the center of the circle
            cv2.circle(processed_image, (i[0], i[1]), 2, (0, 0, 255), 3)

    return processed_image

def test():
    image = cv2.imread("RedCircle.png")
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
        cv2.imshow("output", np.hstack([image, output]))
        cv2.waitKey(0)


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
    # test()



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