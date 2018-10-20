# 用pyhton3进行简单的图片隐写
![2](media/15400298782746/2.png)

## 图片相关简介
> 当我们拿到一张图片的时候，一般是知道图片的像素是多少的，比如500x500的图片，像素点就是250000
> 每个像素点都是有颜色的，图片的成像就是由于这么多不同的颜色组合在一起，我们都知道三基色(RGB)，每个像素点也是由这三种最基本的颜色来描述，区间是[0,255]
> 其实在图片中隐藏信息，就是靠在这些像素点中保存一份规则进去，但是又不能改变图片的成像
> 话不多说，先看效果如下：

### 图1是将一段文字存放进去的萌妹子图片，图2则是从图片中解出来的信息
![meizhi](media/15400298782746/meizhi.png)
![change](media/15400298782746/change.png)

### 代码结构：
* 目录下面是main.py、WriteTextImage.py、ReadTextFromImage.py以及一张原始图片
* 运行main.py,会根据指令选择执行哪份脚本
* 执行写入文件，完成后会在目录下生成一个新的文件夹存放图片，读取的时候直接改变图片的像素点进行成像
* 源码地址：<https://github.com/hongzhiqiang/Python3-WriteTextToImage>

### 下面分析主要的代码
> 首先来看main.py中的实现,导入其他两个文件的方法，获取到执行选择，进行对应的操作


```
from WriteTextToImage import write
from ReadTextFromImage import readImage

if __name__ == '__main__':
    choose = input('a:将一段文本写入图片  b:从图片中读出这段文本:')
    if choose == 'a':
        write()
    else:
        readImage()
```
> 然后WriteTextToImage.py这个文件需要重点分析


```
1. 导入图片相关的模块，需要先安装Pillow三方库
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    
2. 在走入write（）方法后，调用getImagePath()方法获取到图片的路径，然后打开图片
   def getImagePath():
			path = os.getcwd()
			list = os.listdir(path)
			for file in list:
			   #可以判断下是否是文件夹，给这个函数加个路径的参数，递归一下(哈哈哈!),这里简单处理了
			   #简单处理png格式，其他格式自行添加
			   if file.split('.')[-1] in ['png']:
			       filePath = os.path.join(path,file)
   
    return filePath
    、、、、、、此处省略部分代码
      try:
        image = Image.open(path)
    except:
        print('图片无效')
        sys.exit(0)  
 3.打开图片之后，我们通过对图片的像素进行分析和文本，定义一个比较时候的字体大小，然后将文本分割
   一个数组，分行展示
     size = image.size
     text = input('亲,输入您想要隐藏的文字:')
     text = text.strip('\n')
     length = min(size[0],size[1])/1.5
     pix = int(sqrt((pow(length,2)) / len(text)))
     
     、、、、、、
     
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
     
 4.将信息放入图片，这也是最重要的部分，我们创建一张同样大小白底的图片，然后将文本信息写入到这张
   底图片上，文字用黑色，然后我们循环每一个像素点，如果这个像素点为白色，我们在原始图片中相同位置
   的像素点，获取到三基色中的最后一个，判断最会一个是否为奇数，是的会就加1，反之如过这个像素点为
   黑色，同样也是在原始图片相同的位置，获取到三基色中的最后一个，判断是否是偶数，是的话就减去1，
   这样就把规则存到了图片中，而且对于一个像素中三基色中的一个进行+1和-1的操作，不会影响图片的最终
   成像，肉眼看到的还是一模一样的图片：
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
 
```

> 信息写入之后，不能读取出来也就没有意义了，下面分析ReadTextFromImage.py
> 其实这个读取的操作很简单，就是遍历图片的像素点，然后对像素操作过的三基色的那个值进行奇偶判断，然后给像素点赋上不同的颜色，这样就达到了取出信息的操作，这里用黑色和白色进行像素点的颜色填充

```
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
```

#### 哈哈，终于解析完毕啦，当然真的吃鸡的时候可不要搞这种暗号，不然对方还以为你发这种漂亮的妹纸图过去是有什么想法呢,哈哈！ ^_^

* 刚开始学习，闲着无聊写着总结了一下，欢迎交流......
* 源码地址：<https://github.com/hongzhiqiang/Python3-WriteTextToImage>


