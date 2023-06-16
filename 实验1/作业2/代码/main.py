import glob
import cv2
from Bilateral import Processor

if __name__ == '__main__':
    folder_paths = ["./images/GaussianNoise/", "./images/PepperNoise/"]
    # folder_paths = ["./images/GaussianNoise/"]
    arguments = [[0, 0], [1e-4, 1e-2]]
    # arguments = [[1e-4, 1e-2]]
    for folder_path in folder_paths:
        jpg_files = glob.glob(folder_path + '*.jpg')
        png_files = glob.glob(folder_path + '*.png')
        files = jpg_files+png_files
        for file in files:
            image = cv2.imread(file)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('original', img_gray)
            for argument in arguments:
                processor = Processor(image[:,:,0], 7, argument[0], argument[1])
                filtered_image = processor.bilateralFilter()
                cv2.imshow('filtered_image', filtered_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
