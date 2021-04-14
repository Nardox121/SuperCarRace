from pygame import image
from PIL import Image
from enum import Enum

class Map:
    def __init__(self, mapPath, rewardMapPath):
        im = Image.open(rewardMapPath, "r") 
        self.mapImage = image.load(mapPath).convert()
        imageSizeW, imageSizeH = im.size
        self.map = [[MapTile.WALL if im.getpixel((i, j)) == (88, 88, 88) else MapTile.REWARD if im.getpixel((i, j)) == (255, 0, 0) else MapTile.ROAD for i in range(0, imageSizeW)] for j in range(0, imageSizeH)]

    def refresh(self, screen):
        screen.blit(self.mapImage, [0,0])

class MapTile(Enum):
    WALL = 1
    ROAD = 2
    REWARD = 3
