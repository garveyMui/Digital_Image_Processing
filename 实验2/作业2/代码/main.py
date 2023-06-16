import math
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

files = ['images/1.png', 'images/2.png']
for file in files:
    gray_image = cv.imread(file, cv.IMREAD_GRAYSCALE)
    a, b = gray_image.shape
    a /= 2
    b /= 2
    padding = math.floor(math.sqrt(a**2+b**2))//2
    gray_image = np.pad(gray_image, ((padding, padding), (padding, padding)))
    rows, cols = gray_image.shape
    M_rotate = cv.getRotationMatrix2D((cols / 2, rows / 2), 45, 1)
    rotated_image = cv.warpAffine(gray_image, M_rotate, (cols, rows))

    M_translate = np.float32([[1, 0, 20], [0, 1, 0]])
    translated_image = cv.warpAffine(gray_image, M_translate, (cols, rows))

    dft_original = np.fft.fft2(gray_image)
    dft_rotated = np.fft.fft2(rotated_image)
    dft_translated = np.fft.fft2(translated_image)

    dft_original_shifted = np.fft.fftshift(dft_original)
    dft_rotated_shifted = np.fft.fftshift(dft_rotated)
    dft_translated_shifted = np.fft.fftshift(dft_translated)

    magnitude_spectrum_original = 20 * np.log(np.abs(dft_original_shifted))
    magnitude_spectrum_rotated = 20 * np.log(np.abs(dft_rotated_shifted))
    magnitude_spectrum_translated = 20 * np.log(np.abs(dft_translated_shifted))

    plt.subplot(231), plt.imshow(np.log(magnitude_spectrum_original), cmap='jet')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(232), plt.imshow(np.log(magnitude_spectrum_rotated), cmap='jet')
    plt.title('Rotated Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(233), plt.imshow(np.log(magnitude_spectrum_translated), cmap='jet')
    plt.title('Translated Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(234), plt.imshow(gray_image, cmap='gray')
    plt.subplot(235), plt.imshow(rotated_image, cmap='gray')
    plt.subplot(236), plt.imshow(translated_image, cmap='gray')
    plt.savefig('result'+os.path.basename(file))
    plt.show()