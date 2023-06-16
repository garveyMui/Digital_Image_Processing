import numpy as np

class Encoder():
    def __init__(self, image):
        self.image = image

    def get_bits_width(self,num):
        bits_width = 0
        while num != 0:
            num = num >> 1
            bits_width += 1
        return bits_width

    def quarter_flatten(self,data):
        flatten_data = []
        height, width = data.shape
        iteration = 1
        i, j = (0, 0)
        flatten_data.append(data[i, j])
        mark = True
        while(len(flatten_data) < height*width):
            if iteration % 2 == 1:
                if mark:
                    j += 1
                else:
                    i += 1
                flatten_data.append(data[i, j])
                for step in range(iteration):
                    i += 1
                    j -= 1
                    flatten_data.append(data[i, j])
            else:
                if mark:
                    i += 1
                else:
                    j += 1
                flatten_data.append(data[i, j])
                for step in range(iteration):
                    i -= 1
                    j += 1
                    flatten_data.append(data[i, j])
            if mark:
                iteration += 1
            else:
                iteration -= 1
            if iteration == height:
                mark = False
                iteration -= 2
        return np.asarray(flatten_data)

    def rle_encode(self,data):
        encoded_data = []
        count = 1
        for i in range(1, len(data)):
            if data[i] == data[i-1]:
                count += 1
            else:
                encoded_data.append((count, data[i-1]))
                count = 1
        encoded_data.append((count, data[-1]))
        return encoded_data

    def rle_decode(self,encoded_data):
        decoded_data = []
        for value, count in encoded_data:
            decoded_data.extend([value] * count)
        return decoded_data
    def encode(self, show=False):
        img_quarter_flatten = self.quarter_flatten(self.image)
        if show:
            print("原矩阵为：")
            print(self.image)
            print("展开结果：")
            print(img_quarter_flatten)
        data = []
        for i in img_quarter_flatten:
                data.append(i)
        encoded_data = self.rle_encode(data)
        if show:
            print("行程编码结果：", end="")
            print(encoded_data)
        max_bits_width = 0
        for t in encoded_data:
            max_bits_width = max(self.get_bits_width(t[0]), max_bits_width)
        encoded_size = 0
        for t in encoded_data:
            encoded_size += max_bits_width
            encoded_size += 8
        if show:
            print(f"压缩编码位数：{encoded_size}bits")
        return encoded_size

