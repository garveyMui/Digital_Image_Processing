import getFrequency
import numpy as np

def accumulate(freq):
    n = len(freq)
    accumulated_freq = freq.copy()
    accumulated_freq[0] = freq[0]
    for i in range(1, n):
        accumulated_freq[i] += accumulated_freq[i-1]
    return accumulated_freq

def equalize(image):
    freq = getFrequency.get(image)
    accumulated_freq = accumulate(freq)
    equalized_image = image.copy()
    height = image.shape[0]
    width = image.shape[1]
    for i in range(height):
        for j in range(width):
            luminance = equalized_image[i,j]
            equalized_image[i,j] *= accumulated_freq[luminance]
    return equalized_image