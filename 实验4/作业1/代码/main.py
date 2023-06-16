import numpy as np
from Huffman import *

image = np.asarray([[1,1,1,2],
                    [1,1,2,2],
                    [5,5,5,7],
                    [0,0,7,7]]).astype(int)
dict_image = {1:'a',2:'b',5:'c',7:'d',0:'f'}
data = []
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        data.append(dict_image[image[i,j]])
data = "".join(data)

frequency = calculate_frequency(data)
huffman_tree = build_huffman_tree(frequency)
huffman_codes = generate_huffman_codes(huffman_tree)
print("哈夫曼编码结果：", end="")
print(huffman_codes)
print("")
def get_bits_width(num):
    bits_width = 0
    while num != 0:
        num = num >> 1
        bits_width += 1
    return bits_width

def square_flatten(data):
    flatten_data = []
    height, width = data.shape
    iteration = 1
    i, j = (0, 0)
    flatten_data.append(data[i, j])
    while(len(flatten_data) < height*width):
        if iteration % 2 == 1:
            j += 1
            flatten_data.append(data[i, j])
            for step in range(iteration):
                i += 1
                flatten_data.append(data[i, j])
            for step in range(iteration):
                j -= 1
                flatten_data.append(data[i, j])
        else:
            i += 1
            flatten_data.append(data[i, j])
            for step in range(iteration):
                j += 1
                flatten_data.append(data[i, j])
            for step in range(iteration):
                i -= 1
                flatten_data.append(data[i, j])
        iteration += 1

    return np.asarray(flatten_data)

def quarter_flatten(data):
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

def rle_encode(data):
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

def rle_decode(encoded_data):
    decoded_data = []
    for value, count in encoded_data:
        decoded_data.extend([value] * count)
    return decoded_data

print("******************直角S型展开******************")
img_square_flatten = square_flatten(image)
print("展开结果：", end="")
print(img_square_flatten)
data = []
for i in img_square_flatten:
        data.append(dict_image[i])
encoded_data = rle_encode(data)

huffman_dict = {}
for s in data:
    huffman_dict[s] = huffman_encode(s, huffman_codes)

for i in range(len(encoded_data)):
    t = encoded_data[i]
    encoded_data[i] = (t[0], huffman_dict[t[1]])
print("行程编码结果：", end="")
print(encoded_data)
max_bits_width = 0
for t in encoded_data:
    max_bits_width = max(get_bits_width(t[0]), max_bits_width)
encoded_size = 0
for t in encoded_data:
    encoded_size += max_bits_width
    encoded_size += len(t[1])
print(f"压缩编码位数：{encoded_size}bits")

C1 = 3*image.shape[0]*image.shape[1]
C2 = encoded_size
print("直角S型展开混合编码压缩率: {:.4f}".format(C1/C2))
print("")
print("******************45度角S型展开******************")
img_quarter_flatten = quarter_flatten(image)
print("展开结果：", end="")
print(img_quarter_flatten)
data = []
for i in img_quarter_flatten:
        data.append(dict_image[i])
encoded_data = rle_encode(data)

huffman_dict = {}
for s in data:
    huffman_dict[s] = huffman_encode(s, huffman_codes)

for i in range(len(encoded_data)):
    t = encoded_data[i]
    encoded_data[i] = (t[0], huffman_dict[t[1]])
print("行程编码结果：", end="")
print(encoded_data)
max_bits_width = 0
for t in encoded_data:
    max_bits_width = max(get_bits_width(t[0]), max_bits_width)

encoded_size = 0
for t in encoded_data:
    encoded_size += max_bits_width
    encoded_size += len(t[1])

print(f"压缩编码位数：{encoded_size}bits")

C1 = 3*image.shape[0]*image.shape[1]
C2 = encoded_size
print("45度角S型展开混合编码压缩率: {:.4f}".format(C1/C2))