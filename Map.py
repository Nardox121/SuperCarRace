from pygame import draw, Color, Rect, image, display
from PIL import Image
from enum import Enum

class Map:
    def __init__(self, mapPath):
        im = Image.open(mapPath, "r") 
        self.mapImage = image.load(mapPath).convert()
        imageSizeW, imageSizeH = im.size
        print(im.getpixel((1, 1)))
        print(im.getpixel((100, 100)))
        self.map = [[MapTile.ROAD if im.getpixel((i, j)) == (88, 88, 88) else MapTile.WALL for i in range(1, imageSizeW)] for j in range(1, imageSizeH)]
        print(self.map[1][1])
        print(self.map[100][100])
            
    def refresh(self, screen):
        screen.blit(self.mapImage, [0,0])

class MapTile(Enum):
    WALL = 1
    ROAD = 2
