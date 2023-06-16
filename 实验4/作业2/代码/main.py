import cv2 as cv
import numpy as np
from scipy.fft import dctn, idctn
from Encoder import Encoder

def get_quantization_table(quality=100, flag=0):
    quality = max(1, min(quality, 100))
    if quality < 50:
        quality_scale = 5000 // quality
    else:
        quality_scale = 200 - quality * 2
    luma_table = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float32)
    chrominance_table = np.array([
        [17, 18, 24, 47, 99, 99, 99, 99],
        [18, 21, 26, 66, 99, 99, 99, 99],
        [24, 26, 56, 99, 99, 99, 99, 99],
        [47, 66, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99]], dtype=np.float32)

    if flag == 0:
        table = luma_table
    else:
        table = chrominance_table
    scaled_table = np.clip((table * quality_scale + 50) // 100, 1, 255)

    return scaled_table
files = ['1.jpg', '2.jpg']
for file in files:
    image = cv.imread('images/'+file)
    image = cv.resize(image, None, fx=0.5, fy=0.5)
    image = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)
    res_image = image.copy()
    image_height, image_width, _ = image.shape
    C1 = image_height*image_width*3*8
    block_size = 8
    qualities = [10, 20, 40]
    for quality in qualities:
        compression_size = 0
        for c in range(3):
            for y in range(0, image_height, block_size):
                for x in range(0, image_width, block_size):
                    block = image[y:y+block_size, x:x+block_size, c].astype(int)-128
                    dct_block = dctn(block, type=2, norm='ortho')
                    quantization_table = get_quantization_table(quality, flag=c)  # Obtain or generate the quantization table
                    quantized_block = np.round(dct_block / quantization_table).astype(np.int16)
                    encoder = Encoder(quantized_block)
                    block_compression_size = encoder.encode(show=False)
                    # if block_compression_size > 28:
                    #     print("here")
                    compression_size += block_size
                    inverse_quantized_block = quantized_block * quantization_table
                    reconstructed_block = idctn(inverse_quantized_block, type=2, norm='ortho')+128
                    reconstructed_block = np.uint8(reconstructed_block)
                    res_image[int(y):int(y)+block_size, int(x):int(x)+block_size, c] = reconstructed_block
        C2 = compression_size
        print("压缩后字节数{:d}".format(C2//8))
        squared_diff = (image - res_image) ** 2
        mean_squared_diff = np.mean(squared_diff)
        rmsd = np.sqrt(mean_squared_diff)
        print("均方根误差：{:.2f}".format(rmsd))
        print("压缩率：{:.2f}".format(C1/C2))
        image_bgr = cv.cvtColor(image, cv.COLOR_YCrCb2BGR)
        res_image_bgr = cv.cvtColor(res_image, cv.COLOR_YCrCb2BGR)
        cv.imshow("original", image_bgr)
        cv.imwrite(f"images/quality:{quality}"+file, res_image_bgr)
        cv.imshow("result", res_image_bgr)
        cv.waitKey(0)
        cv.destroyAllWindows()
