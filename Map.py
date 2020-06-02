from pygame import draw, Color, Rect, image, display
from PIL import Image
from enum import Enum

class Map:
    def __init__(self, mapPath):
        im = Image.open(mapPath, "r") 
        imageSizeW, imageSizeH = im.size
        self.map = [[MapTile.WALL if im.getpixel((i, j)) == (53, 53, 53) else MapTile.ROAD for i in range(1, imageSizeW)] for j in range(1, imageSizeH)]
            
    def refresh(self, screen):
        screen.blit(self.map, [0,0])
        for dims in self.pointLines:
            draw.rect(screen, Color(0, 0, 255), Rect(dims))

class MapTile(Enum):
    WALL = 1
    ROAD = 2
