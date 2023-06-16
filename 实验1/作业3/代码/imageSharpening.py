import numpy as np
import glob
import cv2 as cv
import os

kernel1x=np.array([-1,0,1,-2,0,2,-1,0,1])
kernel1y=np.array([1,2,1,0,0,0,-1,-2,-1])
kernel2x=np.array([-1,0,1,-1,0,1,-1,0,1])
kernel2y=np.array([1,1,1,0,0,0,-1,-1,-1])
def sharpen(img, kernelX, kernelY):
    height = img.shape[0]
    width = img.shape[1]
    sharpened_img = img.copy()
    for i in range(1, height-1):
        for j in range(1, width-1):
            window = img[i - 1:i + 2, j - 1:j + 2].flatten()
            sharpened_img[i, j] = abs(np.dot(window, kernelX))
            sharpened_img[i, j] += abs(np.dot(window, kernelY))
    return sharpened_img
if __name__ == '__main__':
    folder_path = "./images/"
    jpg_files = glob.glob(folder_path+"*.jpg")
    png_files = glob.glob(folder_path+"*.png")
    files = jpg_files+png_files
    for file in files:
        print(file)
        basename = os.path.basename(file)
        img = cv.imread(file, cv.IMREAD_GRAYSCALE)
        cv.imwrite(folder_path + 'grayscale/' + basename, img)
        cv.imshow('original', img)
        sharpened_img = img.copy()
        sharpened_img[:, :] = sharpen(img[:,:], kernel1x, kernel1y)
        cv.imwrite(folder_path + 'kernel1/' + basename, sharpened_img)
        cv.imshow('kernel1', sharpened_img)
        sharpened_img1 = img.copy()
        sharpened_img1[:, :] = sharpen(img[:, :], kernel2x, kernel2y)
        cv.imwrite(folder_path + 'kernel2/' + basename, sharpened_img1)
        cv.imshow('kernel2', sharpened_img1)
        cv.waitKey(0)
        cv.destroyAllWindows()