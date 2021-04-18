import random, glob, os, textwrap
from PIL import Image, ImageFont, ImageDraw

threeStarW = []
fourStarW = []
fiveStarW = []
fourStarC = []
fiveStarC = []
details = []

class gachaStats():
    def __init__(self, purplePity, yellowPity):
        self.purplePity = purplePity
        self.yellowPity = yellowPity
        self.loadImages()

    def generate(self, lower, upper):
        return random.randint(lower, upper)

    def getRating(self, item):
        return item[1]
    
    def setPity(self, purplePity, yellowPity):
        self.purplePity = purplePity
        self.yellowPity = yellowPity
    
    def loadImages(self):
        i = 0
        for filename in glob.glob('Resources/Genshin/3StarWeapons/*.png'):
            img = Image.open(filename)
            threeStarW.append((i, os.path.basename(filename).split('.')[0], img))
            i = i + 1
    
        i = 0
        for filename in glob.glob('Resources/Genshin/4StarWeapons/*.png'):
            img = Image.open(filename)
            fourStarW.append((i, os.path.basename(filename).split('.')[0], img))
            i = i + 1
        
        i = 0
        for filename in glob.glob('Resources/Genshin/5StarWeapons/*.png'):
            img = Image.open(filename)
            fiveStarW.append((i, os.path.basename(filename).split('.')[0], img))
            i = i + 1
        
        i = 0
        for filename in glob.glob('Resources/Genshin/4StarChars/*.png'):
            img = Image.open(filename)
            fourStarC.append((i, os.path.basename(filename).split('.')[0], img))
            i = i + 1
        
        i = 0
        for filename in glob.glob('Resources/Genshin/5StarChars/*.png'):
            img = Image.open(filename)
            fiveStarC.append((i, os.path.basename(filename).split('.')[0], img))
            i = i + 1
        
        for filename in glob.glob('Resources/Genshin/Details/*.png'):
            img = Image.open(filename)
            details.append(img)
            
        for i in range(0, len(details) - 1):
            details[i] = details[i].resize((int(details[i].size[0] * 0.7), 30))
 
    def getItems(self):
        items = []
        index = 0
    
        while index < 10:
            num = self.generate(0, 1000)

            #4 star
            if (6 < num <= 57  or self.purplePity == 9) and self.yellowPity != 89:
                if self.generate(0, 1) == 0:
                    weapNum = self.generate(0, len(fourStarW) - 1)
                    items.append((fourStarW[weapNum], 4))
                else:
                    charNum = self.generate(0, len(fourStarC) - 1)
                    items.append((fourStarC[charNum], 4))
                
                self.purplePity = 0
                self.yellowPity = self.yellowPity + 1
            #5 star        
            elif num <= 6 or self.yellowPity == 89:
                if self.generate(0, 1) == 0:
                    weapNum = self.generate(0, len(fiveStarW) - 1)
                    items.append((fiveStarW[weapNum], 5))
                else:
                    charNum = self.generate(0, len(fiveStarC) - 1)
                    items.append((fiveStarC[charNum], 5))
            
                self.purplePity = 0
                self.yellowPity = 0
            #3 star
            elif num > 57:
                weapNum = self.generate(0, len(threeStarW) - 1)
                items.append((threeStarW[weapNum], 3))
                self.purplePity = self.purplePity + 1
                self.yellowPity = self.yellowPity + 1
    
            index = index + 1
    
        return items

    def resizeImg(self, images):
        images = [img.convert('RGBA') for img in images]
        resizedImages = []
    
        for img in images:
            width, height = img.size
            
            if width > 1000 and height > 1000:
                left = 1100
                right = 1600
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))
                img = img.resize((200, 500)) 
            else:
                img = img.resize((200, 250)) 
                
            resizedImages.append(img)
    
        return resizedImages
    
    def connectItems(self, images, names, ratings):
        bgImg = details[3]
        widths = []
        for img in images:
            widths.append(img.size[0])
            
        totalWidth = sum(widths)
        bgImg = bgImg.resize((totalWidth + 220, 700))
        bgImg.putalpha(50)
    
        offsetX = 20
        for i in range(0, len(images)):
            bgImg.paste(images[i], (offsetX, 540 // 2 - images[i].size[1] // 2), images[i])
            
            if ratings[i] == 5:
                starDetails = details[2]
            elif ratings[i] == 4:
                starDetails = details[1]
            elif ratings[i] == 3:
                starDetails = details[0]
            
            draw = ImageDraw.Draw(bgImg)
            font = ImageFont.truetype("Resources/Fonts/calibri.ttf", 35)
        
            offsetY = 550
            x = textwrap.wrap(names[i], width=14)
            for word in x:
                width, height = font.getsize(word)
                draw.text((offsetX + (images[i].size[0] - width) // 2, offsetY), word, (255,255,255), font=font)
                offsetY = offsetY + height
                    
            bgImg.paste(starDetails, (offsetX + images[i].size[0] // 2 - starDetails.size[0] // 2, 650), starDetails)
            offsetX = offsetX + img.size[0] + 20

        return bgImg

    def multiPull(self):
        items = self.getItems()
        items = sorted(items, key=self.getRating, reverse=True)
        
        images, names, ratings = [], [], []
        for x in items:
            images.append(x[0][2])
            names.append(x[0][1])
            ratings.append(x[1])
    
        resizedImages = self.resizeImg(images)
        pullImg = self.connectItems(resizedImages, names, ratings)
    
        return pullImg
