from textToBlender import *

def createLadder():
    shape("base") \
        .primitive("cylinder", "10cm,2cm,10cm").subtract()


createLadder()