import cv2
import numpy as np

def detect_lane_lines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    rho = 1
    theta = np.pi / 180
    threshold = 140
    min_line_length = 1
    max_line_gap = 5
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    line_image = np.zeros_like(image)
    draw_lines(line_image, lines)
    output = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    return output

def draw_lines(image, lines, color=(255, 0, 0), thickness=3):
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)

image = cv2.imread('2.png')

output_image = detect_lane_lines(image)

cv2.imwrite('Lane Lines Detection.png', output_image)
cv2.imshow('Lane Lines Detection', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
