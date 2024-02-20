import math

WIDTH = 720
HEIGHT = 720
FPS = 24

SPEED = 20

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


VIEWERPOS = [0, 160, 0]
SCREENPOS = VIEWERPOS[2] + (HEIGHT / 2) / (1 / math.sqrt(3))
print("VIEWERPOS", VIEWERPOS)
print("screenPOS", SCREENPOS)
K = SCREENPOS - VIEWERPOS[2]

SCALE = 100
