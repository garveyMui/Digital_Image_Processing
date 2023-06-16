import os.path

import cv2 as cv
import numpy as np
from scipy.fft import dctn, idctn
import matplotlib.pyplot as plt

files = ['images/1.png', 'images/2.png']
for file in files:
    image = cv.imread(file, cv.IMREAD_GRAYSCALE)
    reduced_image = cv.resize(image, None, fx=0.5, fy=0.5)
    cv.imwrite('gray'+os.path.basename(file), reduced_image)
    dct_image = dctn(reduced_image, type=2, norm='ortho')
    transfer_function_highPass = np.ones_like(dct_image)
    transfer_function_lowPass = np.zeros_like(dct_image)
    size = min(dct_image.shape[0], dct_image.shape[1])
    cutoff_frequency = size*1//10
    transfer_function_highPass[:cutoff_frequency, :cutoff_frequency] = 0
    transfer_function_lowPass[:cutoff_frequency, :cutoff_frequency] = 1
    filtered_image_highPass = dct_image * transfer_function_highPass
    filtered_image_lowPass = dct_image * transfer_function_lowPass
    vmin = np.log(abs(dct_image)).min()
    vmax = np.log(abs(dct_image)).max()
    plt.subplot(121)
    plt.imshow(np.log(abs(filtered_image_highPass)), cmap='jet', origin='lower',
               vmin=vmin, vmax=vmax)
    plt.title('High pass spectrum')
    plt.subplot(122)
    plt.imshow(np.log(abs(filtered_image_lowPass)), cmap='jet', origin='lower',
               vmin=vmin, vmax=vmax)
    plt.title('Low pass spectrum')
    plt.savefig('spectrum_constrast'+os.path.basename(file))
    plt.show()

    plt.subplot(121)
    reconstructed_image_highPass = idctn(filtered_image_highPass, type=2, norm='ortho')
    cv.imwrite('images/highPass/'+os.path.basename(file), reconstructed_image_highPass)
    plt.imshow(reconstructed_image_highPass, cmap='gray')
    plt.axis('off')
    plt.title('High pass restruction')
    plt.subplot(122)
    reconstructed_image_lowPass = idctn(filtered_image_lowPass, type=2, norm='ortho')
    cv.imwrite('images/lowPass/' + os.path.basename(file), reconstructed_image_lowPass)
    plt.imshow(reconstructed_image_lowPass, cmap='gray')
    plt.axis('off')
    plt.title('Low pass restruction')
    plt.savefig('restruction_constrast' + os.path.basename(file))
    plt.show()