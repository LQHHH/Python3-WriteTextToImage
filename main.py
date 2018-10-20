#!usr/bin/env python3
# -*- coding:utf-8 -*-

from WriteTextToImage import write
from ReadTextFromImage import readImage

if __name__ == '__main__':
    choose = input('a:将一段文本写入图片  b:从图片中读出这段文本:')
    if choose == 'a':
        write()
    else:
        readImage()
