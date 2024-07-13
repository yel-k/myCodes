import cv2
import numpy as np
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#https://stackoverflow.com/questions/28816046/
#displaying-different-images-with-actual-size-in-matplotlib-subplot
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()
img = cv2.imread('C:/Users/htike/OneDrive/Pictures/kpay3.jpg')
def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 10000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest
imgcp=img.copy()
# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 15, 15)
edged = cv2.Canny(gray, 100, 150)
# # Pixel values in the original image
# input_points = np.float32([[283, 81], [859, 103], [40, 1055], [709, 1236]])

# # Output image size
# width = 620
# height = 1280 # for A4

# # Desired points values in the output image
# converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

# # Perspective transformation
# matrix = cv2.getPerspectiveTransform(input_points, converted_points)
# img_output = cv2.warpPerspective(img, matrix, (width, height))
# Concatenate images
# Define a kernel (structuring element) for dilation
kernel = np.ones((5, 5), np.uint8)

# Apply dilation
dilated = cv2.dilate(edged, kernel, iterations=1)

# Contour detection
contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
peri = cv2.arcLength(contours[2], True)
biggest=cv2.approxPolyDP(contours[2], 0.015 * peri, True)
# for i in contours:
#     cv2.drawContours(img,[i],-1,(0,255,0),3)
cv2.drawContours(img,[contours[2]],-1,(0,255,0),3)

# Pixel values in the original image
points = biggest.reshape(4, 2)
input_points = np.zeros((4, 2), dtype="float32")

points_sum = points.sum(axis=1)
input_points[0] = points[np.argmin(points_sum)]
input_points[3] = points[np.argmax(points_sum)]

points_diff = np.diff(points, axis=1)
input_points[1] = points[np.argmin(points_diff)]
input_points[2] = points[np.argmax(points_diff)]

(top_left, top_right, bottom_right, bottom_left) = input_points
bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

# Output image size
max_width = max(int(bottom_width), int(top_width))
# max_height = max(int(right_height), int(left_height))
max_height = max(int(left_height), int(right_height))

# Desired points values in the output image
converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

# Perspective transformation
matrix = cv2.getPerspectiveTransform(input_points, converted_points)
img_output = cv2.warpPerspective(imgcp, matrix, (max_width, max_height))

cv2.imwrite('C:/Users/htike/OneDrive/Pictures/kpaypp.jpg', img_output)
# display('C:/Users/htike/OneDrive/Pictures/kpaypp.jpg')
# Load the image
image = Image.open('C:/Users/htike/OneDrive/Pictures/kpaypp.jpg')
# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image,lang='eng+mya')
print(text)
# Image shape modification for hstack
gray = np.stack((gray,) * 3, axis=-1)
edged = np.stack((edged,) * 3, axis=-1)
dilated = np.stack((dilated,) * 3, axis=-1)
combined = np.hstack((gray, edged,dilated,img))  # Horizontal stack
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow('img',combined)

# cv2.imshow('img2', img)
# cv2.imshow('img', img_output)

# cv2.imwrite('output/document.jpg', img_output)

cv2.waitKey(0)