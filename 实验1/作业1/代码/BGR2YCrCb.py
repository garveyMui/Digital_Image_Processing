import cv2
import os
import glob
import numpy as np
'''
For test RGB or BGR
'''
def getChannelRGB(image, channel='B'):
    dic = {'B':0, 'G':1, 'R':2}
    firstChannel = np.squeeze(image[:,:,0])
    height = firstChannel.shape[0]
    width = firstChannel.shape[1]    
    new_image = np.zeros((height, width, 3), firstChannel.dtype)
    new_image[:, :, dic[channel]] = firstChannel
    return new_image
# Data from https://docs.opencv.org/3.4/de/d25/imgproc_color_conversions.html#color_convert_rgb_ycrcb
def cvtColor(image):
    transition = np.array([[0.299, 0.587, 0.114],
                           [0.713*(1-0.299), -(0.713*0.587), -(0.713*0.114)],
                           [-(0.564*0.299), -(0.564*0.587), 0.564*(1-0.114)]])
    shift = np.array([0, 128, 128]).T
    new_image = image.copy()
    height = image.shape[0]
    width = image.shape[1]
    for i in range(height):
        for j in range(width):
            rgb = image[i,j,:][::-1].T
            new_image[i,j,:] = np.matmul(transition, rgb) + shift
    return new_image
if __name__ == '__main__':
    folder_path = "../images/"
    png_files = glob.glob(folder_path + '*.png')
    for file in png_files:
        print(file)
        image = cv2.imread(file) #(height, width, channels)
        cv2.imshow('Original', image)
        # new_image = cvtColor(image)
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        re_image = cv2.cvtColor(new_image, cv2.COLOR_YCrCb2BGR)
        cv2.imshow('YCrCb', new_image)
        cv2.imshow('reconstruct', re_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    
