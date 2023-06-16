import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import BGR2YCrCb
'''
(height, width, channels)
'''

# for YCrCb space 8bits
def get(image):
    counts = np.zeros(256)
    height = image.shape[0]
    width = image.shape[1]
    for i in range(height):
        for j in range(width):
            counts[image[i, j]] += 1
    freq = counts/(height*width)
    return freq

if __name__ == '__main__':
    folder_path = "../images/"
    png_files = glob.glob(folder_path + '*.png')
    for file in png_files:
        print(file)
        image = cv2.imread(file)  # (height, width, channels)
        cv2.imshow('Original', image)
        new_image = BGR2YCrCb.cvtColor(image)
        freq = get(new_image)
        plt.bar(np.arange(0, 256, 1), freq)
        plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break