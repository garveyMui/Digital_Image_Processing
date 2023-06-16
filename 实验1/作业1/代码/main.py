import glob
import cv2
import os

import numpy as np

import BGR2YCrCb
import Color2Gray
import equalizeHist

folder_path = "./images/Color/"
png_files = glob.glob(folder_path + '*.png')
jpg_files = glob.glob(folder_path + '*.jpg')
files = png_files+jpg_files
for file in files:
    '''part 1: 提取彩色图像的亮度通道进行直方图均衡化'''
    file_name = os.path.relpath(file, folder_path)
    list_filename = file_name.split('.')
    image = cv2.imread(file)  # (height, width, channels)
    print(file + "读取完成")
    cv2.imshow('Original', image)
    image_YCrCb = BGR2YCrCb.cvtColor(image)
    image_equalized = image_YCrCb.copy()
    image_equalized[:,:,0] = equalizeHist.equalize(image_YCrCb[:,:,0])
    re_image = cv2.cvtColor(image_equalized, cv2.COLOR_YCrCb2BGR)
    cv2.imshow('Reconstruct', re_image)
    newfile = list_filename[0]+'Equalized.'+list_filename[1]
    newfile = folder_path+"Equalized/"+newfile
    cv2.imwrite(newfile, re_image)
    print(newfile + "写入完成")

    '''part 2: 将彩色图像转换为灰度图像'''
    image_gray = Color2Gray.cvtColor(image)
    cv2.imshow('Grayscaled', image_gray)
    newfile = list_filename[0]+'Grayscaled.'+list_filename[1]
    newfile = "./images/Grayscaled/"+newfile
    cv2.imwrite(newfile, image_gray)
    print(newfile + "写入完成")

    '''part 3: 将灰度图像进行直方图均衡化'''
    image_equalized = equalizeHist.equalize(image_gray)
    cv2.imshow('Reconstruct_gray', image_equalized)
    newfile = list_filename[0]+'GrayscaledEqualized.'+list_filename[1]
    newfile = "./images/Grayscaled/Equalized/"+newfile
    cv2.imwrite(newfile, image_equalized)
    print(newfile + "写入完成")

    '''选中图像窗口，键入0进入下一循环'''
    cv2.waitKey(0)
    cv2.destroyAllWindows()
