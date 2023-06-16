import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('1.png')
plt.imshow(image)
plt.show()
cv2.imshow('original', image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
radius = 3
threshold = 35

corners = []
for i in range(radius, gray.shape[0] - radius):
    for j in range(radius, gray.shape[1] - radius):
        pixel = gray[i, j]
        # if i >= 320 and j == 114:
        #     print("here")
        neighbor_region = gray[i - radius : i + radius + 1, j - radius : j + radius + 1].astype(int)
        diff = np.abs(neighbor_region - pixel).astype(int)
        zero_rank = diff < 120
        one_rank = diff >= 120
        diff[zero_rank] = 0
        diff[one_rank] = 255
        scaled = np.exp(-diff/255)
        susan_score = np.sum(scaled) # Similarity with nuclear
        if susan_score <= threshold:
            corners.append((i, j))

for corner in corners:
    y, x = corner
    cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

# Word另存后图像最右侧与最下侧有莫名黑边，赋值255以删除黑边
image[-1,:,:] = 255
image[:,-1,:] = 255
cv2.imwrite('Corners Detected.png', image)
cv2.imshow('Corners Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
