from PIL import Image
import numpy as np
import random
import string
import os
import random
class generateCaptcha():
    def __init__(self,
                 width = 70,#验证码图片的宽
                 height = 25,#验证码图片的高
                 char_num = 4,#验证码字符个数
                 characters = string.digits + string.ascii_uppercase):#验证码组成，数字+大写字母
        self.width = width
        self.height = height
        self.char_num = char_num
        self.characters = characters
        self.classes = len(characters)

    def gen_captcha(self,batch_size = 50):
        path = os.path.abspath('.')
        inputPath = path + '/rawCaptcha/'
        X = np.zeros([batch_size,self.height,self.width,1])
        # 50 big arrays, each have 70
        Y = np.zeros([batch_size,self.char_num,self.classes])
        # image = ImageCaptcha(width = self.width,height = self.height)

        captcha_str_with_png = os.listdir(inputPath)
        random.shuffle(captcha_str_with_png)
        captcha_str_list = []
        for i in captcha_str_with_png:
            captcha_str_list.append(i[:4])
        captcha_count = 0
        while True:
            for i in range(batch_size):
                # captcha_count = 0

                # the string of generated captcha
                # captcha_str = ''.join(random.sample(self.characters,self.char_num))
                captcha_str = captcha_str_list[captcha_count]
                # the step to input captcha file, img = Image.open('xxx')
                # img = image.generate_image(captcha_str).convert('L')
                img = Image.open(inputPath+captcha_str_with_png[captcha_count]).convert('L')
                #####
                captcha_count += 1
                if captcha_count == 93:
                    captcha_count = 0
                img = np.array(img)
                X[i] = np.reshape(img,[self.height,self.width,1])/255.0
                for j,ch in enumerate(captcha_str):
                    Y[i,j,self.characters.find(ch)] = 1
            Y = np.reshape(Y,(batch_size,self.char_num*self.classes))
            yield X,Y

    def decode_captcha(self,y):
        y = np.reshape(y,(len(y),self.char_num,self.classes))
        return ''.join(self.characters[x] for x in np.argmax(y,axis = 2)[0,:])

    def get_parameter(self):
        return self.width,self.height,self.char_num,self.characters,self.classes

    def gen_test_captcha(self):
        image = ImageCaptcha(width = self.width,height = self.height)
        captcha_str = ''.join(random.sample(self.characters,self.char_num))
        img = image.generate_image(captcha_str)
        img.save(captcha_str + '.jpg')

if __name__ == '__main__':
    e = generateCaptcha()
    e.gen_test_captcha()