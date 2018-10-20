#!usr/bin/env python3
# -*- coding:utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import sys
from math import sqrt


def write():
    filePath = getImagePath()
    openImage(filePath)

def getImagePath():
    path = os.getcwd()
    list = os.listdir(path)
    for file in list:
        #可以判断下是否是文件夹，给这个函数加个路径的参数，递归一下(哈哈哈!),这里简单处理了
        #简单处理png格式，其他格式自行添加
        if file.split('.')[-1] in ['png']:
            filePath = os.path.join(path,file)

    return filePath

def openImage(path):
    try:
        image = Image.open(path)
    except:
        print('图片无效')
        sys.exit(0)

    size = image.size
    text = input('亲,输入您想要隐藏的文字:')
    text = text.strip('\n')
    length = min(size[0],size[1])/1.5
    pix = int(sqrt((pow(length,2)) / len(text)))

    textList = handleText(pix,text,size)
    textImage = makeImage(textList,size,pix)
    saveImage(image,textImage)

def makeImage(textList,size,pix):
    image = Image.new('RGB',size,color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/Library/Fonts/Songti.ttc',pix)
    for i in range(0,len(textList)):
        draw.text((0,pix*i),textList[i],font=font,fill=(0,0,0))
    return image

def saveImage(image,textImage):
    size = image.size
    pixImage = image.load()
    pixTextImage = textImage.load()
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            if pixTextImage[x,y] == (255,255,255):
                if pixImage[x,y][2]%2 != 0 :
                    pixImage[x,y] = (pixImage[x,y][0],pixImage[x,y][1],pixImage[x,y][2]-1)

            else:
                if pixImage[x, y][2] % 2 == 0:
                    pixImage[x, y] = (pixImage[x, y][0], pixImage[x, y][1], pixImage[x, y][2]+1)

    path = os.getcwd()
    filePath = os.path.join(path,'TextImage')
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    image.save(os.path.join(filePath,'change.png'),'PNG')
    print('*****您的文本已经成功写入图片************')


def handleText(pix,text,size):
    textList = []
    lineTextNum = size[0]//pix
    lineNum = len(text)//lineTextNum+1 if len(text)%lineTextNum > 0 else len(text)//lineTextNum
    if lineNum == 0:
        textList.append(text)
    else:
        for i in range(0,lineNum):
            subText = text[lineTextNum*i:(i+1)*lineTextNum]
            textList.append(subText)

    return textList