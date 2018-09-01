import requests
from processImg import processImg
from PIL import Image
import os
from tesserocr import PyTessBaseAPI
import tesserocr
path = os.path.abspath('.')+'/'

def downloadCaptcha():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    captchaUrl = 'https://www.qichamao.com/usercenter/varifyimage'
    resp = requests.get(captchaUrl, headers=header)
    content = resp.content
    for i in range(1,101):
        resp = requests.get(captchaUrl, headers=header)
        content = resp.content
        f = open('./rawCaptcha/'+str(i)+'.png', 'wb')
        f.write(content)
        f.close()
        img = Image.open(path+'rawCaptcha/'+str(i)+'.png')
        img = processImg(img)
        img.save(path + 'rawCaptcha/' + str(i) + '.png')

def checkCaptcha(img):
    r = tesserocr.file_to_text('./rawCaptcha/0B7D.png')
    print('r=', r)


if __name__ == '__main__':
    filenamelist = os.listdir('./rawCaptcha')
    for filename in filenamelist:
        a = Image.open('./rawCaptcha/'+filename)
        print(filename,'=',tesserocr.image_to_text(a))
    # img1 = Image.open("1.png").convert('L')
    checkCaptcha('')
    # downloadCaptcha()