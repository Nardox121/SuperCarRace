from pygame import draw, Color, Rect, image, display
from PIL import Image

class Map:
    def __init__(self, mapPath):
        im = Image.open(mapPath, "r") 
        imageSizeW, imageSizeH = im.size
        self.mapPixels = [(i, j) for i in range (1, imageSizeW) for j in range (1, imageSizeH) if im.getpixel((i, j)) != (255, 255, 255)]
        self.map = image.load(mapPath).convert()
        self.rectMap = [Rect((i, j), (1, 1)) for i, j in self.mapPixels]
        
        #points
        self.pointLines = [((30, 60), (100, 1))]


    def refresh(self, screen):
        screen.blit(self.map, [0,0])
        for dims in self.pointLines:
            draw.rect(screen, Color(0, 0, 255), Rect(dims))
