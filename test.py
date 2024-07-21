import cv2
import numpy as np
from matplotlib import pyplot as plt

from PIL import Image, ImageTk

enhance_path = 'C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/t.jpg'
def rotate_image(image_path, angle):
    # Load the image
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    
    # Calculate the center of the image
    center = (w // 2, h // 2)
    
    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, M, (w, h))
    
    return rotated_image
# Read the image
img = cv2.imread(enhance_path)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Detect lines using Hough Line Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# Initialize variables to find the longest line
max_length = 0
longest_line = None

# Iterate over detected lines
for r_theta in lines:
    r, theta = r_theta[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * r
    y0 = b * r
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    # Calculate the length of the line segment
    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Check if the current line is the longest
    if length > max_length:
        max_length = length
        longest_line = (x1, y1, x2, y2)

    # Draw the line on the image
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# If a longest line was found, calculate its angle
angle_degrees=0
if longest_line:
    x1, y1, x2, y2 = longest_line
    dx = x2 - x1
    dy = y2 - y1
    angle_radians = np.arctan2(dy, dx)
    angle_degrees = np.degrees(angle_radians)

    print(f"The longest line angle is {angle_degrees:.2f} degrees")

# Save the image with the detected lines
cv2.imwrite('linesDetected.jpg', img)
reimg=rotate_image(enhance_path,angle_degrees)
cv2.imwrite("temp.jpg",reimg)
rotated_image = rotate_image('temp.jpg',90)
cv2.imwrite('temp2.jpg',rotated_image)
# Display the image
cv2.imshow('Detected Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
