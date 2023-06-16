import numpy as np

# Data from https://docs.opencv.org/3.4/de/d25/imgproc_color_conversions.html#color_convert_rgb_gray
def cvtColor(image):
    height = image.shape[0]
    width = image.shape[1]
    grayscaled = np.zeros((height, width), 'uint8')
    coeffeciency = np.array([0.299,0.587,0.114]) # RGB
    for i in range(height):
        for j in range(width):
            rgb = image[i,j,:][::-1].T
            grayscaled[i,j] = np.matmul(coeffeciency, rgb)
    return grayscaled
