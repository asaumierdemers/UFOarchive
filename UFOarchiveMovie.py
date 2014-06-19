# DrawBot script that generate a "flip book" animation from UFOs

saveMovie = True

folders = [
    u"/path/to/your/ufo/archive/folder",
    #u"/path/to/your/ufo/archive/folder",
]

# you might want to change the layout here

w, h = 500, 600 # width, height
x, y = 250, 150 # xpos, ypos
s = 0.5 # scale, e.g. 0.5 * 1000 UPM = 500 pt


def drawFrame(font, glyph):
    newPage(w, h)
    save()
    translate(x, y)
    scale(s)
    pen = CocoaPen(font)
    glyph.draw(pen)
    translate(-glyph.width/2, 0)
    drawPath(pen.path)
    restore()

from fontTools.pens.cocoaPen import CocoaPen
from robofab.world import OpenFont
import string
import os

paths = []
for folder in folders:
    for root, dirs, files in os.walk(folder):
        for directory in dirs:
            if directory.endswith(".ufo"):
                paths.append(os.path.join(root, directory))

fonts = []
for path in paths:
    font = OpenFont(path)
    fonts.append(font)
    
skipCount = 0
frameCount = 0

letters = string.letters

for letter in letters:
    
    prevPoints = None
    for font in fonts:
        
        if font.has_key(letter):
            glyph = font[letter]
        else:
            continue
    
        points = [(point.x, point.y) for contour in glyph.contours for point in contour.points]
        if points != prevPoints and len(points) > 1:
            drawFrame(font, glyph)
            frameCount+=1
        else:
            skipCount+=1
        prevPoints = points


print "%s fonts" % str(len(fonts))
print "%s frames" % frameCount
print "---"
print "skipped %s identical glyphs" % skipCount

if saveMovie:
    saveImage(["~/Desktop/UFOarchive.mov"])