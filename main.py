from tokenize import Number
from numpy import testing
from numpy.lib.type_check import imag
import pygame , sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2
from tensorflow.python.keras.backend import constant



WINDOWSIZEX = 640
WINDOWSIZEY = 480

BOUNDRYINC = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = False

MODEL = load_model("/home/dell/PycharmProjects/HandWritten Digit Recongnition/bestmodel.h5")

LABELS = {0: "Zero", 1: "One",
          2: "Two", 3: "Three",
          4: "Four", 5: "Five",
          6: "Six", 7: "Seven",
          8: "Eight", 9: "Nine"}

# Initialize pygame
pygame.init()

# Font = pygame.font.Font("freesansbold.tff",18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))


pygame.display.set_caption("Digit Board")

iswriting = False

number_xcord = ['0','0','0']
number_ycord = ['0','0','0']

image_cnt = 1

REDICT = True

while True:

    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)

            number_xcord.append(xcord)
            number_xcord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord = sorted(int(number_xcord))
            number_ycord = sorted(int(number_ycord))

            rect_min_x, rect_max_x = max(number_xcord[0]-BOUNDRYINC, 0), min(WINDOWSIZEX,number_xcord[-1]+BOUNDRYINC)
            rect_min_Y, rect_max_Y = max(number_ycord[0]-BOUNDRYINC), min(number_ycord[-1]+BOUNDRYINC, WINDOWSIZEX )
     


            number_xcord = []
            number_ycord = []

            ing_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_Y:rect_max_Y].T.astype(
                np.float32)

            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt += 1

            if PREDICT:
                image = cv2.resize(img_arr, (28, 28))
                image = np.pad(image, (10, 10), 'constant', constant_values=0)
                image = cv2.resize(imag, (28, 28) / 255)

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1, 28, 28, 1)))])

                textSurface = FONT.render(label, True, RED, WHITE)
                TextRecObj = testing.get_rect()
                TextRecObj.left, TextRecObj.bottom = rect_min_x, rect_max_x

                DISPLAYSURF.blit(textSurface, TextRecObj)

            if event.type == KEYDOWN:
                if event.unicode == "n":
                    DISPLAYSURF.fill(BLACK)

    pygame.display.update()






