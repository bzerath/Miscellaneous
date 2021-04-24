import pyautogui
import time

COOKIE_droite = (2351, 1100)
COOKIE_gauche = (-200, 1172)
COOKIE_full_droite = (397, 595)

videoviewer_full_gauche = (-471, 773)


def click(x, y):
    pyautogui.platformModule._click(x, y, pyautogui.LEFT)
    time.sleep(0.016)


if __name__ == "__main__":

    COOKIE = videoviewer_full_gauche
    # COOKIE = COOKIE_droite
    # COOKIE = COOKIE_full_droite

    pyautogui.moveTo(*COOKIE)
    click(*COOKIE)
    i = 0
    begin = time.time()

    while True:
        i += 1
        if i % 100 == 0:
            print(i, int(i / (time.time() - begin)))
        click(*COOKIE)
        position = pyautogui.position()
        if int(position.x - COOKIE[0]) > 5 or int(position.y - COOKIE[1]) > 5:
            print(position.x - COOKIE[0], position.y - COOKIE[1])
            break
