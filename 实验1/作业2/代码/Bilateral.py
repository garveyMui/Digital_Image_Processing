import numpy as np
import math
import concurrent.futures
class Processor:
    def __init__(self, image, diameter, var_space, var_color):
        self.image = image
        self.diameter = diameter
        self.var_space = var_space
        self.var_color = var_color
    def weight(self, i, j, k, l):
        try:
            component_space = -((i-k)**2+(j-l)**2)*(2*self.var_space) #以乘代除
            component_color = -(abs(np.int32(self.image[i,j])-np.int32(self.image[k,l])))*(2*self.var_color)
            res = math.exp(component_space+component_color)
            return res
        except Exception as e:
            print("An exception occurred:", e)
            print(component_space, component_color, res)
    def get_kernel_element(self, x_central, y_central, i, j):
        return self.weight(x_central, y_central, i, j)

    def _getKernel(self, x_central, y_central):
        kernel = np.zeros((self.diameter, self.diameter))
        radius = math.ceil(self.diameter / 2)
        data = np.zeros((self.diameter*self.diameter, 4), int)
        data[:,0] = x_central
        data[:,1] = y_central
        for i in range(x_central - radius + 1, x_central + radius):
            for j in range(y_central - radius + 1, y_central + radius):
                data[(i - (x_central - radius + 1)) * self.diameter + j - (y_central - radius + 1), 2] = i
                data[(i - (x_central - radius + 1)) * self.diameter + j - (y_central - radius + 1), 3] = j
        data_x_central = data[:, 0]
        data_y_central = data[:, 1]
        data_i = data[:, 2]
        data_j = data[:, 3]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            kernel_flat = list(executor.map(self.get_kernel_element, data_x_central, data_y_central, data_i, data_j))
        kernel = np.array(kernel_flat).reshape(self.diameter, self.diameter)
        return kernel/kernel.sum()
    def getKernel(self, x_central, y_central):
        kernel = np.zeros((self.diameter, self.diameter))
        radius = math.ceil(self.diameter / 2)
        for i in range(x_central-radius+1, x_central+radius):
            for j in range(y_central-radius+1, y_central+radius):
                kernel[i-(x_central-radius+1), j-(y_central-radius+1)] = \
                    self.weight(x_central, y_central, i, j)
        return kernel/kernel.sum()
    def bilateralFilter(self):
        height = self.image.shape[0]
        width = self.image.shape[1]
        filtered_image = self.image.copy()
        radius = math.ceil(self.diameter / 2)
        for i in range(height-self.diameter+1):
            print(f"{round(100 * i / height)}%\r")
            for j in range(width-self.diameter+1):
                kernel = self.getKernel(i+radius-1,j+radius-1)
                kernel = kernel.flatten()
                window = self.image[i:i+self.diameter,j:j+self.diameter]
                window = window.flatten()
                filtered_image[i+radius-1,j+radius-1] = np.dot(kernel, window)
        return filtered_image

def medianValueFilter(image, kernel_size):
    height = image.shape[0]
    width = image.shape[1]
    filtered_image = image.copy()
    radius = round(kernel_size/2)
    kernel_total = kernel_size*kernel_size
    for i in range(height-kernel_size+1):
        for j in range(width-kernel_size+1):
            kernel = image[i:i+kernel_size,j:j+kernel_size].flatten()
            filtered_image[i+radius-1,j+radius-1] = np.sort(kernel)[kernel_total//2]
    return filtered_image



