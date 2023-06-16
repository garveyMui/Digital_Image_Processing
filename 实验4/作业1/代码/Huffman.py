from heapq import heappop, heappush
from collections import defaultdict

class Node:
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(data):
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1
    return frequency

def build_huffman_tree(frequency):
    heap = []
    for char, freq in frequency.items():
        node = Node(char=char, freq=freq)
        heappush(heap, node)

    while len(heap) > 1:
        left_node = heappop(heap)
        right_node = heappop(heap)
        parent_node = Node(freq=left_node.freq + right_node.freq, left=left_node, right=right_node)
        heappush(heap, parent_node)

    return heap[0]

def generate_huffman_codes(root):
    codes = {}

    def traverse(node, code):
        if node.char:
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")

    traverse(root, "")
    return codes

def huffman_encode(data, codes):
    encoded_data = ""
    for char in data:
        encoded_data += codes[char]
    return encoded_data

def huffman_decode(encoded_data, root):
    decoded_data = ""
    node = root
    for bit in encoded_data:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.char:
            decoded_data += node.char
            node = root
    return decoded_data