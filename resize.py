import glob
import numpy as np
import cv2
from PIL import Image

from resizeimage import resizeimage
'''
X_data = [[],[]]
training_data = [[],[]]
testing_data = [[],[]]
validation_data = [[],[]]

# Get subfolders with images
dirlist = glob.glob('./training_nn/by_class/by_class/*')#finds all the pathname matching a specified pattern according to the rules used by the Unix shell
dirlist.sort()


image = cv2.imread('Test_.jpg')
original_image = Image.open('Test_.jpg')
width, height = original_image.size
print('The original image size is {wide} wide x {height} high'.format(wide=width, height=height))

size=(400, 400)
resized_image = original_image.resize(size)
width, height = resized_image.size


print('The resized image size is {wide} wide x {height} high'.format(wide=width, height=height))
resized_image.save('E:/Design Project/ocr/resizedimage.jpg')

original_image.thumbnail(size, Image.ANTIALIAS)
original_image.save('E:/Design Project/ocr/resizedimage2.jpg')'''

'''def image_resize(image, width = 28, height = 28, inter = cv2.INTER_AREA):
    

   
       
    dim = (width, height)

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


image = cv2.imread('E:/Design Project/ocr/Test_.jpg')

cv2.imshow('image',image)
cv2.waitKey()

image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
_,image =cv2.threshold(image,128,255,cv2.THRESH_BINARY_INV)
image = image_resize(image)

cv2.imshow('image',image)
cv2.waitKey()
cv2.imwrite( ":/Design Project/ocr/resizedimage2.jpg", image )'''
size=(60,60)
original_image = Image.open('Test_.jpg')
original_image.thumbnail(size, Image.ANTIALIAS)
original_image.save('E:/Design Project/ocr/resizedimage2.jpg')
size=(500,500)
original_image = Image.open('E:/Design Project/ocr/resizedimage2.jpg')
original_image.thumbnail(size, Image.ANTIALIAS)
original_image.save('E:/Design Project/ocr/resizedimage4.jpg')
