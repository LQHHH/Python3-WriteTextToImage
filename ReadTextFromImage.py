#!usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from PIL import Image

def readImage():
    filePath = os.path.join(os.getcwd(),'TextImage/change.png')
    image = Image.open(filePath)
    size = image.size
    pix = image.load()
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            if pix[x,y][2] %2 == 0:
                pix[x,y] = (0,0,0)
            else:
                pix[x, y] = (255, 255, 255)

    image.save(filePath)
    print('*****您的文本已经成功解读************')

