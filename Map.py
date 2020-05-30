from pygame import draw, Color, Rect, image, display
from PIL import Image

class Map:
    def __init__(self, mapPath):
        im = Image.open(mapPath, "r") 
        self.mapPixels = []
        imageSizeW, imageSizeH = im.size
        self.mapPiksels = [(i, j) for i in range (1, imageSizeW) for j in range (1, imageSizeH) if im.getpixel((i, j)) != (255, 255, 255)]
        self.map = image.load(mapPath).convert()

    def refresh(self, screen):
        screen.blit(self.map, [0,0])
