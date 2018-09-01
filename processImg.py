import numpy
from PIL import Image
import os


# input Image.open(rawimg) , return a processed captcha
def processImg(rawImg):
    """
    process the raw image, eliminate the interfering line, separate into four images, with only one digit in eah
    :param rawImg: the captcha to process
    :return: list of four images,first four with only one digit in each image; and the full processed image
    """
    # rawImg = Image.open(ImgPath)
    BlackWhiteImage = rawImg.convert('1')
    imArray = numpy.array(BlackWhiteImage)[5:,5:75 ]  #
    imArray = imArray[:len(imArray)-5]
    print(imArray.shape)
    img = Image.fromarray(numpy.uint8(imArray * 255))
    # img.show()

    for i in range(1,24):
        for j in range(1,69):
            whitecount = 0
            if imArray[i][j-1] == True:
                whitecount += 1
            if imArray[i][j+1] == True:
                whitecount += 1
            if imArray[i-1][j] == True:
                whitecount += 1
            if imArray[i-1][j+1] == True:
                whitecount += 1
            if imArray[i-1][j-1] == True:
                whitecount += 1
            if imArray[i+1][j-1] == True:
                whitecount += 1
            if imArray[i+1][j] == True:
                whitecount += 1
            if imArray[i+1][j-1] == True:
                whitecount += 1

            if whitecount >= 6:
                imArray[i][j] = True

    for i in range(1,23):
        imArray[i][0] = True
        imArray[i][69] = True

    for i in range(0,70):
        imArray[0][i] = True
        imArray[24][i] = True



    img = Image.fromarray(numpy.uint8(imArray * 255))

    return img

if __name__ == '__main__':
    processImg(Image.open(os.path.abspath('.')+'/ProcessTestImg.png'))